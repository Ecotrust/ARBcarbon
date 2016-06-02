
# coding: utf-8

# In[1]:

"""FPS2ARB.
FPS-to-ARB Carbon Calculation.
Takes two CSV files in current working directory that were exported from FPS 
(Forest Planning and Projection System) database containing forest inventory 
data, calculates carbon storage for each tree, and documents the calculation 
parameters and writes outputs to a new CSV file, one for each property 
detected in the FPS_ADMIN table/CSV.

Usage:
    FPS2ARB.py [options]
    FPS2ARB.py [-h | --help]
    FPS2ARB.py [--version]

Options:
    -h --help  Show this screen
    --version  Show version
    --property <property>  Name of property to include
    --years <year>  Year for calculations to be made
    --region <region>  Region for equations (WOR, EOR, WWA, EWA, CA)
"""


# In[2]:

from docopt import docopt
import pandas as pd
import math
from ARB_Volume_Equations import *
from ARB_Biomass_Equations import *
from ARB_Equation_Assignments import *


# In[ ]:

if __name__ == "__main__":
    
    args = docopt(__doc__, version='1.0')

    print args['--property']
    properties_to_run = args['--property']
    if not properties_to_run:
        properties_to_run = 'all'
    print properties_to_run
    
    report_yr = args['--year']
    
    region = args['--region']
    if not region:
        region = raw_input("Choose which regional equations to use (WOR, EOR, WWA, EWA, or CA):")
        print "Thanks! All calculations to be done using ", region + " equations\n"


# In[3]:

# Read in the CSV files that were exported from FPS
try:
    FPS_DBHCLS = pd.read_csv('DBHCLS.csv')
    FPS_ADMIN = pd.read_csv('ADMIN.csv')
    print "Successfully read in DBHCLS and ADMIN tables.\n" 
except IOError:
    print "Could not find your DBHCLS and ADMIN CSV files. Please export them from your FPS database in to the same folder as this script.\n"


# In[4]:

# check if all species are recognized from user's crosswalk table
DBHCLS_spp = pd.unique(FPS_DBHCLS.SPECIES) # the species found in the FPS Database
spp_used_list = species_used.Your_species_code.tolist() # species found in the user's crosswalk table
print "Found " + str(len(species_used)) + " species in the species crosswalk spreadsheet and " + str(len(DBHCLS_spp)) + " species in the DBHCLS table.\n"
# if not, list the species that are not recognized 
missing_spp = [spp for spp in DBHCLS_spp if spp not in spp_used_list] # species_used comes from crosswalk table, in ARB_Equation_Assignments script
if len(missing_spp) >0:
    print str(len(missing_spp)) + " species found in DBHCLS but missing from the crosswalk spreadsheet will not have carbon storage calculated:"
    print "(" + ', '.join(str(spp) for spp in missing_spp) + ")\n"
else:
    print "All species will have carbon calculations.\n"


# In[5]:

# tree_list, a dataframe of all the trees in the DBHCLS table
tree_list = FPS_DBHCLS[['STD_ID', 'RPT_YR', 'SPECIES', 'GRP', 'PlotTree', 'TREES', 'DBH', 'HEIGHT']].set_index('STD_ID')

# hold out any trees that were not in species crosswalk spreadsheet
if len(missing_spp) >0:
    tree_list = tree_list.loc[~tree_list['SPECIES'].isin(missing_spp)]
    missing_trees = tree_list.loc[tree_list['SPECIES'].isin(missing_spp)]


# In[ ]:

if report_yr: # if the user specified a specific report year
        tree_list = tree_list.loc[tree_list['RPT_YR'] == report_yr] # only include trees from that year


# In[6]:

# stand_list, a dataframe of all stands in the ADMIN table
stand_list = FPS_ADMIN[['STD_ID', 'RPT_YR', 'MSMT_YR', 'Property', 'AREA_RPT', 'AREA_GIS', 'AREA_NET']].set_index('STD_ID')


# In[7]:

region = 'WOR'
# add new columns to the tree_list:

# Region
tree_list['FIA_Region'] = region

# ARB Volume Equation Number & Total Cubic Volume (CVTS, cubic volume including top and stump)
tree_list['Vol_Eq'] = tree_list['SPECIES'].apply(lambda x: getattr(species_classes[x], region+'_VOL').func_name.split('_')[1])

def get_vol(row):
    return calc_vol(row.DBH, row.HEIGHT, 'CVTS', getattr(species_classes[row.SPECIES], region+'_VOL'))
tree_list['CVTS_ft3'] = tree_list.apply(get_vol, axis = 1) # calculate cubic volume for each row

# Wood Density and Stem Biomass
# wood density in units of lbs/ft3 and cubic volume in ft3
tree_list['Wood_density_lbsft3'] = tree_list['SPECIES'].apply(lambda x: getattr(species_classes[x], 'wood_dens'))
tree_list['Stem_biomass_UStons'] = (tree_list['CVTS_ft3'] * tree_list['Wood_density_lbsft3'])/2000.0
tree_list['Stem_biomass_kg'] = (tree_list['CVTS_ft3'] * tree_list['Wood_density_lbsft3'])*0.453592

# Bark biomass equation and calculation
tree_list['BarkBio_Eq'] = tree_list['SPECIES'].apply(lambda x: getattr(species_classes[x], region+'_BB').func_name.split('_')[1])
def get_bark_bio(row): # convert DBH and HT from English to Metric units
    # equations use metric units, so convert DBH and HT from English to Metric units
    # equations return units of kg
    return check_BB(row.DBH*2.54, row.HEIGHT*0.3048, row.Wood_density_lbsft3, getattr(species_classes[row.SPECIES], region+'_BB'))
tree_list['Bark_biomass_kg'] = tree_list.apply(get_bark_bio, axis = 1)

# Branch biomass equation and calculation
tree_list['BranchBio_Eq'] = tree_list['SPECIES'].apply(lambda x: getattr(species_classes[x], region+'_BLB').func_name.split('_')[1])
def get_branch_bio(row): 
    # equations use metric units, so convert DBH and HT from English to Metric units
    # equations return units of kg
    return check_BLB(row.DBH*2.54, row.HEIGHT*0.3048, getattr(species_classes[row.SPECIES], region+'_BLB'))
tree_list['Branch_biomass_kg'] = tree_list.apply(get_branch_bio, axis = 1)

# Above-ground biomass
tree_list["Aboveground_biomass_kg"] = tree_list['Stem_biomass_kg'] + tree_list['Bark_biomass_kg'] + tree_list['Branch_biomass_kg']

# Below-ground biomass, calculated using Cairns et al. (1997) Equation #1
tree_list["Belowground_biomass_kg"] = tree_list["Aboveground_biomass_kg"].apply(cairns)

# Total live tree biomass
tree_list["LiveTree_biomass_kg"] = tree_list["Aboveground_biomass_kg"] + tree_list["Belowground_biomass_kg"]

