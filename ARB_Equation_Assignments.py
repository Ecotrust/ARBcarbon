from ARB_Volume_Equations import *
from ARB_Biomass_Equations import *
import pandas as pd


# The volume equations were translated from the PDF availabe on the ARB website:
# http://www.arb.ca.gov/cc/capandtrade/protocols/usforest/usforestprojects_2015.htm
# Assignments to individual species were drawn from from this page on May 11, 2016, and downloaded as a PDF
# http://www.arb.ca.gov/cc/capandtrade/protocols/usforest/2015/volume.equations.ca.or.wa.pdf


def check_for_None(equation_number):
    eqn = str(equation_number)
    if eqn == '--':
        return None
    elif '.' in eqn:
        return eqn.replace('.','')
    else:
        return eqn


# Create a class that holds the equations and related attributes to be used for each species.
class Species:
    def __init__(self, FIAcode, common_name, wood_type):
        '''
        Instantiates the class to hold various attributes of a tree species.
        '''
        self.code = FIAcode # Numerical species code used by USFS FIA Program
        self.common_name = common_name # Common_name of the species
        self.wood_type = wood_type # Hardwood or Softwood (as "HW" or "SW")

    def add_vols(self, WOR, WWA, EOR, EWA, CA):
        '''
        Adds cubic volume equation assignments for each region to the Species class
        '''
        self.WOR_VOL = eval("Eq_"+str(check_for_None(WOR)))
        self.WWA_VOL = eval("Eq_"+str(check_for_None(WWA)))
        self.EOR_VOL = eval("Eq_"+str(check_for_None(EOR)))
        self.EWA_VOL = eval("Eq_"+str(check_for_None(EWA)))
        self.CA_VOL = eval("Eq_"+str(check_for_None(CA)))

    def add_wood_specs(self, spec_grav, wood_dens):
        '''
        Adds specific gravity and wood density to the Species class
        '''
        self.spec_grav = spec_grav
        self.wood_dens = wood_dens

    def add_bark(self, WOR, WWA, EOR, EWA, CA):
        '''
        Adds bark biomass equation assignments for each region to the Species class
        '''
        self.WOR_BB = eval("BB_"+str(check_for_None(WOR)))
        self.WWA_BB = eval("BB_"+str(check_for_None(WWA)))
        self.EOR_BB = eval("BB_"+str(check_for_None(EOR)))
        self.EWA_BB = eval("BB_"+str(check_for_None(EWA)))
        self.CA_BB = eval("BB_"+str(check_for_None(CA)))

    def add_branch(self, WOR, WWA, EOR, EWA, CA):
        '''
        Adds live branch biomass equation assignments for each region to the Species class
        '''
        self.WOR_BLB = eval("BLB_"+str(check_for_None(WOR)))
        self.WWA_BLB = eval("BLB_"+str(check_for_None(WWA)))
        self.EOR_BLB = eval("BLB_"+str(check_for_None(EOR)))
        self.EWA_BLB = eval("BLB_"+str(check_for_None(EWA)))
        self.CA_BLB = eval("BLB_"+str(check_for_None(CA)))


# read in the species codes provided by the user
# includes the user's code, the FIA code, and the common_name
species_crosswalk = pd.read_excel("Your_species_codes.xlsx", "Crosswalk")
species_used = species_crosswalk.dropna() # ignore species the user didn't provide in the crosswalk table


# read in the tables that describe which equations and wood parameters are required by ARB
with pd.ExcelFile('ARB_Volume_and_Biomass_Tables.xlsx') as xlsx:
    SW_VOL = pd.read_excel(xlsx, 'SW_Volume_equations', index_col= 'FIA_code')
    HW_VOL = pd.read_excel(xlsx, 'HW_Volume_equations', index_col= 'FIA_code')
    VOL = pd.concat([SW_VOL, HW_VOL]) # concatenate all volume equation assignments

    SW_Wood = pd.read_excel(xlsx, 'SW_Wood_specs', index_col= 'FIA_code').drop('Common_name', axis=1)
    HW_Wood = pd.read_excel(xlsx, 'HW_Wood_specs', index_col= 'FIA_code').drop('Common_name', axis=1)
    Wood = pd.concat([SW_Wood, HW_Wood]) # concatenate all wood specifications

    VOL_Wood = pd.merge(VOL, Wood, left_index = True, right_index = True) # merge (outer join) volume equation assignments and wood specs on FIA_code

    SW_BB = pd.read_excel(xlsx, 'SW_Bark_biomass', index_col= 'FIA_code').drop('Common_name', axis=1)
    HW_BB = pd.read_excel(xlsx, 'HW_Bark_biomass', index_col= 'FIA_code').drop('Common_name', axis=1)
    BB = pd.concat([SW_BB, HW_BB]) # concatenate all bark biomass equation assigments

    SW_BLB = pd.read_excel(xlsx, 'SW_LiveBranch_biomass', index_col= 'FIA_code').drop('Common_name', axis=1)
    HW_BLB = pd.read_excel(xlsx, 'HW_LiveBranch_biomass', index_col= 'FIA_code').drop('Common_name', axis=1)
    BLB = pd.concat([SW_BLB, HW_BLB]) # concatenate all live branch biomass equation assignments

    BB_BLB = pd.merge(BB, BLB, left_index = True, right_index = True) # merge (outer join) bark and branch equation assignments on FIA_code

