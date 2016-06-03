
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
    --year <year>  Year for calculations to be made
    --region <region>  Region for equations (WOR, EOR, WWA, EWA, CA)
"""


# In[17]:

import os
from docopt import docopt
import pandas as pd
import math
import time
from ARB_Volume_Equations import *
from ARB_Biomass_Equations import *
from ARB_Equation_Assignments import *


# In[ ]:

if __name__ == "__main__":
    
    args = docopt(__doc__, version='1.0')

    properties_to_run = args['--property']
    report_yr = args['--year']
    region = args['--region']


# In[3]:

# Read in the CSV files that were exported from FPS
try:
    FPS_DBHCLS = pd.read_csv('DBHCLS.csv')
    FPS_ADMIN = pd.read_csv('ADMIN.csv')
    print "Successfully read in DBHCLS and ADMIN tables.\n" 
except IOError:
    print "Could not find your DBHCLS and ADMIN CSV files. Please export them from your FPS database in to the same folder as this script.\n"


# In[4]:

# stand_list, a dataframe of all stands in the ADMIN table
stand_list = FPS_ADMIN[['STD_ID', 'RPT_YR', 'MSMT_YR', 'Property', 'AREA_GIS']]

# tree_list, a dataframe of all the trees in the DBHCLS table
tree_list = FPS_DBHCLS[['RPT_YR', 'STD_ID', 'PlotTree', 'GRP', 'SPECIES', 'TREES', 'DBH', 'HEIGHT']]


# In[6]:

# report_yr = None
# properties_to_run = None
# region = None


# In[7]:

# Prompt user to specify a single property
all_properties = pd.unique(stand_list['Property']).tolist()
if not properties_to_run:
    print str(len(all_properties)) + ' properties found in the ADMIN table:',
    print ', '.join(str(prop) for prop in all_properties) + "\n"
    
    while True:
        chosen_prop = raw_input('Choose a property to run, or type ALL: ')
        if chosen_prop.lower() == 'all':
            properties_to_run = all_properties
            print 'Running carbon calculations for all properties.\n'
            break
        elif chosen_prop in all_properties:
            properties_to_run = [chosen_prop]
            print 'Running carbon calculations for ' + properties_to_run[0] + '\n'
            break
        else:
            print 'Property not recognized. Try again.\n'


# In[8]:

# Prompt user to specify a region
if not region:
    while True:
        region = raw_input('Choose which regional volume equations to use (WOR, EOR, WWA, EWA, or CA): ')
        if region in ['WOR', 'EOR', 'WWA', 'EWA', 'CA']:
            print 'All calculations to be done using ' + region + ' equations.\n'
            break
        else:
            print 'Region not recognized. Try again.\n'


# In[9]:

# Prompt user to specify a single report year
all_years = sorted(pd.unique(tree_list['RPT_YR']).tolist())
if not report_yr:
    while True:
        report_yr = raw_input('Choose a year to run (RPT_YR from DBHCLS table), or type ALL: ')
        if report_yr.lower() == 'all':
            report_yr = all_years
            print 'Running all years.\n'
            break
        elif int(report_yr) in all_years:
            report_yr = [int(report_yr)]
            print 'Running calculations for ' + str(report_yr[0]) + ' only.\n'
            break
        else: 
            print report_yr + ' not found in DBHCLS table. Try again using one of these:'
            print ', '.join(str(yr) for yr in all_years) + '\n'


# In[10]:

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


# In[11]:

# hold out RPT_YR years that were not requested by user
tree_list = tree_list.loc[tree_list['RPT_YR'].isin(report_yr)] # only include trees from that year
    
# hold out trees from any properties not requested by user
stands_in_properties_to_run = pd.unique(stand_list['STD_ID'].loc[stand_list['Property'].isin(properties_to_run)]).tolist()
tree_list = tree_list.loc[tree_list['STD_ID'].isin(stands_in_properties_to_run)]
        
# hold out any trees that were not in species crosswalk spreadsheet
if len(missing_spp) >0:
    tree_list = tree_list.loc[~tree_list['SPECIES'].isin(missing_spp)]
    missing_trees = tree_list.loc[tree_list['SPECIES'].isin(missing_spp)]
    
# hold out any trees that are not living, based on a GRP code 
live_trees = ['..', '.R', '.I', '.L', '.W'] # codes for live, residual, ingrowth, leave, and wildlife trees
dead_trees = tree_list.loc[~tree_list['GRP'].isin(live_trees)] # trees with codes other than live_trees
tree_list = tree_list.loc[tree_list['GRP'].isin(live_trees)] # trees only with recognized live_trees codes


# In[12]:

# add new columns to the tree_list for individual trees:

# Region
tree_list['FIA_Region'] = region

# ARB Volume Equation Number & Total Cubic Volume (CVTS, cubic volume including top and stump)
tree_list['Vol_Eq'] = tree_list['SPECIES'].apply(lambda x: getattr(species_classes[x], region+'_VOL').func_name.split('_')[1])

def get_vol(row):
    return calc_vol(row.DBH, row.HEIGHT, 'CVTS', getattr(species_classes[row.SPECIES], region+'_VOL'))
tree_list['CVTS_ft3'] = tree_list.apply(get_vol, axis = 1) # calculate cubic volume for each row

# Wood Density and Stem Biomass, density in units of lbs/ft3 and cubic volume in ft3
tree_list['Wood_density_lbs_ft3'] = tree_list['SPECIES'].apply(lambda x: getattr(species_classes[x], 'wood_dens'))
tree_list['Stem_biomass_UStons'] = (tree_list['CVTS_ft3'] * tree_list['Wood_density_lbs_ft3'])/2000.0
tree_list['Stem_biomass_kg'] = (tree_list['CVTS_ft3'] * tree_list['Wood_density_lbs_ft3'])*0.453592

# Bark biomass equation and calculation
tree_list['BarkBio_Eq'] = tree_list['SPECIES'].apply(lambda x: getattr(species_classes[x], region+'_BB').func_name.split('_')[1])
def get_bark_bio(row): # convert DBH and HT from English to Metric units
    # equations use metric units, so convert DBH and HT from English to Metric units
    # equations return units of kg
    return check_BB(row.DBH*2.54, row.HEIGHT*0.3048, row.Wood_density_lbs_ft3, getattr(species_classes[row.SPECIES], region+'_BB'))
tree_list['Bark_biomass_kg'] = tree_list.apply(get_bark_bio, axis = 1)

# Branch biomass equation and calculation
tree_list['BranchBio_Eq'] = tree_list['SPECIES'].apply(lambda x: getattr(species_classes[x], region+'_BLB').func_name.split('_')[1])
def get_branch_bio(row): 
    # equations use metric units, so convert DBH and HT from English to Metric units
    # equations return units of kg
    return check_BLB(row.DBH*2.54, row.HEIGHT*0.3048, getattr(species_classes[row.SPECIES], region+'_BLB'))
tree_list['Branch_biomass_kg'] = tree_list.apply(get_branch_bio, axis = 1)

# Above-ground biomass
tree_list['Aboveground_biomass_kg'] = tree_list['Stem_biomass_kg'] + tree_list['Bark_biomass_kg'] + tree_list['Branch_biomass_kg']

# Below-ground biomass, calculated using Cairns et al. (1997) Equation #1
tree_list['Belowground_biomass_kg'] = tree_list['Aboveground_biomass_kg'].apply(cairns)

# Total live tree biomass
tree_list['LiveTree_biomass_kg'] = tree_list['Aboveground_biomass_kg'] + tree_list['Belowground_biomass_kg']

# Total live tree carbon
tree_list['LiveTree_carbon_tCO2_tree'] = tree_list['LiveTree_biomass_kg'] / 1000.0 *  44.0/12.0

# Total live tree carbon per acre
tree_list['LiveTree_carbon_tCO2_ac'] = tree_list['LiveTree_carbon_tCO2_tree'] * tree_list['TREES']

# Total carbon across property
# add GIS_Area to tree_list
tree_list = tree_list.merge(stand_list[['STD_ID', 'AREA_GIS', 'Property']], on='STD_ID')
tree_list['LiveTree_carbon_tCO2_total'] = tree_list['LiveTree_carbon_tCO2_ac'] * tree_list['AREA_GIS']


# In[15]:

# add back in unrecognized species and dead_trees
tree_list = tree_list.append([missing_trees, dead_trees], ignore_index=True)


# In[16]:

# sort the tree_list
tree_list = tree_list.sort_values(by = ['Property', 'RPT_YR', 'STD_ID', 'PlotTree'])

# column order to use for CSV output
cols = ['Property', 'RPT_YR', 'STD_ID', 'AREA_GIS', 'PlotTree', 'GRP', 'SPECIES', 'DBH', 'HEIGHT', 
           'TREES', 'FIA_Region', 'Vol_Eq', 'BarkBio_Eq', 'BranchBio_Eq', 'CVTS_ft3', 
           'Wood_density_lbs_ft3', 'Stem_biomass_UStons', 'Stem_biomass_kg', 'Bark_biomass_kg',
           'Branch_biomass_kg', 'Aboveground_biomass_kg', 'Belowground_biomass_kg', 
           'LiveTree_biomass_kg', 'LiveTree_carbon_tCO2_tree', 'LiveTree_carbon_tCO2_ac', 
           'LiveTree_carbon_tCO2_total']

# write a separate CSV for each property in dataframe:
if not os.path.exists('FPS2ARB_Outputs'):
    os.makedirs('FPS2ARB_Outputs')

num_files = 0
for prop in properties_to_run:
    tree_list.loc[tree_list['Property'] == prop].to_csv(os.getcwd() + '/FPS2ARB_Outputs/' + 'FPS2ARB_' + prop + '_' + time.strftime('%Y-%m-%d') + '.csv', columns = cols, index = False)
    num_files += 1

print 'FPS2ARB calculations completed. \n' + str(num_files) + ' CSV file(s) successfully written to ' + os.getcwd() + '\FPS2ARB_Outputs \n'