# merge all these into a single dataframe
ARB_species_attributes = pd.merge(VOL_Wood, BB_BLB, left_index = True, right_index = True)


# create a dictionary that will hold all species provide by the user
# the key to the dict is the species code provided by the user, the value is the Species class
species_classes = {}

# iterate through the rows in the user's crosswalk
for index, row in species_used.iterrows():

    # create a class for the species, stored in the dictionary
    species_classes[row.Your_species_code] = Species(row.FIA_code, row.Common_name, row.Wood_type)

    # add the attributes for those species by selecting the appropriate values from the species_attributes dataframe

    # gather the volume equation assignments
    WOR_VOL = ARB_species_attributes.loc[row.FIA_code, 'WOR_VOL']
    WWA_VOL = ARB_species_attributes.loc[row.FIA_code, 'WWA_VOL']
    EOR_VOL = ARB_species_attributes.loc[row.FIA_code, 'EOR_VOL']
    EWA_VOL = ARB_species_attributes.loc[row.FIA_code, 'EWA_VOL']
    CA_VOL = ARB_species_attributes.loc[row.FIA_code, 'CA_VOL']
    species_classes[row.Your_species_code].add_vols(WOR_VOL, WWA_VOL, EOR_VOL, EWA_VOL, CA_VOL) # add them to the class in the dictionary

    # gather the wood_specs
    spec_grav = ARB_species_attributes.loc[row.FIA_code, 'Specific_gravity']
    wood_dens = ARB_species_attributes.loc[row.FIA_code, 'Wood_density']
    species_classes[row.Your_species_code].add_wood_specs(spec_grav, wood_dens) # add them to the class in the dictionary

    # gather the bark equation assignments
    WOR_BB = ARB_species_attributes.loc[row.FIA_code, 'WOR_BB']
    WWA_BB = ARB_species_attributes.loc[row.FIA_code, 'WWA_BB']
    EOR_BB = ARB_species_attributes.loc[row.FIA_code, 'EOR_BB']
    EWA_BB = ARB_species_attributes.loc[row.FIA_code, 'EWA_BB']
    CA_BB = ARB_species_attributes.loc[row.FIA_code, 'CA_BB']
    species_classes[row.Your_species_code].add_bark(WOR_BB, WWA_BB, EOR_BB, EWA_BB, CA_BB) # add them to the class in the dictionary

    # gather the live branch equation assignments
    WOR_BLB = ARB_species_attributes.loc[row.FIA_code, 'WOR_BLB']
    WWA_BLB = ARB_species_attributes.loc[row.FIA_code, 'WWA_BLB']
    EOR_BLB = ARB_species_attributes.loc[row.FIA_code, 'EOR_BLB']
    EWA_BLB = ARB_species_attributes.loc[row.FIA_code, 'EWA_BLB']
    CA_BLB = ARB_species_attributes.loc[row.FIA_code, 'CA_BLB']
    species_classes[row.Your_species_code].add_branch(WOR_BLB, WWA_BLB, EOR_BLB, EWA_BLB, CA_BLB) # add them to the class in the dictionary


def confirm_assignments():
    '''
    Prints all attributes (equations & wood specs) for all species provided by user.
    Reproduces tables like original original ARB versions.
    '''
    def replace_func_with_name(x):
        if callable(x):
            try:
                name = x.func_name.split('_')[1]
            except AttributeError: # volume equations are classes, not functions, don't have func_name attribute
                name = x.__name__.split('_')[1]
            if name == 'None':
                return '--'
            else:
                return name
        else:
            return x

    confirm_eqs = pd.DataFrame(species_classes[spp].__dict__ for spp in pd.unique(species_used.Your_species_code)).applymap(replace_func_with_name)
    print "Volume Equations"
    print confirm_eqs[['code', 'common_name', 'WOR_VOL', 'WWA_VOL', 'EOR_VOL', 'EWA_VOL', 'CA_VOL']].to_string(index=False) + '\n'
    print "Wood specifications"
    print confirm_eqs[['code', 'common_name', 'spec_grav', 'wood_dens']].to_string(index=False) + '\n'
    print "Bark Biomass Equations"
    print confirm_eqs[['code', 'common_name', 'WOR_BB', 'WWA_BB', 'EOR_BB', 'EWA_BB', 'CA_BB']].to_string(index=False) + '\n'
    print "Live Branch Biomass Equations"
    print confirm_eqs[['code', 'common_name', 'WOR_BLB', 'WWA_BLB', 'EOR_BLB', 'EWA_BLB', 'CA_BLB']].to_string(index=False) + '\n'
