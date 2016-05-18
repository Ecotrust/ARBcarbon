
# coding: utf-8

# In[3]:

# Tree equations required by the California Air Resources Board (ARB)
# Used to calculate tree volume for projects located in California, Oregon, or Washington


# In[4]:

# These equations were translated from the PDF available on the ARB website: 
# http://www.arb.ca.gov/cc/capandtrade/protocols/usforest/usforestprojects_2015.htm
# These volume equations were accessed from this page on May 11, 2016, and downloaded as a PDF
# http://www.arb.ca.gov/cc/capandtrade/protocols/usforest/2015/volume.equations.ca.or.wa.pdf


# In[5]:

import math


# In[6]:

# ARB-APPROVED VOLUME EQUATIONS ARE REPRODUCED BELOW AS FUNCTIONS
# Each volume equation is a function that calculates a variety of variables.
# These variables are materialized as a dictionary within the local volume equation/function environment.


# In[7]:

# This helper function is called within individual tree volume equations to return the volume or  
# equation parameter requested by the user.

def get_metric(metric_dict, metric, wood_type):
    """
    takes a dictionary of metric names (key) and values for those metrics from a cubic volume equation
    returns the value of the metric requested, handling both hardwood and softwood trees as well as 
    providing generalized metrics (i.e., selects appropriate cubic volume metric based on merchantability 
    limit/top diameter)
    """
    if metric == 'total_cubic':
        return metric_dict['CVT']
    else:
        try:
            return metric_dict[metric]
        except:
            if wood_type == 'SW':
                return SW_BFConversion(metric_dict['DBH'], metric_dict['CV4'], metric_dict['TARIF'], metric)
            if wood_type == 'HW':
                return HW_BFConversion(metric_dict['CV4'], metric_dict['CV8'], metric_dict['DBH'], metric_dict['eq_number'], 
                                       metric_dict['CVT'], metric_dict['TARIF'], metric_dict['HT'], metric)


# In[8]:

# THE VOLUME EQUATIONS


# In[9]:

# For species where there is no identified volume equation by ARB/CAR
def Eq_None(DBH, HT, metric):
    return 0


# In[10]:

# Equation 1 Douglas-Fir (WEYERHAUSER-DNR RPT#24,1977)

# Brackett, M. 1973. Notes on TARIF tree volume computation. Res. Management Report 24. 
# WA Dept. of Nat. Resources. Olympia. 26p.

# Brackett, Michael.  1977. Notes on TARIF tree-volume computation.  DNR report #24. 
# State of Washington, Department of Natural Resources, Olympia, WA. 132p.   

def Eq_1(DBH, HT, metric):
    """
    WHERE:
    DBH (inches) = DBH (CM) CONVERTED TO INCHES (DBH/2.54)
    HT (feet) = HT (M) CONVERTED TO FEET (HT/0.3048)
    BA = BASAL AREA/ACRE (DBH IN INCHES)    BA = 0.005454154*(DBH**2)
    CVTSL = LOG BASE 10, CUBIC FOOT VOLUME, INCLUDING TOP AND STUMP
    CVTS = CUBIC FOOT VOLUME, INCLUDING TOP AND STUMP
    TARIF = TARIF NUMBER EQUATION (REF. DNR NOTE NO.27, P.2)
    CVT = CUBIC FOOT VOLUME ABOVE STUMP
    CV4 = CUBIC FOOT VOLUME ABOVE STUMP, 4-INCH TOP
    """
    eq_number = 1
    BA = 0.005454154*(DBH**2)
    # note that math.log() uses natural logarithm while math.log10() uses log base 10
    CVTSL = -3.21809 + 0.04948 * math.log10(HT) * math.log10(DBH) - 0.15664 * (math.log10(DBH))**2 + 2.02132 * math.log10(DBH) + 1.63408 * math.log10(HT) - 0.16185 * (math.log10(HT))**2
    CVTS = 10**CVTSL
    TARIF = (CVTS * 0.912733)/((1.033*(1.0 + 1.382937 * math.exp(-4.105292 * (DBH/10.0))))*(BA+0.087266)-0.174533)
    CV4 = TARIF * (BA - 0.087266)/0.912733
    CVT = TARIF * (0.9679 - 0.1051 * 0.5523**(DBH-1.5))*((1.033*(1.0 + 1.382937 * math.exp(-4.015292*(DBH/10.0))))*(BA + 0.087266)-0.174533)/0.912733
    
    # record these values in a dictionary
    metric_dict = {}
    for each_metric in ['CVTSL', 'CVTS', 'TARIF', 'CV4', 'CVT', 'DBH']:
        metric_dict[each_metric] = eval(each_metric)
    
    # if metric requested by user is a cubic volume metric, return it
    return get_metric(metric_dict, metric, 'SW')


# In[11]:

# Equation 2 Douglas-Fir (DNR MEMO--SUMMERFIELD, 11/7/80)

# Summerfield, Edward.  1980. In-house memo describing equations for Douglas-fir and ponderosa pine. 
# State of Washington, Department of Natural Resources. On file with the PNW Research Station.

def Eq_2(DBH, HT, metric):
    """
    WHERE:
    DBH (inches) = DBH (CM) CONVERTED TO INCHES (DBH/2.54)
    HT (feet) = HT (M) CONVERTED TO FEET (HT/0.3048)
    BA = BASAL AREA/ACRE (DBH IN INCHES)    BA = 0.005454154*(DBH**2)
    CVTSL = Natural Log, CUBIC FOOT VOLUME, INCLUDING TOP AND STUMP
    CVTS = CUBIC FOOT VOLUME, INCLUDING TOP AND STUMP
    TARIF = TARIF NUMBER EQUATION (REF. DNR NOTE NO.27, P.2)
    CVT = CUBIC FOOT VOLUME ABOVE STUMP
    CV4 = CUBIC FOOT VOLUME ABOVE STUMP, 4-INCH TOP
    """
    eq_number = 2
    BA = 0.005454154*(DBH**2)
    # note that math.log() uses natural logarithm while math.log10() uses log base 10
    CVTSL = -6.110493 + 1.81306 * math.log(DBH) + 1.083884 * math.log(HT)
    CVTS = math.exp(CVTSL)
    TARIF = (CVTS * 0.912733)/((1.033*(1.0 + 1.382937 * math.exp(-4.105292 * (DBH/10.0))))*(BA+0.087266)-0.174533)
    CV4 = TARIF * (BA - 0.087266)/0.912733
    CVT = TARIF * (0.9679 - 0.1051 * 0.5523**(DBH-1.5))*((1.033*(1.0 + 1.382937 * math.exp(-4.015292*(DBH/10.0))))*(BA + 0.087266)-0.174533)/0.912733
    
    # record these values in a dictionary
    metric_dict = {}
    for each_metric in ['CVTSL', 'CVTS', 'TARIF', 'CV4', 'CVT', 'DBH']:
        metric_dict[each_metric] = eval(each_metric)
    
    # if metric requested by user is a cubic volume metric, return it
    return get_metric(metric_dict, metric, 'SW')


# In[12]:

# Equation 3 Douglas-Fir (USDA-FS RES NOTE PNW-266)

# MacLean, Colin and John M. Berger.  1976.  Softwood tree-volume equations for major California species.  
# PNW Research Note, PNW-266.  Pacific Northwest Forest and Range Experiment Station, Portland Oregon. 34p.

def Eq_3(DBH, HT, metric):
    """
    WHERE:
    DBH (inches) = DBH (CM) CONVERTED TO INCHES (DBH/2.54)
    HT (feet) = HT (M) CONVERTED TO FEET (HT/0.3048)
    CVTS = CUBIC FOOT VOLUME, INCLUDING TOP AND STUMP
    TARIF = TARIF NUMBER EQUATION (REF. DNR NOTE NO.27, P.2)
    CVT = CUBIC FOOT VOLUME ABOVE STUMP
    CV4 = CUBIC FOOT VOLUME ABOVE STUMP, 4-INCH TOP
    """
    eq_number = 3
    
    # FOR THIS SET OF EQUATIONS CREATE A TEMPORARY DBH AND BA for trees less than 6” DBH
    
    #if DBH < 6.0:     # this conditional statement is unnecessary. TMP_DBH and other TMP variables 
    TMP_DBH = 6.0      # are only called in equations below if DBH <6. Assign TMP_DBH regardless.
    
    # CALCULATE BASAL AREA PER TREE USING DBH AND DBH_TEMP
    BA = DBH**2 * 0.005454154
    BA_TMP = TMP_DBH **2 * 0.005454154
    
    # CALCULATE A CUBIC FORM FACTOR (CF4) USING TMP_DBH and DBH
    # CF4 EQUATIONS VARY BY VOLUME EQUATION
    CF4 = 0.248569 + 0.0253524*(HT/DBH) - 0.0000560175*(HT**2/ DBH)
    if(CF4 < 0.3):
        CF4=0.3
    if(CF4 > 0.4): 
        CF4=0.4
    
    CF4_TMP = 0.248569 + 0.0253524*(HT/TMP_DBH) - 0.0000560175*(HT**2/ TMP_DBH)
    if(CF4_TMP < 0.3):
        CF4_TMP=0.3
    if(CF4_TMP > 0.4):
        CF4_TMP=0.4
    
    # ----------------
    # For ease of use and to improve readability of equations, 
    # calculate the following term and use it in the equations that follow. 
    # Note that actual DBH and BA are used for all trees.
    # Do not use TMP_DBH or BA_TMP here.
    
    TERM = ((1.033 * (1.0 + 1.382937 * math.exp(-4.015292 * (DBH/10.0)))) * (BA + 0.087266) - 0.174533 )
    # ----------------
    
    if DBH >= 6.0:
        CV4 = CF4 * BA * HT
        TARIF = (CV4 * 0.912733) / (BA - 0.087266)
        if (TARIF <= 0.0):
            TARIF=0.01
        CVTS = (CV4 * TERM )/ (BA - 0.087266)

        # set floor of CVTS to zero (in case equation generates negative values)
        CVTS = max(0,CVTS)

        CVT = TARIF * (0.9679 - 0.1051 * 0.5523**(DBH-1.5) ) * TERM / 0.912733
    
    elif DBH < 6.0:
        CV4_TMP = CF4_TMP * BA_TMP * HT
        TARIF_TMP = (CV4_TMP * 0.912733) / (BA_TMP - 0.087266)
        if(TARIF_TMP <= 0.0):
            TARIF_TMP = 0.01
        # CALCULATE An ADJUSTED TARIF FOR SMALL TREES (Both DBH and TMP_DBH are used)
        TARIF = TARIF_TMP * ( 0.5 * (TMP_DBH - DBH)**2 + (1.0 + 0.063 * (TMP_DBH - DBH)**2) )
        if(TARIF <= 0.0):
            TARIF = 0.01
        CVTS = TARIF * TERM

        # set floor of CVTS to zero (in case equation generates negative values)
        CVTS = max(0,CVTS)

        CVT = TARIF * (0.9679 - 0.1051 * 0.5523**(DBH-1.5) ) * TERM / 0.912733
        CV4 = CF4 * BA * HT #(calculated with actual DBH and BA)
        
    if DBH < 5.0:
        CV4 = 0
    #elif DBH >= 5.0:
    #    pass # THEN KEEP CV4
    
    # record these values in a dictionary
    metric_dict = {}
    for each_metric in ['CVTS', 'TARIF', 'CV4', 'CVT', 'DBH']:
        metric_dict[each_metric] = eval(each_metric)
    
    # if metric requested by user is a cubic volume metric, return it
    return get_metric(metric_dict, metric, 'SW')


# In[13]:

# Equation 4 Ponderosa pine (DNR MEMO--SUMMERFIELD,11/7/80)

# Summerfield, Edward.  1980. In-house memo describing equations for Douglas-fir and ponderosa pine. 
# State of Washington, Department of Natural Resources. On file with the PNW Research Station.

def Eq_4(DBH, HT, metric):
    """
    WHERE:
    DBH (inches) = DBH (CM) CONVERTED TO INCHES (DBH/2.54)
    HT (feet) = HT (M) CONVERTED TO FEET (HT/0.3048)
    BA = BASAL AREA (DBH IN INCHES) BA= .005454154 x DBH2
    CVTSL = LOG BASE e, CUBIC FOOT VOLUME, INCLUDING TOP AND STUMP
        # original documentation states CVTSL is log base 10
    CVTS = CUBIC FOOT VOLUME, INCLUDING TOP AND STUMP
    TARIF = TARIF NUMBER EQUATION (REF. DNR NOTE NO.27, P.2)
    CVT = CUBIC FOOT VOLUME ABOVE STUMP
    CV4 = CUBIC FOOT VOLUME ABOVE STUMP, 4-INCH TOP
    """
    eq_number = 4
    BA = 0.005454154 * DBH**2
    # note that math.log() uses natural logarithm while math.log10() uses log base 10
    CVTSL = -8.521558 + 1.977243 * math.log(DBH) - 0.105288 * (math.log(HT))**2 + 136.0489/HT**2 + 1.99546 * math.log(HT)
    CVTS = math.exp(CVTSL)
    TARIF = (CVTS * 0.912733)/((1.033 * (1.0 + 1.382937 * math.exp(-4.015292 * DBH))) * (BA + 0.087266) - 0.174533)
    CV4 = TARIF * (BA - 0.087266)/0.912733
    CVT = TARIF * (0.9679 - 0.1051 * 0.5523**(DBH-1.5))*((1.033*(1.0 + 1.382937 * math.exp(-4.015292*(DBH/10.0))))*(BA + 0.087266)-0.174533)/0.912733
    
    # record these values in a dictionary
    metric_dict = {}
    for each_metric in ['CVTS', 'TARIF', 'CV4', 'CVT', 'DBH']:
        metric_dict[each_metric] = eval(each_metric)
    
    # if metric requested by user is a cubic volume metric, return it
    return get_metric(metric_dict, metric, 'SW')


# In[14]:

# Equation 5 Ponderosa pine (USDA-FS RES NOTE PNW-266)

# MacLean, Colin and John M. Berger.  1976.  Softwood tree-volume equations for major California species.  
# PNW Research Note, PNW-266.  Pacific Northwest Forest and Range Experiment Station, Portland Oregon. 34p.

def Eq_5(DBH, HT, metric):
    """
    WHERE:
    DBH (inches) = DBH (CM) CONVERTED TO INCHES (DBH/2.54)
    HT (feet) = HT (M) CONVERTED TO FEET (HT/0.3048)
    CVTS = CUBIC FOOT VOLUME, INCLUDING TOP AND STUMP
    TARIF = TARIF NUMBER EQUATION (REF. DNR NOTE NO.27, P.2)
    CVT = CUBIC FOOT VOLUME ABOVE STUMP
    CV4 = CUBIC FOOT VOLUME ABOVE STUMP, 4-INCH TOP
    """
    eq_number = 5
    
    # FOR THIS SET OF EQUATIONS CREATE A TEMPORARY DBH AND BA for trees less than 6” DBH
    
    #if DBH < 6.0:     # this conditional statement is unnecessary. TMP_DBH and other TMP variables 
    TMP_DBH = 6.0      # are only called in equations below if DBH <6. Assign TMP_DBH regardless.
    
    # CALCULATE BASAL AREA PER TREE USING DBH AND DBH_TEMP
    BA = DBH**2 * 0.005454154
    BA_TMP = TMP_DBH **2 * 0.005454154
    
    # CALCULATE A CUBIC FORM FACTOR (CF4) USING TMP_DBH and DBH
    # CF4 EQUATIONS VARY BY VOLUME EQUATION
    CF4 = 0.402060 - 0.899914 * (1/DBH)
    if(CF4 < 0.3):
        CF4=0.3
    if(CF4 > 0.4): 
        CF4=0.4
    CF4_TMP = 0.402060 - 0.899914 * (1/TMP_DBH)
    if (CF4_TMP < 0.3):
        CF4_TMP=0.3
    if (CF4_TMP > 0.4):
        CF4_TMP=0.4

    # ----------------
    # For ease of use and to improve readability of equations, 
    # calculate the following term and use it in the equations that follow. 
    # Note that actual DBH and BA are used for all trees.
    # Do not use TMP_DBH or BA_TMP here.
    
    TERM = ((1.033 * (1.0 + 1.382937 * math.exp(-4.015292 * (DBH/10.0)))) * (BA + 0.087266) - 0.174533 )
    # ----------------
    
    if DBH >= 6.0:
        CV4 = CF4 * BA * HT
        TARIF = (CV4 * 0.912733) / (BA - 0.087266)
        if (TARIF <= 0.0):
            TARIF=0.01
        CVTS = (CV4 * TERM )/ (BA - 0.087266)
        
        # set floor of CVTS to zero (in case equation generates negative values)
        CVTS = max(0,CVTS)

        CVT = TARIF * (0.9679 - 0.1051 * 0.5523**(DBH-1.5) ) * TERM / 0.912733
        
    elif DBH < 6.0:
        CV4_TMP = CF4_TMP *BA_TMP * HT
        TARIF_TMP = (CV4_TMP * 0.912733) / (BA_TMP - 0.087266)
        if(TARIF_TMP <= 0.0):
            TARIF_TMP = 0.01
        # CALCULATE An ADJUSTED TARIF FOR SMALL TREES (Both DBH and TMP_DBH are used)
        TARIF = TARIF_TMP * ( 0.5 * (TMP_DBH - DBH)**2 + (1.0 + 0.063 * (TMP_DBH - DBH)**2) )
        if(TARIF <= 0.0):
            TARIF = 0.01
        CVTS = TARIF * TERM
        
        # set floor of CVTS to zero (in case equation generates negative values)
        CVTS = max(0,CVTS)

        CVT = TARIF * (0.9679 - 0.1051 * 0.5523**(DBH-1.5) ) * TERM / 0.912733
        CV4 = CF4 * BA * HT #(calculated with actual DBH and BA)
        
    if DBH < 5.0:
        CV4 = 0
    #elif DBH >= 5.0:
    #    pass # THEN KEEP CV4
    
    # record these values in a dictionary
    metric_dict = {}
    for each_metric in ['CVTS', 'TARIF', 'CV4', 'CVT', 'DBH']:
        metric_dict[each_metric] = eval(each_metric)
    
    # if metric requested by user is a cubic volume metric, return it
    return get_metric(metric_dict, metric, 'SW')


# In[15]:

# Equation 6 Western hemlock (DNR NOTE 27,4/79)

# Chambers, C.J. and Foltz, B. 1979. The TARIF system -- revisions and additions., 
# Resource Management Report #27. WA Dept. of Nat. Resources. Olympia.

def Eq_6(DBH, HT, metric):
    """
    WHERE:
    DBH (inches) = DBH (CM) CONVERTED TO INCHES (DBH/2.54)
    HT (feet) = HT (M) CONVERTED TO FEET (HT/0.3048)
    BA = BASAL AREA (DBH IN INCHES) BA= .005454154 x DBH2
    CVTSL = LOG BASE 10, CUBIC FOOT VOLUME, INCLUDING TOP AND STUMP
    CVTS = CUBIC FOOT VOLUME, INCLUDING TOP AND STUMP
    TARIF = TARIF NUMBER EQUATION (REF. DNR NOTE NO.27, P.2)
    CVT = CUBIC FOOT VOLUME ABOVE STUMP
    CV4 = CUBIC FOOT VOLUME ABOVE STUMP, 4-INCH TOP
    """
    eq_number = 6
    BA = 0.005454154 * DBH**2
    # note that math.log() uses natural logarithm while math.log10() uses log base 10
    CVTSL = -2.72170 + 2.00857 * math.log10(DBH) + 1.08620 * math.log10(HT) - 0.00568 * DBH
    CVTS = 10**CVTSL
    TARIF = (CVTS * 0.912733)/((1.033 * (1.0 + 1.382937 * math.exp(-4.015292 * DBH))) * (BA + 0.087266) - 0.174533)
    CV4 = TARIF * (BA - 0.087266)/0.912733
    CVT = TARIF * (0.9679 - 0.1051 * 0.5523**(DBH-1.5))*((1.033*(1.0 + 1.382937 * math.exp(-4.015292*(DBH/10.0))))*(BA + 0.087266)-0.174533)/0.912733
    
    # record these values in a dictionary
    metric_dict = {}
    for each_metric in ['CVTS', 'TARIF', 'CV4', 'CVT', 'DBH']:
        metric_dict[each_metric] = eval(each_metric)
    
    # if metric requested by user is a cubic volume metric, return it
    return get_metric(metric_dict, metric, 'SW')


# In[16]:

# Equation 7 Western hemlock (BROWN (1962) BC FOREST SERV,P33)

# Browne, J.E. 1962. Standard cubic-foot volume tables for the commercial tree species 
# of British Columbia. B.C. Forest Service, Victoria. 107 p.

def Eq_7(DBH, HT, metric):
    """
    WHERE:
    DBH (inches) = DBH (CM) CONVERTED TO INCHES (DBH/2.54)
    HT (feet) = HT (M) CONVERTED TO FEET (HT/0.3048)
    BA = BASAL AREA (DBH IN INCHES) BA= .005454154 x DBH2
    CVTSL = LOG BASE 10, CUBIC FOOT VOLUME, INCLUDING TOP AND STUMP
    CVTS = CUBIC FOOT VOLUME, INCLUDING TOP AND STUMP
    TARIF = TARIF NUMBER EQUATION (REF. DNR NOTE NO.27, P.2)
    CVT = CUBIC FOOT VOLUME ABOVE STUMP
    CV4 = CUBIC FOOT VOLUME ABOVE STUMP, 4-INCH TOP
    """
    eq_number = 7
    BA = 0.005454154 * DBH**2
    # note that math.log() uses natural logarithm while math.log10() uses log base 10
    CVTSL = -2.663834 + 1.79023 * math.log10(DBH) + 1.124873 * math.log10(HT)
    CVTS = 10**CVTSL
    TARIF = (CVTS * 0.912733)/((1.033 * (1.0 + 1.382937 * math.exp(-4.015292 * DBH))) * (BA + 0.087266) - 0.174533)
    CV4 = TARIF * (BA - 0.087266)/0.912733
    CVT = TARIF * (0.9679 - 0.1051 * 0.5523**(DBH-1.5))*((1.033*(1.0 + 1.382937 * math.exp(-4.015292*(DBH/10.0))))*(BA + 0.087266)-0.174533)/0.912733
    
    # record these values in a dictionary
    metric_dict = {}
    for each_metric in ['CVTS', 'TARIF', 'CV4', 'CVT', 'DBH']:
        metric_dict[each_metric] = eval(each_metric)
    
    # if metric requested by user is a cubic volume metric, return it
    return get_metric(metric_dict, metric, 'SW')


# In[17]:

# Equation 8 Redcedar (REDCEDAR INTERIOR--DNR RPT#24,1977)

# Brackett, M. 1973. Notes on TARIF tree volume computation. Res. Management Report 24. 
# WA Dept. of Nat. Resources. Olympia. 26p.

# Brackett, Michael.  1977. Notes on TARIF tree-volume computation.  DNR report #24. 
# State of Washington, Department of Natural Resources, Olympia, WA. 132p.   

def Eq_8(DBH, HT, metric):
    """
    WHERE:
    DBH (inches) = DBH (CM) CONVERTED TO INCHES (DBH/2.54)
    HT (feet) = HT (M) CONVERTED TO FEET (HT/0.3048)
    BA = BASAL AREA (DBH IN INCHES) BA= .005454154 x DBH2
    CVTSL = LOG BASE 10, CUBIC FOOT VOLUME, INCLUDING TOP AND STUMP
    CVTS = CUBIC FOOT VOLUME, INCLUDING TOP AND STUMP
    TARIF = TARIF NUMBER EQUATION (REF. DNR NOTE NO.27, P.2)
    CVT = CUBIC FOOT VOLUME ABOVE STUMP
    CV4 = CUBIC FOOT VOLUME ABOVE STUMP, 4-INCH TOP
    """
    eq_number = 8
    BA = 0.005454154 * DBH**2
    # note that math.log() uses natural logarithm while math.log10() uses log base 10
    CVTSL = -2.464614 + 1.701993 * math.log10(DBH) + 1.067038 * math.log10(HT)
    CVTS = 10**CVTSL
    TARIF = (CVTS * 0.912733)/((1.033 * (1.0 + 1.382937 * math.exp(-4.015292 * DBH))) * (BA + 0.087266) - 0.174533)
    CV4 = TARIF * (BA - 0.087266)/0.912733
    CVT = TARIF * (0.9679 - 0.1051 * 0.5523**(DBH-1.5))*((1.033*(1.0 + 1.382937 * math.exp(-4.015292*(DBH/10.0))))*(BA + 0.087266)-0.174533)/0.912733
    
    # record these values in a dictionary
    metric_dict = {}
    for each_metric in ['CVTS', 'TARIF', 'CV4', 'CVT', 'DBH']:
        metric_dict[each_metric] = eval(each_metric)
    
    # if metric requested by user is a cubic volume metric, return it
    return get_metric(metric_dict, metric, 'SW')


# In[18]:

# Equation 9 Redcedar (REDCEDAR COAST--DNR RPT#24,1977)

# Brackett, M. 1973. Notes on TARIF tree volume computation. Res. Management Report 24. 
# WA Dept. of Nat. Resources. Olympia. 26p.

# Brackett, Michael.  1977. Notes on TARIF tree-volume computation.  DNR report #24. 
# State of Washington, Department of Natural Resources, Olympia, WA. 132p.   

def Eq_9(DBH, HT, metric):
    """
    WHERE:
    DBH (inches) = DBH (CM) CONVERTED TO INCHES (DBH/2.54)
    HT (feet) = HT (M) CONVERTED TO FEET (HT/0.3048)
    BA = BASAL AREA (DBH IN INCHES) BA= .005454154 x DBH2
    CVTSL = LOG BASE 10, CUBIC FOOT VOLUME, INCLUDING TOP AND STUMP
    CVTS = CUBIC FOOT VOLUME, INCLUDING TOP AND STUMP
    TARIF = TARIF NUMBER EQUATION (REF. DNR NOTE NO.27, P.2)
    CVT = CUBIC FOOT VOLUME ABOVE STUMP
    CV4 = CUBIC FOOT VOLUME ABOVE STUMP, 4-INCH TOP
    """
    eq_number = 9
    BA = 0.005454154 * DBH**2
    # note that math.log() uses natural logarithm while math.log10() uses log base 10
    CVTSL = -2.379642 + 1.682300 * math.log10(DBH) + 1.039712 * math.log10(HT)
    CVTS = 10**CVTSL
    TARIF = (CVTS * 0.912733)/((1.033 * (1.0 + 1.382937 * math.exp(-4.015292 * DBH))) * (BA + 0.087266) - 0.174533)
    CV4 = TARIF * (BA - 0.087266)/0.912733
    CVT = TARIF * (0.9679 - 0.1051 * 0.5523**(DBH-1.5))*((1.033*(1.0 + 1.382937 * math.exp(-4.015292*(DBH/10.0))))*(BA + 0.087266)-0.174533)/0.912733
    
    # record these values in a dictionary
    metric_dict = {}
    for each_metric in ['CVTS', 'TARIF', 'CV4', 'CVT', 'DBH']:
        metric_dict[each_metric] = eval(each_metric)
    
    # if metric requested by user is a cubic volume metric, return it
    return get_metric(metric_dict, metric, 'SW')


# In[19]:

# Equation 10 True Firs (INTERIOR BALSAM--DNR RPT#24,1977)

# Brackett, M. 1973. Notes on TARIF tree volume computation. Res. Management Report 24. 
# WA Dept. of Nat. Resources. Olympia. 26p.

# Brackett, Michael.  1977. Notes on TARIF tree-volume computation.  DNR report #24. 
# State of Washington, Department of Natural Resources, Olympia, WA. 132p.   

def Eq_10(DBH, HT, metric):
    """
    WHERE:
    DBH (inches) = DBH (CM) CONVERTED TO INCHES (DBH/2.54)
    HT (feet) = HT (M) CONVERTED TO FEET (HT/0.3048)
    BA = BASAL AREA (DBH IN INCHES) BA= .005454154 x DBH2
    CVTSL = LOG BASE 10, CUBIC FOOT VOLUME, INCLUDING TOP AND STUMP
    CVTS = CUBIC FOOT VOLUME, INCLUDING TOP AND STUMP
    TARIF = TARIF NUMBER EQUATION (REF. DNR NOTE NO.27, P.2)
    CVT = CUBIC FOOT VOLUME ABOVE STUMP
    CV4 = CUBIC FOOT VOLUME ABOVE STUMP, 4-INCH TOP
    """
    eq_number = 10
    BA = 0.005454154 * DBH**2
    # note that math.log() uses natural logarithm while math.log10() uses log base 10
    CVTSL = -2.502332 + 1.864963 * math.log10(DBH) + 1.004903 * math.log10(HT)
    CVTS = 10**CVTSL
    TARIF = (CVTS * 0.912733)/((1.033 * (1.0 + 1.382937 * math.exp(-4.015292 * DBH))) * (BA + 0.087266) - 0.174533)
    CV4 = TARIF * (BA - 0.087266)/0.912733
    CVT = TARIF * (0.9679 - 0.1051 * 0.5523**(DBH-1.5))*((1.033*(1.0 + 1.382937 * math.exp(-4.015292*(DBH/10.0))))*(BA + 0.087266)-0.174533)/0.912733
    
    # record these values in a dictionary
    metric_dict = {}
    for each_metric in ['CVTS', 'TARIF', 'CV4', 'CVT', 'DBH']:
        metric_dict[each_metric] = eval(each_metric)
    
    # if metric requested by user is a cubic volume metric, return it
    return get_metric(metric_dict, metric, 'SW')


# In[20]:

# Equation 11 True Firs (COAST BALSAM--DNR RPT#24,1977)

# Brackett, M. 1973. Notes on TARIF tree volume computation. Res. Management Report 24. 
# WA Dept. of Nat. Resources. Olympia. 26p.

# Brackett, Michael.  1977. Notes on TARIF tree-volume computation.  DNR report #24. 
# State of Washington, Department of Natural Resources, Olympia, WA. 132p.   

def Eq_11(DBH, HT, metric):
    """
    WHERE:
    DBH (inches) = DBH (CM) CONVERTED TO INCHES (DBH/2.54)
    HT (feet) = HT (M) CONVERTED TO FEET (HT/0.3048)
    BA = BASAL AREA (DBH IN INCHES) BA= .005454154 x DBH2
    CVTSL = LOG BASE 10, CUBIC FOOT VOLUME, INCLUDING TOP AND STUMP
    CVTS = CUBIC FOOT VOLUME, INCLUDING TOP AND STUMP
    TARIF = TARIF NUMBER EQUATION (REF. DNR NOTE NO.27, P.2)
    CVT = CUBIC FOOT VOLUME ABOVE STUMP
    CV4 = CUBIC FOOT VOLUME ABOVE STUMP, 4-INCH TOP
    """
    eq_number = 11
    BA = 0.005454154 * DBH**2
    # note that math.log() uses natural logarithm while math.log10() uses log base 10
    CVTSL = -2.575642 + 1.806775 * math.log10(DBH) + 1.094665 * math.log10(HT)
    CVTS = 10**CVTSL
    TARIF = (CVTS * 0.912733)/((1.033 * (1.0 + 1.382937 * math.exp(-4.015292 * DBH))) * (BA + 0.087266) - 0.174533)
    CV4 = TARIF * (BA - 0.087266)/0.912733
    CVT = TARIF * (0.9679 - 0.1051 * 0.5523**(DBH-1.5))*((1.033*(1.0 + 1.382937 * math.exp(-4.015292*(DBH/10.0))))*(BA + 0.087266)-0.174533)/0.912733
    
    # record these values in a dictionary
    metric_dict = {}
    for each_metric in ['CVTS', 'TARIF', 'CV4', 'CVT', 'DBH']:
        metric_dict[each_metric] = eval(each_metric)
    
    # if metric requested by user is a cubic volume metric, return it
    return get_metric(metric_dict, metric, 'SW')


# In[21]:

# Equation 12 Spruce (SITKA SPRUCE INTERIOR--DNR RPT#24,1977)

# Brackett, M. 1973. Notes on TARIF tree volume computation. Res. Management Report 24. 
# WA Dept. of Nat. Resources. Olympia. 26p.

# Brackett, Michael.  1977. Notes on TARIF tree-volume computation.  DNR report #24. 
# State of Washington, Department of Natural Resources, Olympia, WA. 132p.   

def Eq_12(DBH, HT, metric):
    """
    WHERE:
    DBH (inches) = DBH (CM) CONVERTED TO INCHES (DBH/2.54)
    HT (feet) = HT (M) CONVERTED TO FEET (HT/0.3048)
    BA = BASAL AREA (DBH IN INCHES) BA= .005454154 x DBH2
    CVTSL = LOG BASE 10, CUBIC FOOT VOLUME, INCLUDING TOP AND STUMP
    CVTS = CUBIC FOOT VOLUME, INCLUDING TOP AND STUMP
    TARIF = TARIF NUMBER EQUATION (REF. DNR NOTE NO.27, P.2)
    CVT = CUBIC FOOT VOLUME ABOVE STUMP
    CV4 = CUBIC FOOT VOLUME ABOVE STUMP, 4-INCH TOP
    """
    eq_number = 12
    BA = 0.005454154 * DBH**2
    # note that math.log() uses natural logarithm while math.log10() uses log base 10
    CVTSL = -2.539944 + 1.841226 * math.log10(DBH) + 1.034051 * math.log10(HT)
    CVTS = 10**CVTSL
    TARIF = (CVTS * 0.912733)/((1.033 * (1.0 + 1.382937 * math.exp(-4.015292 * DBH))) * (BA + 0.087266) - 0.174533)
    CV4 = TARIF * (BA - 0.087266)/0.912733
    CVT = TARIF * (0.9679 - 0.1051 * 0.5523**(DBH-1.5))*((1.033*(1.0 + 1.382937 * math.exp(-4.015292*(DBH/10.0))))*(BA + 0.087266)-0.174533)/0.912733
    
    # record these values in a dictionary
    metric_dict = {}
    for each_metric in ['CVTS', 'TARIF', 'CV4', 'CVT', 'DBH']:
        metric_dict[each_metric] = eval(each_metric)
    
    # if metric requested by user is a cubic volume metric, return it
    return get_metric(metric_dict, metric, 'SW')


# In[22]:

# EQUATION 13 SPRUCE (SITKA SPRUCE MATURE--DNR RPT#24,1977)

# Brackett, M. 1973. Notes on TARIF tree volume computation. Res. Management Report 24. 
# WA Dept. of Nat. Resources. Olympia. 26p.

# Brackett, Michael.  1977. Notes on TARIF tree-volume computation.  DNR report #24. 
# State of Washington, Department of Natural Resources, Olympia, WA. 132p.   

def Eq_13(DBH, HT, metric):
    """
    WHERE:
    DBH (inches) = DBH (CM) CONVERTED TO INCHES (DBH/2.54)
    HT (feet) = HT (M) CONVERTED TO FEET (HT/0.3048)
    BA = BASAL AREA (DBH IN INCHES) BA= .005454154 x DBH2
    CVTSL = LOG BASE 10, CUBIC FOOT VOLUME, INCLUDING TOP AND STUMP
    CVTS = CUBIC FOOT VOLUME, INCLUDING TOP AND STUMP
    TARIF = TARIF NUMBER EQUATION (REF. DNR NOTE NO.27, P.2)
    CVT = CUBIC FOOT VOLUME ABOVE STUMP
    CV4 = CUBIC FOOT VOLUME ABOVE STUMP, 4-INCH TOP
    """
    eq_number = 13
    BA = 0.005454154 * DBH**2
    # note that math.log() uses natural logarithm while math.log10() uses log base 10
    CVTSL = -2.700574 + 1.754171 * math.log10(DBH) + 1.164531 * math.log10(HT)
    CVTS = 10**CVTSL    
    TARIF = (CVTS * 0.912733)/((1.033 * (1.0 + 1.382937 * math.exp(-4.015292 * DBH))) * (BA + 0.087266) - 0.174533)
    CV4 = TARIF * (BA - 0.087266)/0.912733
    CVT = TARIF * (0.9679 - 0.1051 * 0.5523**(DBH-1.5))*((1.033*(1.0 + 1.382937 * math.exp(-4.015292*(DBH/10.0))))*(BA + 0.087266)-0.174533)/0.912733
    
    # record these values in a dictionary
    metric_dict = {}
    for each_metric in ['CVTS', 'TARIF', 'CV4', 'CVT', 'DBH']:
        metric_dict[each_metric] = eval(each_metric)
    
    # if metric requested by user is a cubic volume metric, return it
    return get_metric(metric_dict, metric, 'SW')


# In[23]:

# EQUATION 14 - OTHER JUNIPERS (CHOJNACKY, 1985)

# Chojnacky D.C., 1985.  Pinyon-Juniper Volume Equations for the Central Rocky Mountain States.
# Res. Note INT-339, USDA, Forest Service, Intermountain Res. Station, Ogden, UT 84401.

def Eq_14(DRC, HT, STEMS, metric):
    """
    WHERE
    CVTS = cubic foot volume from ground level to a 1.5-inch minimum branch diameter (includes live wood, dead wood, and bark)
    STEMS = number of stems 3 inches and larger within the first foot above DRC. When STEMS=1 it is a single stemmed tree
    DRC (inches) = Diameter at the root collar
    HT (feet) =  Total height of the tree 
    """
    eq_number = 14
    if DRC >= 3 and HT >0:
        Factor = DRC * DRC * HT
    else:
        Factor = 0
    
    if STEMS == 1:
        S = 1
    elif STEMS >1:
        S = 0
        
    CVTS = (-0.13386 + (0.133726 * (Factor**(1/3))) + (0.036329 * S))**3
    if CVTS <= 0:
        CVTS = 0.1
        
    # THERE IS NO BOARDFOOT VOLUME EQUATION
    
    # record these values in a dictionary
    metric_dict = {}
    for each_metric in ['CVTS', 'DRC', 'STEMS']:
        metric_dict[each_metric] = eval(each_metric)
    
    # if metric requested by user is a cubic volume metric, return it
    if metric == 'total_cubic':
        return CVTS
    else:
        try:
            return get_metric(metric_dict, metric, 'SW')
        # otherwise try to return a boardfoot volume metric
        except:
            return 0 # no boardfoot volume according to CAR/ARB documentation


# In[24]:

# EQUATION 14.1 - SINGLELEAF PINYON (CHOJNACKY, 1985)

# Chojnacky D.C., 1985.  Pinyon-Juniper Volume Equations for the Central Rocky Mountain States.
# Res. Note INT-339, USDA, Forest Service, Intermountain Res. Station, Ogden, UT 84401.

def Eq_141(DRC, HT, STEMS, metric):
    """
    WHERE
    CVTS = cubic foot volume from ground level to a 1.5-inch minimum branch diameter (includes live wood, dead wood, and bark)
    DRC (inches) = Diameter at the root collar
    HT (feet) =  Total height of the tree 
    """
    eq_number = 14.1
    if DRC >= 3 and HT >0:
        Factor = DRC * DRC * HT
    else:
        Factor = 0
    
    if STEMS == 1:
        S = 1
    elif STEMS >1:
        S = 0
        
    CVTS = (-0.14240 + (0.148190 * (Factor**(1/3))) - (0.16712 * S))**3
    if CVTS <= 0:
        CVTS = 0.1
        
    # THERE IS NO BOARDFOOT VOLUME EQUATION
        
    # record these values in a dictionary
    metric_dict = {}
    for each_metric in ['CVTS', 'DRC', 'STEMS']:
        metric_dict[each_metric] = eval(each_metric)
    
    # if metric requested by user is a cubic volume metric, return it
    if metric == 'total_cubic':
        return CVTS
    else:
        try:
            return get_metric(metric_dict, metric, 'SW')
        # otherwise try to return a boardfoot volume metric
        except:
            return 0 # no boardfoot volume according to CAR/ARB documentation


# In[25]:

# EQUATION 14.2 - ROCKY MOUNTAIN JUNIPER (CHOJNACKY, 1985)

# Chojnacky D.C., 1985.  Pinyon-Juniper Volume Equations for the Central Rocky Mountain States.
# Res. Note INT-339, USDA, Forest Service, Intermountain Res. Station, Ogden, UT 84401.

def Eq_142(DRC, HT, metric):
    """
    WHERE
    CVTS = cubic foot volume from ground level to a 1.5-inch minimum branch diameter (includes live wood, dead wood, and bark)
    STEMS = number of stems 3 inches and larger within the first foot above DRC. When STEMS=1 it is a single stemmed tree
    DRC (inches) = Diameter at the root collar
    HT (feet) =  Total height of the tree 
    """
    eq_number = 14.2
    if DRC >= 3 and HT >0:
        Factor = DRC * DRC * HT
    else:
        Factor = 0
        
    CVTS = (0.02434 + (0.119106 * (Factor**(1/3))))**3
    if CVTS <= 0:
        CVTS = 0.1
    
    # THERE IS NO BOARDFOOT VOLUME EQUATION
    
    # record these values in a dictionary
    metric_dict = {}
    for each_metric in ['CVTS', 'DRC']:
        metric_dict[each_metric] = eval(each_metric)
    
    # if metric requested by user is a cubic volume metric, return it
    if metric == 'total_cubic':
        return CVTS
    else:
        try:
            return get_metric(metric_dict, metric, 'SW')
        # otherwise try to return a boardfoot volume metric
        except:
            return 0 # no boardfoot volume according to CAR/ARB documentation


# In[26]:

# EQUATION 15 LODGEPOLE PINE (LODGEPOLE PINE--DNR RPT#24,1977)

# Brackett, M. 1973. Notes on TARIF tree volume computation. Res. Management Report 24. 
# WA Dept. of Nat. Resources. Olympia. 26p.

# Brackett, Michael.  1977. Notes on TARIF tree-volume computation.  DNR report #24. 
# State of Washington, Department of Natural Resources, Olympia, WA. 132p.   

def Eq_15(DBH, HT, metric):
    """
    WHERE:
    DBH (inches) = DBH (CM) CONVERTED TO INCHES (DBH/2.54)
    HT (feet) = HT (M) CONVERTED TO FEET (HT/0.3048)
    BA = BASAL AREA (DBH IN INCHES) BA= .005454154 x DBH2
    CVTSL = LOG BASE 10, CUBIC FOOT VOLUME, INCLUDING TOP AND STUMP
    CVTS = CUBIC FOOT VOLUME, INCLUDING TOP AND STUMP
    TARIF = TARIF NUMBER EQUATION (REF. DNR NOTE NO.27, P.2)
    CVT = CUBIC FOOT VOLUME ABOVE STUMP
    CV4 = CUBIC FOOT VOLUME ABOVE STUMP, 4-INCH TOP
    """
    eq_number = 15
    BA = 0.005454154 * DBH**2
    # note that math.log() uses natural logarithm while math.log10() uses log base 10
    CVTSL = -2.615591 + 1.847504 * math.log10(DBH) + 1.085772 * math.log10(HT)
    CVTS = 10**CVTSL
    TARIF = (CVTS * 0.912733)/((1.033 * (1.0 + 1.382937 * math.exp(-4.015292 * DBH))) * (BA + 0.087266) - 0.174533)
    CV4 = TARIF * (BA - 0.087266)/0.912733
    CVT = TARIF * (0.9679 - 0.1051 * 0.5523**(DBH-1.5))*((1.033*(1.0 + 1.382937 * math.exp(-4.015292*(DBH/10.0))))*(BA + 0.087266)-0.174533)/0.912733
    
    # record these values in a dictionary
    metric_dict = {}
    for each_metric in ['CVTS', 'TARIF', 'CV4', 'CVT', 'DBH']:
        metric_dict[each_metric] = eval(each_metric)
    
    # if metric requested by user is a cubic volume metric, return it
    return get_metric(metric_dict, metric, 'SW')


# In[27]:

# EQUATION 16 LODGEPOLE PINE (USDA-FS RES NOTE PNW-266)

# MacLean, Colin and John M. Berger.  1976.  Softwood tree-volume equations for major California species.  
# PNW Research Note, PNW-266.  Pacific Northwest Forest and Range Experiment Station, Portland Oregon. 34p.

def Eq_16(DBH, HT, metric):
    """
    WHERE:
    DBH (inches) = DBH (CM) CONVERTED TO INCHES (DBH/2.54)
    HT (feet) = HT (M) CONVERTED TO FEET (HT/0.3048)
    CVTS = CUBIC FOOT VOLUME, INCLUDING TOP AND STUMP
    TARIF = TARIF NUMBER EQUATION (REF. DNR NOTE NO.27, P.2)
    CVT = CUBIC FOOT VOLUME ABOVE STUMP
    CV4 = CUBIC FOOT VOLUME ABOVE STUMP, 4-INCH TOP
    """
    eq_number = 16
    
    # FOR THIS SET OF EQUATIONS CREATE A TEMPORARY DBH AND BA for trees less than 6” DBH
    
    #if DBH < 6.0:     # this conditional statement is unnecessary. TMP_DBH and other TMP variables 
    TMP_DBH = 6.0      # are only called in equations below if DBH <6. Assign TMP_DBH regardless.
    
    # CALCULATE BASAL AREA PER TREE USING DBH AND DBH_TEMP
    BA = DBH**2 * 0.005454154
    BA_TMP = TMP_DBH **2 * 0.005454154

    # CALCULATE A CUBIC FORM FACTOR (CF4) USING TMP_DBH and DBH
    # CF4 EQUATIONS VARY BY VOLUME EQUATION
    CF4 = 0.422709 - 0.0000612236 * (HT**2/DBH)
    if(CF4 < 0.3):
        CF4=0.3
    if(CF4 > 0.4): 
        CF4=0.4
    CF4_TMP = 0.422709 - 0.0000612236 * (HT**2/TMP_DBH)
    if(CF4_TMP < 0.3):
        CF4_TMP=0.3
    if(CF4_TMP > 0.4):
        CF4_TMP=0.4
        
    # ----------------
    # For ease of use and to improve readability of equations, 
    # calculate the following term and use it in the equations that follow. 
    # Note that actual DBH and BA are used for all trees.
    # Do not use TMP_DBH or BA_TMP here.
    
    TERM = ((1.033 * (1.0 + 1.382937 * math.exp(-4.015292 * (DBH/10.0)))) * (BA + 0.087266) - 0.174533 )
    # ----------------
    
    if DBH >= 6.0:
        CV4 = CF4 * BA * HT
        TARIF = (CV4 * 0.912733) / (BA - 0.087266)
        if (TARIF <= 0.0):
            TARIF=0.01
        CVTS = (CV4 * TERM )/ (BA - 0.087266)
        
        # set floor of CVTS to zero (in case equation generates negative values)
        CVTS = max(0,CVTS)

        CVT = TARIF * (0.9679 - 0.1051 * 0.5523**(DBH-1.5) ) * TERM / 0.912733
    
    elif DBH < 6.0:
        CV4_TMP = CF4_TMP *BA_TMP * HT
        TARIF_TMP = (CV4_TMP * 0.912733) / (BA_TMP - 0.087266)
        if(TARIF_TMP <= 0.0):
            TARIF_TMP = 0.01
        # CALCULATE An ADJUSTED TARIF FOR SMALL TREES (Both DBH and TMP_DBH are used)
        TARIF = TARIF_TMP * ( 0.5 * (TMP_DBH - DBH)**2 + (1.0 + 0.063 * (TMP_DBH - DBH)**2) )
        if(TARIF <= 0.0):
            TARIF = 0.01
        CVTS = TARIF * TERM

        # set floor of CVTS to zero (in case equation generates negative values)
        CVTS = max(0,CVTS)
        
        CVT = TARIF * (0.9679 - 0.1051 * 0.5523**(DBH-1.5) ) * TERM / 0.912733
        CV4 = CF4 * BA * HT #(calculated with actual DBH and BA)
        
    if DBH < 5.0:
        CV4 = 0
    #elif DBH >= 5.0:
    #    pass # THEN KEEP CV4
    
    # record these values in a dictionary
    metric_dict = {}
    for each_metric in ['CVTS', 'TARIF', 'CV4', 'CVT', 'DBH']:
        metric_dict[each_metric] = eval(each_metric)
    
    # if metric requested by user is a cubic volume metric, return it
    return get_metric(metric_dict, metric, 'SW')


# In[28]:

# EQUATION 17 MTN.HEMLOCK (BELL, OSU RES.BULL 35)

# Bell, J.F., Marshall, D.D. and Johnson G.P.  1981.  Tarif tables for mountain hemlock: 
# developed from an equation of total stem cubic-foot volume.  Research Bulletin #35. 
# OSU Forest Research Lab, School of Forestry, Oregon State University, Corvallis, OR.

def Eq_17(DBH, HT, metric):
    """
    WHERE:
    DBH (inches) = DBH (CM) CONVERTED TO INCHES (DBH/2.54)
    HT (feet) = HT (M) CONVERTED TO FEET (HT/0.3048)
    BA = BASAL AREA (DBH IN INCHES) BA= .005454154 x DBH2
    CVTS = CUBIC FOOT VOLUME, INCLUDING TOP AND STUMP
    TARIF = TARIF NUMBER EQUATION (REF. DNR NOTE NO.27, P.2)
    CVT = CUBIC FOOT VOLUME ABOVE STUMP
    CV4 = CUBIC FOOT VOLUME ABOVE STUMP, 4-INCH TOP
    """
    eq_number = 17
    BA = 0.005454154 * DBH**2
    CVTS = 0.001106485 * DBH**1.8140497 * HT**1.2744923
    TARIF = (CVTS * 0.912733)/((1.033 * (1.0 + 1.382937 * math.exp(-4.015292 * DBH))) * (BA + 0.087266) - 0.174533)
    CV4 = TARIF * (BA - 0.087266)/0.912733
    CVT = TARIF * (0.9679 - 0.1051 * 0.5523**(DBH-1.5))*((1.033*(1.0 + 1.382937 * math.exp(-4.015292*(DBH/10.0))))*(BA + 0.087266)-0.174533)/0.912733
    
    # record these values in a dictionary
    metric_dict = {}
    for each_metric in ['CVTS', 'TARIF', 'CV4', 'CVT', 'DBH']:
        metric_dict[each_metric] = eval(each_metric)
    
    # if metric requested by user is a cubic volume metric, return it
    return get_metric(metric_dict, metric, 'SW')


# In[29]:

# EQUATION 18 SHASTA RED FIR (USDA-FS RES NOTE PNW-266)

# MacLean, Colin and John M. Berger.  1976.  Softwood tree-volume equations for major California species.  
# PNW Research Note, PNW-266.  Pacific Northwest Forest and Range Experiment Station, Portland Oregon. 34p.

def Eq_18(DBH, HT, metric):
    """
    WHERE:
    DBH (inches) = DBH (CM) CONVERTED TO INCHES (DBH/2.54)
    HT (feet) = HT (M) CONVERTED TO FEET (HT/0.3048)
    CVTS = CUBIC FOOT VOLUME, INCLUDING TOP AND STUMP
    TARIF = TARIF NUMBER EQUATION (REF. DNR NOTE NO.27, P.2)
    CVT = CUBIC FOOT VOLUME ABOVE STUMP
    CV4 = CUBIC FOOT VOLUME ABOVE STUMP, 4-INCH TOP
    """
    eq_number = 18
    
    # FOR THIS SET OF EQUATIONS CREATE A TEMPORARY DBH AND BA for trees less than 6” DBH
    
    #if DBH < 6.0:     # this conditional statement is unnecessary. TMP_DBH and other TMP variables 
    TMP_DBH = 6.0      # are only called in equations below if DBH <6. Assign TMP_DBH regardless.
    
    # CALCULATE BASAL AREA PER TREE USING DBH AND DBH_TEMP
    BA = DBH**2 * 0.005454154
    BA_TMP = TMP_DBH **2 * 0.005454154
          
    # CALCULATE A CUBIC FORM FACTOR (CF4) USING TMP_DBH and DBH
    # CF4 EQUATIONS VARY BY VOLUME EQUATION
    CF4 = 0.231237 + 0.028176 * (HT/DBH)
    if(CF4 < 0.3):
        CF4=0.3
    if(CF4 > 0.4): 
        CF4=0.4
    CF4_TMP = 0.231237 + 0.028176 * (HT/TMP_DBH)
    if(CF4_TMP < 0.3):
        CF4_TMP=0.3
    if(CF4_TMP > 0.4):
        CF4_TMP=0.4
      
    # ----------------
    # For ease of use and to improve readability of equations, 
    # calculate the following term and use it in the equations that follow. 
    # Note that actual DBH and BA are used for all trees.
    # Do not use TMP_DBH or BA_TMP here.
    
    TERM = ((1.033 * (1.0 + 1.382937 * math.exp(-4.015292 * (DBH/10.0)))) * (BA + 0.087266) - 0.174533 )
    # ----------------
    
    if DBH >= 6.0:
        CV4 = CF4 * BA * HT
        TARIF = (CV4 * 0.912733) / (BA - 0.087266)
        if (TARIF <= 0.0):
            TARIF=0.01
        CVTS = (CV4 * TERM )/ (BA - 0.087266)

        # set floor of CVTS to zero (in case equation generates negative values)
        CVTS = max(0,CVTS)

        CVT = TARIF * (0.9679 - 0.1051 * 0.5523**(DBH-1.5) ) * TERM / 0.912733
    
    elif DBH < 6.0:
        CV4_TMP = CF4_TMP *BA_TMP * HT
        TARIF_TMP = (CV4_TMP * 0.912733) / (BA_TMP - 0.087266)
        if(TARIF_TMP <= 0.0):
            TARIF_TMP = 0.01
        # CALCULATE An ADJUSTED TARIF FOR SMALL TREES (Both DBH and TMP_DBH are used)
        TARIF = TARIF_TMP * ( 0.5 * (TMP_DBH - DBH)**2 + (1.0 + 0.063 * (TMP_DBH - DBH)**2) )
        if(TARIF <= 0.0):
            TARIF = 0.01
        CVTS = TARIF * TERM

        # set floor of CVTS to zero (in case equation generates negative values)
        CVTS = max(0,CVTS)

        CVT = TARIF * (0.9679 - 0.1051 * 0.5523**(DBH-1.5) ) * TERM / 0.912733
        CV4 = CF4 * BA * HT #(calculated with actual DBH and BA)
        
    if DBH < 5.0:
        CV4 = 0
    #elif DBH >= 5.0:
    #    pass # THEN KEEP CV4
    
    # record these values in a dictionary
    metric_dict = {}
    for each_metric in ['CVTS', 'TARIF', 'CV4', 'CVT', 'DBH']:
        metric_dict[each_metric] = eval(each_metric)
    
    # if metric requested by user is a cubic volume metric, return it
    return get_metric(metric_dict, metric, 'SW')


# In[30]:

# EQUATION 19 INCENSE CEDAR (USDA-FS RES NOTE PNW-266)

# MacLean, Colin and John M. Berger.  1976.  Softwood tree-volume equations for major California species.  
# PNW Research Note, PNW-266.  Pacific Northwest Forest and Range Experiment Station, Portland Oregon. 34p.

def Eq_19(DBH, HT, metric):
    """
    WHERE:
    DBH (inches) = DBH (CM) CONVERTED TO INCHES (DBH/2.54)
    HT (feet) = HT (M) CONVERTED TO FEET (HT/0.3048)
    CVTS = CUBIC FOOT VOLUME, INCLUDING TOP AND STUMP
    TARIF = TARIF NUMBER EQUATION (REF. DNR NOTE NO.27, P.2)
    CVT = CUBIC FOOT VOLUME ABOVE STUMP
    CV4 = CUBIC FOOT VOLUME ABOVE STUMP, 4-INCH TOP
    """
    eq_number = 19

    # FOR THIS SET OF EQUATIONS CREATE A TEMPORARY DBH AND BA for trees less than 6” DBH
    
    #if DBH < 6.0:     # this conditional statement is unnecessary. TMP_DBH and other TMP variables 
    TMP_DBH = 6.0      # are only called in equations below if DBH <6. Assign TMP_DBH regardless.
    
    # CALCULATE BASAL AREA PER TREE USING DBH AND DBH_TEMP
    BA = DBH**2 * 0.005454154
    BA_TMP = TMP_DBH **2 * 0.005454154
       
    # CALCULATE A CUBIC FORM FACTOR (CF4) USING TMP_DBH and DBH
    # CF4 EQUATIONS VARY BY VOLUME EQUATION
    CF4 = 0.225786 + 4.44236 * (1/HT)
    if(CF4 < 0.3):
        CF4=0.3
    if(CF4 > 0.4): 
        CF4=0.4
    CF4_TMP = 0.225786 + 4.44236 * (1/HT)
    if(CF4_TMP < 0.3):
        CF4_TMP=0.3
    if(CF4_TMP > 0.4):
        CF4_TMP=0.4
 
    # ----------------
    # For ease of use and to improve readability of equations, 
    # calculate the following term and use it in the equations that follow. 
    # Note that actual DBH and BA are used for all trees.
    # Do not use TMP_DBH or BA_TMP here.
    
    TERM = ((1.033 * (1.0 + 1.382937 * math.exp(-4.015292 * (DBH/10.0)))) * (BA + 0.087266) - 0.174533 )
    # ----------------
    
    if DBH >= 6.0:
        CV4 = CF4 * BA * HT
        TARIF = (CV4 * 0.912733) / (BA - 0.087266)
        if (TARIF <= 0.0):
            TARIF=0.01
        CVTS = (CV4 * TERM )/ (BA - 0.087266)

        # set floor of CVTS to zero (in case equation generates negative values)
        CVTS = max(0,CVTS)

        CVT = TARIF * (0.9679 - 0.1051 * 0.5523**(DBH-1.5) ) * TERM / 0.912733
    
    elif DBH < 6.0:
        CV4_TMP = CF4_TMP *BA_TMP * HT
        TARIF_TMP = (CV4_TMP * 0.912733) / (BA_TMP - 0.087266)
        if(TARIF_TMP <= 0.0):
            TARIF_TMP = 0.01
        # CALCULATE An ADJUSTED TARIF FOR SMALL TREES (Both DBH and TMP_DBH are used)
        TARIF = TARIF_TMP * ( 0.5 * (TMP_DBH - DBH)**2 + (1.0 + 0.063 * (TMP_DBH - DBH)**2) )
        if(TARIF <= 0.0):
            TARIF = 0.01
        CVTS = TARIF * TERM

        # set floor of CVTS to zero (in case equation generates negative values)
        CVTS = max(0,CVTS)

        CVT = TARIF * (0.9679 - 0.1051 * 0.5523**(DBH-1.5) ) * TERM / 0.912733
        CV4 = CF4 * BA * HT #(calculated with actual DBH and BA)
        
    if DBH < 5.0:
        CV4 = 0
    #elif DBH >= 5.0:
    #    pass # THEN KEEP CV4
    
    # record these values in a dictionary
    metric_dict = {}
    for each_metric in ['CVTS', 'TARIF', 'CV4', 'CVT', 'DBH']:
        metric_dict[each_metric] = eval(each_metric)
    
    # if metric requested by user is a cubic volume metric, return it
    return get_metric(metric_dict, metric, 'SW')


# In[31]:

# EQUATION 20 SUGAR PINE (USDA-FS RES NOTE PNW-266)

# MacLean, Colin and John M. Berger.  1976.  Softwood tree-volume equations for major California species.  
# PNW Research Note, PNW-266.  Pacific Northwest Forest and Range Experiment Station, Portland Oregon. 34p.

def Eq_20(DBH, HT, metric):
    """
    WHERE:
    DBH (inches) = DBH (CM) CONVERTED TO INCHES (DBH/2.54)
    HT (feet) = HT (M) CONVERTED TO FEET (HT/0.3048)
    CVTS = CUBIC FOOT VOLUME, INCLUDING TOP AND STUMP
    TARIF = TARIF NUMBER EQUATION (REF. DNR NOTE NO.27, P.2)
    CVT = CUBIC FOOT VOLUME ABOVE STUMP
    CV4 = CUBIC FOOT VOLUME ABOVE STUMP, 4-INCH TOP
    """
    eq_number = 19
    
    # FOR THIS SET OF EQUATIONS CREATE A TEMPORARY DBH AND BA for trees less than 6” DBH
    
    #if DBH < 6.0:     # this conditional statement is unnecessary. TMP_DBH and other TMP variables 
    TMP_DBH = 6.0      # are only called in equations below if DBH <6. Assign TMP_DBH regardless.
    
    # CALCULATE BASAL AREA PER TREE USING DBH AND DBH_TEMP
    BA = DBH**2 * 0.005454154
    BA_TMP = TMP_DBH **2 * 0.005454154

    # CALCULATE A CUBIC FORM FACTOR (CF4) USING TMP_DBH and DBH
    # CF4 EQUATIONS VARY BY VOLUME EQUATION
    CF4 = 0.358550 - 0.488134 * (1/DBH)
    if(CF4 < 0.3):
        CF4=0.3
    if(CF4 > 0.4): 
        CF4=0.4
    CF4_TMP = 0.358550 - 0.488134 * (1/ TMP_DBH)
    if(CF4_TMP < 0.3):
        CF4_TMP=0.3
    if(CF4_TMP > 0.4):
        CF4_TMP=0.4

    # ----------------
    # For ease of use and to improve readability of equations, 
    # calculate the following term and use it in the equations that follow. 
    # Note that actual DBH and BA are used for all trees.
    # Do not use TMP_DBH or BA_TMP here.
    
    TERM = ((1.033 * (1.0 + 1.382937 * math.exp(-4.015292 * (DBH/10.0)))) * (BA + 0.087266) - 0.174533 )
    # ----------------
    
    if DBH >= 6.0:
        CV4 = CF4 * BA * HT
        TARIF = (CV4 * 0.912733) / (BA - 0.087266)
        if (TARIF <= 0.0):
            TARIF=0.01
        CVTS = (CV4 * TERM )/ (BA - 0.087266)

        # set floor of CVTS to zero (in case equation generates negative values)
        CVTS = max(0,CVTS)

        CVT = TARIF * (0.9679 - 0.1051 * 0.5523**(DBH-1.5) ) * TERM / 0.912733
    
    elif DBH < 6.0:
        CV4_TMP = CF4_TMP *BA_TMP * HT
        TARIF_TMP = (CV4_TMP * 0.912733) / (BA_TMP - 0.087266)
        if(TARIF_TMP <= 0.0):
            TARIF_TMP = 0.01
        # CALCULATE An ADJUSTED TARIF FOR SMALL TREES (Both DBH and TMP_DBH are used)
        TARIF = TARIF_TMP * ( 0.5 * (TMP_DBH - DBH)**2 + (1.0 + 0.063 * (TMP_DBH - DBH)**2) )
        if(TARIF <= 0.0):
            TARIF = 0.01
        CVTS = TARIF * TERM

        # set floor of CVTS to zero (in case equation generates negative values)
        CVTS = max(0,CVTS)
    
        CVT = TARIF * (0.9679 - 0.1051 * 0.5523**(DBH-1.5) ) * TERM / 0.912733
        CV4 = CF4 * BA * HT #(calculated with actual DBH and BA)
        
    if DBH < 5.0:
        CV4 = 0
    #elif DBH >= 5.0:
    #    pass # THEN KEEP CV4
    
    # record these values in a dictionary
    metric_dict = {}
    for each_metric in ['CVTS', 'TARIF', 'CV4', 'CVT', 'DBH']:
        metric_dict[each_metric] = eval(each_metric)
    
    # if metric requested by user is a cubic volume metric, return it
    return get_metric(metric_dict, metric, 'SW')


# In[32]:

# EQUATION 21 W.JUNIPER (CHITTESTER,1984)

# Chittester, Judith and Colin MacLean.  1984.  Cubic-foot tree-volume equations and tables for western juniper.  
# Research Note, PNW-420. Pacific Northwest Forest and Range Experiment Station. Portland, Oregon. 8p.

def Eq_21(DBH, HT, metric):
    """
    WHERE:
    DBH (inches) = DBH (CM) CONVERTED TO INCHES (DBH/2.54)
    HT (feet) = HT (M) CONVERTED TO FEET (HT/0.3048)
    BA = BASAL AREA (DBH IN INCHES) BA= .005454154 x DBH2
    CVTS = CUBIC FOOT VOLUME, INCLUDING TOP AND STUMP
    TARIF = TARIF NUMBER EQUATION (REF. DNR NOTE NO.27, P.2)
    CVT = CUBIC FOOT VOLUME ABOVE STUMP
    CV4 = CUBIC FOOT VOLUME ABOVE STUMP, 4-INCH TOP
    """
    eq_number = 21
    BA = 0.005454154 * DBH**2
    CVTS = 0.005454154 * (0.30708901 + 0.00086157622 * HT - 0.0037255243 * DBH * HT/(HT-4.5)) * DBH**2 * HT * (HT/(HT-4.5))**2
    
    TARIF = (CVTS * 0.912733)/((1.033 * (1.0 + 1.382937 * math.exp(-4.015292 * DBH))) * (BA + 0.087266) - 0.174533)
    CV4 = (CVTS + 3.48) / (1.18052 + 0.32736 * math.exp(-0.1 * DBH)) - 2.948
    CVT = TARIF * (0.9679 - 0.1051 * 0.5523**(DBH-1.5))*((1.033*(1.0 + 1.382937 * math.exp(-4.015292*(DBH/10.0))))*(BA + 0.087266)-0.174533)/0.912733
    
    if CVTS < 0:
        CVTS = 2
    if CV4 < 0:
        CV4 = 1
    
    # record these values in a dictionary
    metric_dict = {}
    for each_metric in ['CVTS', 'TARIF', 'CV4', 'CVT', 'DBH']:
        metric_dict[each_metric] = eval(each_metric)
    
    # if metric requested by user is a cubic volume metric, return it
    return get_metric(metric_dict, metric, 'SW')


# In[33]:

# EQUATION 22 W.LARCH (LARCH--DNR RPT#24,1977)
def Eq_22(DBH, HT, metric):
    """
    WHERE:
    DBH (inches) = DBH (CM) CONVERTED TO INCHES (DBH/2.54)
    HT (feet) = HT (M) CONVERTED TO FEET (HT/0.3048)
    BA = BASAL AREA (DBH IN INCHES) BA= .005454154 x DBH2
    CVTSL = LOG BASE 10, CUBIC FOOT VOLUME, INCLUDING TOP AND STUMP
    CVTS = CUBIC FOOT VOLUME, INCLUDING TOP AND STUMP
    TARIF = TARIF NUMBER EQUATION (REF. DNR NOTE NO.27, P.2)
    CVT = CUBIC FOOT VOLUME ABOVE STUMP
    CV4 = CUBIC FOOT VOLUME ABOVE STUMP, 4-INCH TOP
    """
    eq_number = 22
    BA = 0.005454154 * DBH**2
    # note that math.log() uses natural logarithm while math.log10() uses log base 10
    CVTSL = -2.624325 + 1.847123 * math.log10(DBH) + 1.044007 * math.log10(HT)
    CVTS = 10**CVTSL
    TARIF = (CVTS * 0.912733)/((1.033 * (1.0 + 1.382937 * math.exp(-4.015292 * DBH))) * (BA + 0.087266) - 0.174533)
    CV4 = TARIF * (BA - 0.087266)/0.912733
    CVT = TARIF * (0.9679 - 0.1051 * 0.5523**(DBH-1.5))*((1.033*(1.0 + 1.382937 * math.exp(-4.015292*(DBH/10.0))))*(BA + 0.087266)-0.174533)/0.912733
    
    # record these values in a dictionary
    metric_dict = {}
    for each_metric in ['CVTS', 'TARIF', 'CV4', 'CVT', 'DBH']:
        metric_dict[each_metric] = eval(each_metric)
    
    # if metric requested by user is a cubic volume metric, return it
    return get_metric(metric_dict, metric, 'SW')


# In[34]:

# EQUATION 23 WHITE FIR (USDA-FS RES NOTE PNW-266)

# MacLean, Colin and John M. Berger.  1976.  Softwood tree-volume equations for major California species.  
# PNW Research Note, PNW-266.  Pacific Northwest Forest and Range Experiment Station, Portland Oregon. 34p.

def Eq_23(DBH, HT, metric):
    """
    WHERE:
    DBH (inches) = DBH (CM) CONVERTED TO INCHES (DBH/2.54)
    HT (feet) = HT (M) CONVERTED TO FEET (HT/0.3048)
    CVTS = CUBIC FOOT VOLUME, INCLUDING TOP AND STUMP
    TARIF = TARIF NUMBER EQUATION (REF. DNR NOTE NO.27, P.2)
    CVT = CUBIC FOOT VOLUME ABOVE STUMP
    CV4 = CUBIC FOOT VOLUME ABOVE STUMP, 4-INCH TOP
    """
    eq_number = 23
        
    # FOR THIS SET OF EQUATIONS CREATE A TEMPORARY DBH AND BA for trees less than 6” DBH
    
    #if DBH < 6.0:     # this conditional statement is unnecessary. TMP_DBH and other TMP variables 
    TMP_DBH = 6.0      # are only called in equations below if DBH <6. Assign TMP_DBH regardless.
    
    # CALCULATE BASAL AREA PER TREE USING DBH AND DBH_TEMP
    BA = DBH**2 * 0.005454154
    BA_TMP = TMP_DBH **2 * 0.005454154
    
    # CALCULATE A CUBIC FORM FACTOR (CF4) USING TMP_DBH and DBH
    # CF4 EQUATIONS VARY BY VOLUME EQUATION
    CF4 = 0.299039 + 1.91272 * (1/HT) + 0.0000367217 * (HT**2/DBH)
    if(CF4 < 0.3):
        CF4=0.3
    if(CF4 > 0.4): 
        CF4=0.4
    CF4_TMP = 0.299039 + 1.91272 * (1/HT) + 0.0000367217 * (HT**2/TMP_DBH)
    if(CF4_TMP < 0.3):
        CF4_TMP=0.3
    if(CF4_TMP > 0.4):
        CF4_TMP=0.4

    # ----------------
    # For ease of use and to improve readability of equations, 
    # calculate the following term and use it in the equations that follow. 
    # Note that actual DBH and BA are used for all trees.
    # Do not use TMP_DBH or BA_TMP here.
    
    TERM = ((1.033 * (1.0 + 1.382937 * math.exp(-4.015292 * (DBH/10.0)))) * (BA + 0.087266) - 0.174533 )
    # ----------------
    
    if DBH >= 6.0:
        CV4 = CF4 * BA * HT
        TARIF = (CV4 * 0.912733) / (BA - 0.087266)
        if (TARIF <= 0.0):
            TARIF=0.01
        CVTS = (CV4 * TERM )/ (BA - 0.087266)

        # set floor of CVTS to zero (in case equation generates negative values)
        CVTS = max(0,CVTS)

        CVT = TARIF * (0.9679 - 0.1051 * 0.5523**(DBH-1.5) ) * TERM / 0.912733
    
    elif DBH < 6.0:
        CV4_TMP = CF4_TMP *BA_TMP * HT
        TARIF_TMP = (CV4_TMP * 0.912733) / (BA_TMP - 0.087266)
        if(TARIF_TMP <= 0.0):
            TARIF_TMP = 0.01
        # CALCULATE An ADJUSTED TARIF FOR SMALL TREES (Both DBH and TMP_DBH are used)
        TARIF = TARIF_TMP * ( 0.5 * (TMP_DBH - DBH)**2 + (1.0 + 0.063 * (TMP_DBH - DBH)**2) )
        if(TARIF <= 0.0):
            TARIF = 0.01
        CVTS = TARIF * TERM

        # set floor of CVTS to zero (in case equation generates negative values)
        CVTS = max(0,CVTS)

        CVT = TARIF * (0.9679 - 0.1051 * 0.5523**(DBH-1.5) ) * TERM / 0.912733
        CV4 = CF4 * BA * HT #(calculated with actual DBH and BA)
        
    if DBH < 5.0:
        CV4 = 0
    #elif DBH >= 5.0:
    #    pass # THEN KEEP CV4
    
    # record these values in a dictionary
    metric_dict = {}
    for each_metric in ['CVTS', 'TARIF', 'CV4', 'CVT', 'DBH']:
        metric_dict[each_metric] = eval(each_metric)
    
    # if metric requested by user is a cubic volume metric, return it
    return get_metric(metric_dict, metric, 'SW')


# In[35]:

# EQUATION 24 REDWOOD (Krumland, B.E. and L.E. Wensel. 1975. And DNR RPT#24,1977)

# Krumland, B.E. and L.E. Wensel. 1975. Preliminary young growth volume tables for coastal California conifers.  
# Research Note #1. In-house memo. Co-op Redwood Yield Research Project. Department of Forestry and Conservation, 
# College of Natural Resources, U of Cal, Berkeley.  On file with the PNW Research Station.

def Eq_24(DBH, HT, metric):
    """
    WHERE:
    DBH (inches) = DBH (CM) CONVERTED TO INCHES (DBH/2.54)
    HT (feet) = HT (M) CONVERTED TO FEET (HT/0.3048)
    BA = BASAL AREA (DBH IN INCHES) BA= .005454154 x DBH2
    CVTS = CUBIC FOOT VOLUME, INCLUDING TOP AND STUMP
    TARIF = TARIF NUMBER EQUATION (REF. DNR NOTE NO.27, P.2)
    CVT = CUBIC FOOT VOLUME ABOVE STUMP
    CV4 = CUBIC FOOT VOLUME ABOVE STUMP, 4-INCH TOP
    """
    eq_number = 24
    BA = 0.005454154 * DBH**2
    # note that math.log() uses natural logarithm while math.log10() uses log base 10
    CVTS = math.exp(-6.2597 + 1.9967 * math.log(DBH) + 0.9642 * math.log(HT))
    TARIF = (CVTS * 0.912733)/((1.033 * (1.0 + 1.382937 * math.exp(-4.015292 * DBH))) * (BA + 0.087266) - 0.174533)
    CV4 = TARIF * (BA - 0.087266) / 0.912733
    CVT = TARIF * (0.9679 - 0.1051 * 0.5523**(DBH-1.5))*((1.033*(1.0 + 1.382937 * math.exp(-4.015292*(DBH/10.0))))*(BA + 0.087266)-0.174533)/0.912733
    
    # record these values in a dictionary
    metric_dict = {}
    for each_metric in ['CVTS', 'TARIF', 'CV4', 'CVT', 'DBH']:
        metric_dict[each_metric] = eval(each_metric)
    
    # if metric requested by user is a cubic volume metric, return it
    return get_metric(metric_dict, metric, 'SW')


# In[36]:

# EQUATION 25 ALDER (CURTIS/BRUCE, PNW-56)

# Curtis, Robert O., Bruce, David, and Caryanne VanCoevering. 1968. Volume and taper tables for red
# alder.  US Forest Serv. Res. Pap. PNW-56.  PNW Forest & Range Exp. Sta., Portland, Oregon.  35p.

def Eq_25(DBH, HT, metric):
    """
    WHERE:
    DBH = DBH(CM) CONVERTED TO INCHES (DBH/2.54)
    HT = HT (M) CONVERTED TO FEET (HT/0.3048)
    BA = BASAL AREA (DBH IN INCHES) BA= .005454154 x DBH2
    CVTS = CUBIC FOOT VOLUME, TOTAL STEM, WITH TOP AND STUMP
    TARIF = TARIF NUMBER EQUATION
    CVT = CUBIC FOOT VOLUME ABOVE STUMP
    CV4 = CUBIC FOOT VOLUME, 4-IN TOP
    CV8 = CUBIC FOOT VOLUME, SAWLOG (8-IN TOP)
    """
    eq_number = 25
    
    if HT <18:
        HT = 18
    
    BA = 0.005454154 * DBH**2
    Z = (HT - 0.5 - DBH/24.0)/(HT - 4.5)
    F = 0.3651*Z**2.5 - 7.9032*(Z**2.5)*DBH/1000.0 + 3.295*(Z**2.5)*HT/1000.0 - 1.9856*(Z**2.5)*HT*DBH/100000.0 +         -2.9668*(Z**2.5)*(HT**2)/1000000.0 + 1.5092*(Z**2.5)*(HT**0.5)/1000.0 + 4.9395*(Z**4)*DBH/1000.0 +         -2.05937*(Z**4)*HT/1000.0 + 1.5042*(Z**33)*HT*DBH/1000000.0 - 1.1433*(Z**33)*(HT**0.5)/10000.0 + 1.809*(Z**41)*(HT**2)/10000000.0
    
    CVT = 0.00545415 * DBH**2 * (HT-4.5)*F
    TARIF = (CVT * 0.912733)/((0.9679 - 1.051 * 0.5523**(DBH-1.5))*(1.033 * (1.0 + 1.382937 * math.exp(-4.015292 * DBH))) * (BA + 0.087266) - 0.174533)
    CVTS = TARIF * ((1.0330*(1.0 + 1.382937 * math.exp(-4.015292*(DBH/10.0))))*(BA*0.087266)-0.174533)/0.912733
    
    # set floor of CVTS to zero (in case equation generates negative values)
    CVTS = max(0,CVTS)
    
    CV4 = TARIF * (BA - 0.087266)/0.912733
    RC8 = 0.983 - (0.983 * 0.65**(DBH-8.6))
    CV8 = RC8 * CV4
    # CV4X = CV4 # this is not used in this set of equations, only in BF calculation and is calculated there
    
    # record these values in a dictionary
    metric_dict = {}
    for each_metric in ['CVTS', 'TARIF', 'CV4', 'CVT', 'CV8', 'DBH', 'eq_number', 'HT']:
        metric_dict[each_metric] = eval(each_metric)
    
    # if metric requested by user is a cubic volume metric, return it
    return get_metric(metric_dict, metric, 'HW')


# In[37]:

# EQUATION 26 ALDER (BC-ALDER--DNR RPT#24,1977)

# Brackett, Michael.  1977. Notes on TARIF tree-volume computation.  DNR report #24. 
# State of Washington, Department of Natural Resources, Olympia, WA. 132p.

def Eq_26(DBH, HT, metric):
    """
    WHERE:
    DBH (inches) = DBH (CM) CONVERTED TO INCHES (DBH/2.54)
    HT (feet) = HT (M) CONVERTED TO FEET (HT/0.3048)
    BA = BASAL AREA (DBH IN INCHES) BA= .005454154 x DBH2
    CVTSL = LOG BASE 10, CUBIC FOOT VOLUME, INCLUDING TOP AND STUMP
    CVTS = CUBIC FOOT VOLUME, INCLUDING TOP AND STUMP
    TARIF = TARIF NUMBER EQUATION (REF. DNR NOTE NO.27, P.2)
    CVT = CUBIC FOOT VOLUME ABOVE STUMP
    CV4 = CUBIC FOOT VOLUME ABOVE STUMP, 4-INCH TOP
    """
    eq_number = 26
    
    BA = 0.005454154 * DBH**2
    # note that math.log() uses natural logarithm while math.log10() uses log base 10
    CVTSL = -2.672775 + 1.920617 * math.log10(DBH) + 1.074024 * math.log10(HT)
    CVTS = 10**CVTSL
    TARIF = (CVTS * 0.912733)/((1.033 * (1.0 + 1.382937 * math.exp(-4.015292 * DBH))) * (BA + 0.087266) - 0.174533)
    CVT = TARIF * (0.9679 - 0.1051 * 0.5523**(DBH-1.5))*((1.033*(1.0 + 1.382937 * math.exp(-4.015292*(DBH/10.0))))*(BA + 0.087266)-0.174533)/0.912733
    CV4 = TARIF * (BA - 0.087266)/0.912733
    RC8 = 0.983 - (0.983 * 0.65**(DBH-8.6))
    CV8 = RC8 * CV4
    # CV4X = CV4 # this is not used in this set of equations, only in BF calculation and is calculated there
    
    # record these values in a dictionary
    metric_dict = {}
    for each_metric in ['CVTS', 'TARIF', 'CV4', 'CVT', 'CV8', 'DBH', 'eq_number', 'HT']:
        metric_dict[each_metric] = eval(each_metric)
    
    # if metric requested by user is a cubic volume metric, return it
    return get_metric(metric_dict, metric, 'HW')


# In[38]:

# EQUATION 27 COTTONWOOD (BC-COTTONWOOD--DNR RPT#24,1977)

# Brackett, Michael.  1977. Notes on TARIF tree-volume computation.  DNR report #24. 
# State of Washington, Department of Natural Resources, Olympia, WA. 132p.

def Eq_27(DBH, HT, metric):
    """
    WHERE:
    DBH (inches) = DBH (CM) CONVERTED TO INCHES (DBH/2.54)
    HT (feet) = HT (M) CONVERTED TO FEET (HT/0.3048)
    BA = BASAL AREA (DBH IN INCHES) BA= .005454154 x DBH2
    CVTSL = LOG BASE 10, CUBIC FOOT VOLUME, INCLUDING TOP AND STUMP
    CVTS = CUBIC FOOT VOLUME, INCLUDING TOP AND STUMP
    TARIF = TARIF NUMBER EQUATION (REF. DNR NOTE NO.27, P.2)
    CVT = CUBIC FOOT VOLUME ABOVE STUMP
    CV4 = CUBIC FOOT VOLUME ABOVE STUMP, 4-INCH TOP
    """
    eq_number = 27
    
    BA = 0.005454154 * DBH**2
    # note that math.log() uses natural logarithm while math.log10() uses log base 10
    CVTSL = -2.945047 + 1.803973 * math.log10(DBH) + 1.238853 * math.log10(HT)
    CVTS = 10**CVTSL
    TARIF = (CVTS * 0.912733)/((1.033 * (1.0 + 1.382937 * math.exp(-4.015292 * DBH))) * (BA + 0.087266) - 0.174533)
    CVT = TARIF * (0.9679 - 0.1051 * 0.5523**(DBH-1.5))*((1.033*(1.0 + 1.382937 * math.exp(-4.015292*(DBH/10.0))))*(BA + 0.087266)-0.174533)/0.912733
    CV4 = TARIF * (BA - 0.087266)/0.912733
    RC8 = 0.983 - (0.983 * 0.65**(DBH-8.6))
    CV8 = RC8 * CV4
    # CV4X = CV4 # this is not used in this set of equations, only in BF calculation and is calculated there
    
    # record these values in a dictionary
    metric_dict = {}
    for each_metric in ['CVTS', 'TARIF', 'CV4', 'CVT', 'CV8', 'DBH', 'eq_number', 'HT']:
        metric_dict[each_metric] = eval(each_metric)
    
    # if metric requested by user is a cubic volume metric, return it
    return get_metric(metric_dict, metric, 'HW')


# In[39]:

# EQUATION 28 ASPEN (BC-ASPEN--DNR RPT#24,1977)

# Brackett, Michael.  1977. Notes on TARIF tree-volume computation.  DNR report #24. 
# State of Washington, Department of Natural Resources, Olympia, WA. 132p.

def Eq_28(DBH, HT, metric):
    """
    WHERE:
    DBH (inches) = DBH (CM) CONVERTED TO INCHES (DBH/2.54)
    HT (feet) = HT (M) CONVERTED TO FEET (HT/0.3048)
    BA = BASAL AREA (DBH IN INCHES) BA= .005454154 x DBH2
    CVTSL = LOG BASE 10, CUBIC FOOT VOLUME, INCLUDING TOP AND STUMP
    CVTS = CUBIC FOOT VOLUME, INCLUDING TOP AND STUMP
    TARIF = TARIF NUMBER EQUATION (REF. DNR NOTE NO.27, P.2)
    CVT = CUBIC FOOT VOLUME ABOVE STUMP
    CV4 = CUBIC FOOT VOLUME ABOVE STUMP, 4-INCH TOP
    """
    eq_number = 28
    
    BA = 0.005454154 * DBH**2
    # note that math.log() uses natural logarithm while math.log10() uses log base 10
    CVTSL = -2.635360 + 1.946034 * math.log10(DBH) + 1.024793 * math.log10(HT)
    CVTS = 10**CVTSL
    TARIF = (CVTS * 0.912733)/((1.033 * (1.0 + 1.382937 * math.exp(-4.015292 * DBH))) * (BA + 0.087266) - 0.174533)
    CVT = TARIF * (0.9679 - 0.1051 * 0.5523**(DBH-1.5))*((1.033*(1.0 + 1.382937 * math.exp(-4.015292*(DBH/10.0))))*(BA + 0.087266)-0.174533)/0.912733
    CV4 = TARIF * (BA - 0.087266)/0.912733
    RC8 = 0.983 - (0.983 * 0.65**(DBH-8.6))
    CV8 = RC8 * CV4
    # CV4X = CV4 # this is not used in this set of equations, only in BF calculation and is calculated there
    
    # record these values in a dictionary
    metric_dict = {}
    for each_metric in ['CVTS', 'TARIF', 'CV4', 'CVT', 'CV8', 'DBH', 'eq_number', 'HT']:
        metric_dict[each_metric] = eval(each_metric)
    
    # if metric requested by user is a cubic volume metric, return it
    return get_metric(metric_dict, metric, 'HW')


# In[40]:

# EQUATION 29 BIRCH (BC-BIRCH--DNR RPT#24,1977)

# Brackett, Michael.  1977. Notes on TARIF tree-volume computation.  DNR report #24. 
# State of Washington, Department of Natural Resources, Olympia, WA. 132p.

def Eq_29(DBH, HT, metric):
    """
    WHERE:
    DBH (inches) = DBH (CM) CONVERTED TO INCHES (DBH/2.54)
    HT (feet) = HT (M) CONVERTED TO FEET (HT/0.3048)
    BA = BASAL AREA (DBH IN INCHES) BA= .005454154 x DBH2
    CVTSL = LOG BASE 10, CUBIC FOOT VOLUME, INCLUDING TOP AND STUMP
    CVTS = CUBIC FOOT VOLUME, INCLUDING TOP AND STUMP
    TARIF = TARIF NUMBER EQUATION (REF. DNR NOTE NO.27, P.2)
    CVT = CUBIC FOOT VOLUME ABOVE STUMP
    CV4 = CUBIC FOOT VOLUME ABOVE STUMP, 4-INCH TOP
    """
    eq_number = 29
    
    BA = 0.005454154 * DBH**2
    # note that math.log() uses natural logarithm while math.log10() uses log base 10
    CVTSL = -2.757813 + 1.911681 * math.log10(DBH) + 1.105403 * math.log10(HT)
    CVTS = 10**CVTSL
    TARIF = (CVTS * 0.912733)/((1.033 * (1.0 + 1.382937 * math.exp(-4.015292 * DBH))) * (BA + 0.087266) - 0.174533)
    CVT = TARIF * (0.9679 - 0.1051 * 0.5523**(DBH-1.5))*((1.033*(1.0 + 1.382937 * math.exp(-4.015292*(DBH/10.0))))*(BA + 0.087266)-0.174533)/0.912733
    CV4 = TARIF * (BA - 0.087266)/0.912733
    RC8 = 0.983 - (0.983 * 0.65**(DBH-8.6))
    CV8 = RC8 * CV4
    # CV4X = CV4 # this is not used in this set of equations, only in BF calculation and is calculated there
    
    # record these values in a dictionary
    metric_dict = {}
    for each_metric in ['CVTS', 'TARIF', 'CV4', 'CVT', 'CV8', 'DBH', 'eq_number', 'HT']:
        metric_dict[each_metric] = eval(each_metric)
    
    # if metric requested by user is a cubic volume metric, return it
    return get_metric(metric_dict, metric, 'HW')


# In[41]:

# EQUATION 30 BIGLEAF MAPLE (BC-MAPLE--DNR RPT#24,1977)

# Brackett, Michael.  1977. Notes on TARIF tree-volume computation.  DNR report #24. 
# State of Washington, Department of Natural Resources, Olympia, WA. 132p.

def Eq_30(DBH, HT, metric):
    """
    WHERE:
    DBH (inches) = DBH (CM) CONVERTED TO INCHES (DBH/2.54)
    HT (feet) = HT (M) CONVERTED TO FEET (HT/0.3048)
    BA = BASAL AREA (DBH IN INCHES) BA= .005454154 x DBH2
    CVTSL = LOG BASE 10, CUBIC FOOT VOLUME, INCLUDING TOP AND STUMP
    CVTS = CUBIC FOOT VOLUME, INCLUDING TOP AND STUMP
    TARIF = TARIF NUMBER EQUATION (REF. DNR NOTE NO.27, P.2)
    CVT = CUBIC FOOT VOLUME ABOVE STUMP
    CV4 = CUBIC FOOT VOLUME ABOVE STUMP, 4-INCH TOP
    """
    eq_number = 30
    
    BA = 0.005454154 * DBH**2
    # note that math.log() uses natural logarithm while math.log10() uses log base 10
    CVTSL = -2.770324 + 1.885813 * math.log10(DBH) + 1.119043 * math.log10(HT)
    CVTS = 10**CVTSL
    TARIF = (CVTS * 0.912733)/((1.033 * (1.0 + 1.382937 * math.exp(-4.015292 * DBH))) * (BA + 0.087266) - 0.174533)
    CVT = TARIF * (0.9679 - 0.1051 * 0.5523**(DBH-1.5))*((1.033*(1.0 + 1.382937 * math.exp(-4.015292*(DBH/10.0))))*(BA + 0.087266)-0.174533)/0.912733
    CV4 = TARIF * (BA - 0.087266)/0.912733
    RC8 = 0.983 - (0.983 * 0.65**(DBH-8.6))
    CV8 = RC8 * CV4
    # CV4X = CV4 # this is not used in this set of equations, only in BF calculation and is calculated there
    
    # record these values in a dictionary
    metric_dict = {}
    for each_metric in ['CVTS', 'TARIF', 'CV4', 'CVT', 'CV8', 'DBH', 'eq_number', 'HT']:
        metric_dict[each_metric] = eval(each_metric)
    
    # if metric requested by user is a cubic volume metric, return it
    return get_metric(metric_dict, metric, 'HW')


# In[42]:

# EQUATION 31 EUCALYPTUS (MEMO,COLIN D. MacLEAN 1/27/83,(REVISED 2/7/83) )

# Colin MacLean and Tom Farrenkopf. 1983. Eucalyptus volume equation.  In-house memo 
# describing the volume equation for CVTS, to be used for all species of Eucalyptus.  
# The equation was developed from 111 trees.  On file at the PNW Research Station, Portland,OR.

def Eq_31(DBH, HT, metric):
    """
    WHERE:
    DBH (inches) = DBH (CM) CONVERTED TO INCHES (DBH/2.54)
    HT (feet) = HT (M) CONVERTED TO FEET (HT/0.3048)
    BA = BASAL AREA (DBH IN INCHES) BA= .005454154 x DBH2
    CVTS = CUBIC FOOT VOLUME, INCLUDING TOP AND STUMP
    TARIF = TARIF NUMBER EQUATION (REF. DNR NOTE NO.27, P.2)
    CVT = CUBIC FOOT VOLUME ABOVE STUMP
    CV4 = CUBIC FOOT VOLUME ABOVE STUMP, 4-INCH TOP
    """
    eq_number = 31
    
    BA = 0.005454154 * DBH**2
    # note that math.log() uses natural logarithm while math.log10() uses log base 10
    CVTS = 0.0016144 * DBH**2 * HT
    TARIF = (CVTS * 0.912733)/((1.033 * (1.0 + 1.382937 * math.exp(-4.015292 * DBH))) * (BA + 0.087266) - 0.174533)
    CVT = TARIF * (0.9679 - 0.1051 * 0.5523**(DBH-1.5))*((1.033*(1.0 + 1.382937 * math.exp(-4.015292*(DBH/10.0))))*(BA + 0.087266)-0.174533)/0.912733
    CV4 = TARIF * (BA - 0.087266)/0.912733
    RC8 = 0.983 - (0.983 * 0.65**(DBH-8.6))
    CV8 = RC8 * CV4
    # CV4X = CV4 # this is not used in this set of equations, only in BF calculation and is calculated there
    
    # record these values in a dictionary
    metric_dict = {}
    for each_metric in ['CVTS', 'TARIF', 'CV4', 'CVT', 'CV8', 'DBH', 'eq_number', 'HT']:
        metric_dict[each_metric] = eval(each_metric)
    
    # if metric requested by user is a cubic volume metric, return it
    return get_metric(metric_dict, metric, 'HW')


# In[43]:

# EQUATION 32 G.CHINQUAPIN (PILLSBURY (H,D), CHARLES BOLSINGER 1/3/83)

# Pillsbury, Norman H. and Michael L. Kirkley. 1984.  Equations for Total, Wood, and 
# Saw-log Volume for Thirteen California Hardwoods.  PNW Research Note, PNW-414. 
# Pacific Northwest Research Station, Portland Oregon. 52p.

def Eq_32(DBH, HT, metric):
    """
    WHERE
    DBH = DBH(CM) CONVERTED TO INCHES (DBH/2.54)
    HT = HT (M) CONVERTED TO FEET (HT/0.3048)
    BA = BASAL AREA (DBH IN INCHES) BA= .005454154 x DBH2
    CVTS = CUBIC FOOT VOLUME, TOTAL STEM, WITH TOP AND STUMP
    TARIF = TARIF NUMBER EQUATION
    CVT = CUBIC FOOT VOLUME ABOVE STUMP
    CV4 = CUBIC FOOT VOLUME, 4-IN TOP
    CV8 = CUBIC FOOT VOLUME, SAWLOG (8-IN TOP)
    """
    eq_number = 32
    
    BA = 0.005454154 * DBH**2
    CVTS = 0.0120372263 * DBH**2.02232 * HT**0.68638
    CV4 = 0.0055212937 * DBH**2.07202 * HT**0.77467
    CV8 = 0.0018985111 * DBH**2.38285 * HT**0.77105
    RTS = 0.9679 - 0.1051 * 0.5523**(DBH - 1.5) # RTS is not defined in the documentation
    CVT = CVTS * RTS #  RTS appears to be proportion of cubic volume in tree above stump
    # CV4X = CVT * (0.99875 - 43.336/DBH**3 - 124.717/DBH**4 + (0.193437*HT)/DBH**3 + 479.83/(DBH**3 * HT)) 
        # this is not used in this set of equations, only in BF calculation and is calculated there
    try:
        TARIF = (CV8 * 0.912733)/((0.983 - 0.983 * 0.65**(DBH-8.6)) * (BA - 0.087266))
    except ZeroDivisionError:
        TARIF = 0.01
    
    # record these values in a dictionary
    metric_dict = {}
    for each_metric in ['CVTS', 'TARIF', 'CV4', 'CVT', 'CV8', 'DBH', 'eq_number', 'HT']:
        metric_dict[each_metric] = eval(each_metric)
    
    # if metric requested by user is a cubic volume metric, return it
    return get_metric(metric_dict, metric, 'HW')


# In[44]:

# EQUATION 33 C.LAUREL (PILLSBURY (H,D), CHARLES BOLSINGER 1/3/83)

# Pillsbury, Norman H. and Michael L. Kirkley. 1984.  Equations for Total, Wood, and 
# Saw-log Volume for Thirteen California Hardwoods.  PNW Research Note, PNW-414. 
# Pacific Northwest Research Station, Portland Oregon. 52p.

def Eq_33(DBH, HT, metric):
    """
    WHERE
    DBH = DBH(CM) CONVERTED TO INCHES (DBH/2.54)
    HT = HT (M) CONVERTED TO FEET (HT/0.3048)
    BA = BASAL AREA (DBH IN INCHES) BA= .005454154 x DBH2
    CVTS = CUBIC FOOT VOLUME, TOTAL STEM, WITH TOP AND STUMP
    TARIF = TARIF NUMBER EQUATION
    CVT = CUBIC FOOT VOLUME ABOVE STUMP
    CV4 = CUBIC FOOT VOLUME, 4-IN TOP
    CV8 = CUBIC FOOT VOLUME, SAWLOG (8-IN TOP)
    """
    eq_number = 33
    
    BA = 0.005454154 * DBH**2
    CVTS = 0.0057821322 * DBH**1.94553 * HT**0.88389
    CV4 = 0.0016380753 * DBH**2.05910 * HT**1.05293
    CV8 = 0.0007741517 * DBH**2.23009 * HT**1.03700
    RTS = 0.9679 - 0.1051 * 0.5523**(DBH - 1.5) # RTS is not defined in the documentation
    CVT = CVTS * RTS #  RTS appears to be proportion of cubic volume in tree above stump
    # CV4X = CVT * (0.99875 - 43.336/DBH**3 - 124.717/DBH**4 + (0.193437*HT)/DBH**3 + 479.83/(DBH**3 * HT)) 
        # this is not used in this set of equations, only in BF calculation and is calculated there
    try:
        TARIF = (CV8 * 0.912733)/((0.983 - 0.983 * 0.65**(DBH-8.6)) * (BA - 0.087266))
    except ZeroDivisionError:
        TARIF = 0.01
    
    # record these values in a dictionary
    metric_dict = {}
    for each_metric in ['CVTS', 'TARIF', 'CV4', 'CVT', 'CV8', 'DBH', 'eq_number', 'HT']:
        metric_dict[each_metric] = eval(each_metric)
    
    # if metric requested by user is a cubic volume metric, return it
    return get_metric(metric_dict, metric, 'HW')


# In[45]:

# EQUATION 34 TANOAK (PILLSBURY (H,D), CHARLES BOLSINGER 1/3/83)

# Pillsbury, Norman H. and Michael L. Kirkley. 1984.  Equations for Total, Wood, and 
# Saw-log Volume for Thirteen California Hardwoods.  PNW Research Note, PNW-414. 
# Pacific Northwest Research Station, Portland Oregon. 52p.

def Eq_34(DBH, HT, metric):
    """
    WHERE
    DBH = DBH(CM) CONVERTED TO INCHES (DBH/2.54)
    HT = HT (M) CONVERTED TO FEET (HT/0.3048)
    BA = BASAL AREA (DBH IN INCHES) BA= .005454154 x DBH2
    CVTS = CUBIC FOOT VOLUME, TOTAL STEM, WITH TOP AND STUMP
    TARIF = TARIF NUMBER EQUATION
    CVT = CUBIC FOOT VOLUME ABOVE STUMP
    CV4 = CUBIC FOOT VOLUME, 4-IN TOP
    CV8 = CUBIC FOOT VOLUME, SAWLOG (8-IN TOP)
    """
    eq_number = 34
    
    if HT > 120:
        HT = 120
        
    BA = 0.005454154 * DBH**2
    CVTS = 0.0058870024 * DBH**1.94165 * HT**0.86562
    CV4 = 0.0005774970 * DBH**2.19576 * HT**1.14078
    CV8 = 0.0002526443 * DBH**2.30949 * HT**1.21069
    RTS = 0.9679 - 0.1051 * 0.5523**(DBH - 1.5) # RTS is not defined in the documentation
    CVT = CVTS * RTS #  RTS appears to be proportion of cubic volume in tree above stump
    # CV4X = CVT * (0.99875 - 43.336/DBH**3 - 124.717/DBH**4 + (0.193437*HT)/DBH**3 + 479.83/(DBH**3 * HT)) 
        # this is not used in this set of equations, only in BF calculation and is calculated there
    try:
        TARIF = (CV8 * 0.912733)/((0.983 - 0.983 * 0.65**(DBH-8.6)) * (BA - 0.087266))
    except ZeroDivisionError:
        TARIF = 0.01
    
    # record these values in a dictionary
    metric_dict = {}
    for each_metric in ['CVTS', 'TARIF', 'CV4', 'CVT', 'CV8', 'DBH', 'eq_number', 'HT']:
        metric_dict[each_metric] = eval(each_metric)
    
    # if metric requested by user is a cubic volume metric, return it
    return get_metric(metric_dict, metric, 'HW')


# In[46]:

# EQUATION 35 CALIF WHITE OAK (PILLSBURY (H,D), CHARLES BOLSINGER 1/3/83)

# Pillsbury, Norman H. and Michael L. Kirkley. 1984.  Equations for Total, Wood, and 
# Saw-log Volume for Thirteen California Hardwoods.  PNW Research Note, PNW-414. 
# Pacific Northwest Research Station, Portland Oregon. 52p.

def Eq_35(DBH, HT, metric):
    """
    WHERE
    DBH = DBH(CM) CONVERTED TO INCHES (DBH/2.54)
    HT = HT (M) CONVERTED TO FEET (HT/0.3048)
    BA = BASAL AREA (DBH IN INCHES) BA= .005454154 x DBH2
    CVTS = CUBIC FOOT VOLUME, TOTAL STEM, WITH TOP AND STUMP
    TARIF = TARIF NUMBER EQUATION
    CVT = CUBIC FOOT VOLUME ABOVE STUMP
    CV4 = CUBIC FOOT VOLUME, 4-IN TOP
    CV8 = CUBIC FOOT VOLUME, SAWLOG (8-IN TOP)
    """
    eq_number = 35
    
    BA = 0.005454154 * DBH**2
    CVTS = 0.0042870077  * DBH**2.33631 * HT**0.74872
    CV4 = 0.0009684363 * DBH**2.39565 * HT**0.98878
    CV8 = 0.0001880044 * DBH**1.87346 * HT**1.62443
    RTS = 0.9679 - 0.1051 * 0.5523**(DBH - 1.5) # RTS is not defined in the documentation
    CVT = CVTS * RTS #  RTS appears to be proportion of cubic volume in tree above stump
    # CV4X = CVT * (0.99875 - 43.336/DBH**3 - 124.717/DBH**4 + (0.193437*HT)/DBH**3 + 479.83/(DBH**3 * HT)) 
        # this is not used in this set of equations, only in BF calculation and is calculated there
    try:
        TARIF = (CV8 * 0.912733)/((0.983 - 0.983 * 0.65**(DBH-8.6)) * (BA - 0.087266))
    except ZeroDivisionError:
        TARIF = 0.01
    
    # record these values in a dictionary
    metric_dict = {}
    for each_metric in ['CVTS', 'TARIF', 'CV4', 'CVT', 'CV8', 'DBH', 'eq_number', 'HT']:
        metric_dict[each_metric] = eval(each_metric)
    
    # if metric requested by user is a cubic volume metric, return it
    return get_metric(metric_dict, metric, 'HW')


# In[47]:

# EQUATION 36 ENGELMANN OAK (PILLSBURY (H,D), CHARLES BOLSINGER 1/3/83)

# Pillsbury, Norman H. and Michael L. Kirkley. 1984.  Equations for Total, Wood, and 
# Saw-log Volume for Thirteen California Hardwoods.  PNW Research Note, PNW-414. 
# Pacific Northwest Research Station, Portland Oregon. 52p.

def Eq_36(DBH, HT, metric):
    """
    WHERE
    DBH = DBH(CM) CONVERTED TO INCHES (DBH/2.54)
    HT = HT (M) CONVERTED TO FEET (HT/0.3048)
    BA = BASAL AREA (DBH IN INCHES) BA= .005454154 x DBH2
    CVTS = CUBIC FOOT VOLUME, TOTAL STEM, WITH TOP AND STUMP
    TARIF = TARIF NUMBER EQUATION
    CVT = CUBIC FOOT VOLUME ABOVE STUMP
    CV4 = CUBIC FOOT VOLUME, 4-IN TOP
    CV8 = CUBIC FOOT VOLUME, SAWLOG (8-IN TOP)
    """
    eq_number = 36
    
    BA = 0.005454154 * DBH**2
    CVTS = 0.0191453191* DBH**2.40248 * HT**0.28060
    CV4 = 0.0053866353 * DBH**2.61268 * HT**0.31103
    CV8 = CV4
    RTS = 0.9679 - 0.1051 * 0.5523**(DBH - 1.5) # RTS is not defined in the documentation
    CVT = CVTS * RTS #  RTS appears to be proportion of cubic volume in tree above stump
    # CV4X = CVT * (0.99875 - 43.336/DBH**3 - 124.717/DBH**4 + (0.193437*HT)/DBH**3 + 479.83/(DBH**3 * HT)) 
        # this is not used in this set of equations, only in BF calculation and is calculated there
    try:
        TARIF = (CV8 * 0.912733)/((0.983 - 0.983 * 0.65**(DBH-8.6)) * (BA - 0.087266))
    except ZeroDivisionError:
        TARIF = 0.01
    
    # record these values in a dictionary
    metric_dict = {}
    for each_metric in ['CVTS', 'TARIF', 'CV4', 'CVT', 'CV8', 'DBH', 'eq_number', 'HT']:
        metric_dict[each_metric] = eval(each_metric)
    
    # if metric requested by user is a cubic volume metric, return it
    return get_metric(metric_dict, metric, 'HW')


# In[48]:

# EQUATION 37 BIGLEAF MAPLE (PILLSBURY (H,D,FC), CHARLES BOLSINGER 1/3/83)

# Pillsbury, Norman H. and Michael L. Kirkley. 1984.  Equations for Total, Wood, and 
# Saw-log Volume for Thirteen California Hardwoods.  PNW Research Note, PNW-414. 
# Pacific Northwest Research Station, Portland Oregon. 52p.

def Eq_37(DBH, HT, metric):
    """
    WHERE
    DBH = DBH(CM) CONVERTED TO INCHES (DBH/2.54)
    HT = HT (M) CONVERTED TO FEET (HT/0.3048)
    BA = BASAL AREA (DBH IN INCHES) BA= .005454154 x DBH2
    FC = HARDWOOD FORM CLASS
        # in the original publication, this is actually noted as
        # IV = an indicator variable (1 = non-merchantable first segment; 10 = merchantable first segment). 
        # based on: "STRAIGHT MERCHANTABLE SECTIONS AT LEAST 8 FEET LONG TO A 9-INCH TOP OUTSIDE BARK"
    CVTS = CUBIC FOOT VOLUME, TOTAL STEM, WITH TOP AND STUMP
    TARIF = TARIF NUMBER EQUATION
    CVT = CUBIC FOOT VOLUME ABOVE STUMP
    CV4 = CUBIC FOOT VOLUME, 4-IN TOP
    CV8 = CUBIC FOOT VOLUME, SAWLOG (8-IN TOP)
    """
    eq_number = 37
    
    BA = 0.005454154 * DBH**2
    CVTS = 0.0101786350 * DBH**2.22462 * HT**0.57561
    CV4 = 0.0034214162 * DBH**2.35347 * HT**0.69586
    
    # no method provided in documentation to calculte FC from DBH and HT
    # using FVS default form classes to estimate diameter at 8 ft above a 1 ft stump
    # linear interpolation between BH (4.5 ft) and 16 ft (where form factor is measured)
    
    # DBH Classes at 16 ft height
    # 0<DBH<11, 11<=DBH<21, 21<=DBH<31, 31<=DBH<41, DBH>=41
    # 86, 86, 84, 82, 82                            # FVS PN Variant, Siuslaw NF, Bigleaf Maple
    # 86, 86, 84, 82, 82                            # FVS PN Variant, Olympic NF, Bigleaf Maple
    # 75, 75, 73, 72, 71                            # FVS WC Variant, Willamette NF, Bigleaf Maple
    # 85, 85, 83, 82, 81                            # FVS WC Variant, Umpqua, Bigleaf Maple
    # 81, 81, 80, 79, 78                            # FVS WC Variant, Rogue River, Bigleaf Maple
    # 84, 84, 82, 81, 80                            # FVS WC Variant, Mt Baker/Snoqualmie, Bigleaf Maple
    # 84, 84, 82, 81, 80                            # FVS WC Variant, Gifford Pinchot NF, Bigleaf Maple
    # 84, 84, 82, 81, 80                            # FVS WC Variant, Mt Hood, Bigleaf Maple
    # 98, 84, 81, 80, 79                            # FVS CA Variant, Rogue River NF, Bigleaf Maple
    # 98, 84, 81, 80, 79                            # FVS CA Variant, Siskiyou NF, Bigleaf Maple
    
    # define form factors for each diameter range
    if DBH <11:
        FF = 84
    elif DBH >= 11 and DBH < 21:
        FF = 84
    elif DBH >= 21 and DBH < 31:
        FF = 82
    elif DBH >= 31 and DBH < 41:
        FF = 81
    elif DBH >= 41:
        FF = 80
    
    FF_9ft = 100 + (FF - 100) * (9 - 4.5)/(16 - 4.5) # calculate form factor at 9 ft above ground by linear interpolation
    diam_9ft = FF_9ft/100.0 * DBH # calculate diameter at 9 ft
    
    # If tree height >= 9 ft and diam_9ft >= 9 in., set Pillsbury FC variable to 10, else 1
    if diam_9ft >= 9 and HT >= 9:
        FC = 10
    else:
        FC = 1
    
    CV8 = 0.0004236332 * DBH**2.10316 * HT**1.08584 * FC**0.40017
    RTS = 0.9679 - 0.1051 * 0.5523**(DBH - 1.5) # RTS is not defined in the documentation
    CVT = CVTS * RTS #  RTS appears to be proportion of cubic volume in tree above stump
    # CV4X = CVT * (0.99875 - 43.336/DBH**3 - 124.717/DBH**4 + (0.193437*HT)/DBH**3 + 479.83/(DBH**3 * HT)) 
        # this is not used in this set of equations, only in BF calculation and is calculated there
    try:
        TARIF = (CV8 * 0.912733)/((0.983 - 0.983 * 0.65**(DBH-8.6)) * (BA - 0.087266))
    except ZeroDivisionError:
        TARIF = 0.01
    
    
    # record these values in a dictionary
    metric_dict = {}
    for each_metric in ['CVTS', 'TARIF', 'CV4', 'CVT', 'CV8', 'DBH', 'eq_number', 'HT']:
        metric_dict[each_metric] = eval(each_metric)
    
    # if metric requested by user is a cubic volume metric, return it
    return get_metric(metric_dict, metric, 'HW')


# In[49]:

# EQUATION 38 CALIF BLACK OAK (PILLSBURY (H,D,FC), CHARLES BOLSINGER 1/3/83)

# Pillsbury, Norman H. and Michael L. Kirkley. 1984.  Equations for Total, Wood, and 
# Saw-log Volume for Thirteen California Hardwoods.  PNW Research Note, PNW-414. 
# Pacific Northwest Research Station, Portland Oregon. 52p.

def Eq_38(DBH, HT, metric):
    """
    WHERE
    DBH = DBH(CM) CONVERTED TO INCHES (DBH/2.54)
    HT = HT (M) CONVERTED TO FEET (HT/0.3048)
    BA = BASAL AREA (DBH IN INCHES) BA= .005454154 x DBH2
    FC = HARDWOOD FORM CLASS
        # in the original publication, this is actually noted as
        # IV = an indicator variable (1 = non-merchantable first segment; 10 = merchantable first segment). 
        # based on: "STRAIGHT MERCHANTABLE SECTIONS AT LEAST 8 FEET LONG TO A 9-INCH TOP OUTSIDE BARK"
    CVTS = CUBIC FOOT VOLUME, TOTAL STEM, WITH TOP AND STUMP
    TARIF = TARIF NUMBER EQUATION
    CVT = CUBIC FOOT VOLUME ABOVE STUMP
    CV4 = CUBIC FOOT VOLUME, 4-IN TOP
    CV8 = CUBIC FOOT VOLUME, SAWLOG (8-IN TOP)
    """
    eq_number = 38
    
    BA = 0.005454154 * DBH**2
    CVTS = 0.0070538108 * DBH**1.97437 * HT**0.85034
    CV4 = 0.0036795695 * DBH**2.12635 * HT**0.83339
    
    # no method provided in documentation to calculte FC from DBH and HT
    # using FVS default form classes to estimate diameter at 8 ft above a 1 ft stump
    # linear interpolation between BH (4.5 ft) and 16 ft (where form factor is measured)
    
    # DBH Classes at 16 ft height
    # 0<DBH<11, 11<=DBH<21, 21<=DBH<31, 31<=DBH<41, DBH>=41
    # 95, 95, 82, 82, 82                            # FVS PN Variant, Siuslaw NF, White Oak/Black Oak
    # 95, 95, 82, 82, 82                            # FVS PN Variant, Olympic NF, White Oak/Black Oak
    # 95, 95, 95, 95, 95                            # FVS WC Variant, Willamette NF, White Oak/Black Oak
    # 95, 95, 95, 95, 95                            # FVS WC Variant, Umpqua, White Oak/Black Oak
    # 89, 89, 89, 89, 89                            # FVS WC Variant, Rogue River, White Oak/Black Oak
    # 95, 95, 95, 95, 95                            # FVS WC Variant, Mt Baker/Snoqualmie, White Oak/Black Oak
    # 95, 95, 95, 95, 95                            # FVS WC Variant, Gifford Pinchot NF, White Oak/Black Oak
    # 95, 95, 95, 95, 95                            # FVS WC Variant, Mt Hood, White Oak/Black Oak
    # 98, 88, 84, 81, 81                            # FVS CA Variant, Rogue River NF, Black Oak
    # 98, 88, 84, 81, 81                            # FVS CA Variant, Siskiyou NF, Black Oak
    
    # define form factors for each diameter range
    if DBH <11:
        FF = 95
    elif DBH >= 11 and DBH < 21:
        FF = 95
    elif DBH >= 21 and DBH < 31:
        FF = 84
    elif DBH >= 31 and DBH < 41:
        FF = 82
    elif DBH >= 41:
        FF = 82
    
    FF_9ft = 100 + (FF - 100) * (9 - 4.5)/(16 - 4.5) # calculate form factor at 9 ft above ground by linear interpolation
    diam_9ft = FF_9ft/100.0 * DBH # calculate diameter at 9 ft
    
    # If tree height >= 9 ft and diam_9ft >= 9 in., set Pillsbury FC variable to 10, else 1
    if diam_9ft >= 9 and HT >= 9:
        FC = 10
    else:
        FC = 1
    
    CV8 = 0.0012478663 * DBH**2.68099 * HT**0.42441 * FC**0.28385
    RTS = 0.9679 - 0.1051 * 0.5523**(DBH - 1.5) # RTS is not defined in the documentation
    CVT = CVTS * RTS #  RTS appears to be proportion of cubic volume in tree above stump
    # CV4X = CVT * (0.99875 - 43.336/DBH**3 - 124.717/DBH**4 + (0.193437*HT)/DBH**3 + 479.83/(DBH**3 * HT)) 
        # this is not used in this set of equations, only in BF calculation and is calculated there
    try:
        TARIF = (CV8 * 0.912733)/((0.983 - 0.983 * 0.65**(DBH-8.6)) * (BA - 0.087266))
    except ZeroDivisionError:
        TARIF = 0.01
    
    # record these values in a dictionary
    metric_dict = {}
    for each_metric in ['CVTS', 'TARIF', 'CV4', 'CVT', 'CV8', 'DBH', 'eq_number', 'HT']:
        metric_dict[each_metric] = eval(each_metric)
    
    # if metric requested by user is a cubic volume metric, return it
    return get_metric(metric_dict, metric, 'HW')


# In[50]:

# EQUATION 39 BLUE OAK (PILLSBURY (H,D,FC), CHARLES BOLSINGER 1/3/83)

# Pillsbury, Norman H. and Michael L. Kirkley. 1984.  Equations for Total, Wood, and 
# Saw-log Volume for Thirteen California Hardwoods.  PNW Research Note, PNW-414. 
# Pacific Northwest Research Station, Portland Oregon. 52p.

def Eq_39(DBH, HT, metric):
    """
    WHERE
    DBH = DBH(CM) CONVERTED TO INCHES (DBH/2.54)
    HT = HT (M) CONVERTED TO FEET (HT/0.3048)
    BA = BASAL AREA (DBH IN INCHES) BA= .005454154 x DBH2
    FC = HARDWOOD FORM CLASS
        # in the original publication, this is actually noted as
        # IV = an indicator variable (1 = non-merchantable first segment; 10 = merchantable first segment). 
        # based on: "STRAIGHT MERCHANTABLE SECTIONS AT LEAST 8 FEET LONG TO A 9-INCH TOP OUTSIDE BARK"
    CVTS = CUBIC FOOT VOLUME, TOTAL STEM, WITH TOP AND STUMP
    TARIF = TARIF NUMBER EQUATION
    CVT = CUBIC FOOT VOLUME ABOVE STUMP
    CV4 = CUBIC FOOT VOLUME, 4-IN TOP
    CV8 = CUBIC FOOT VOLUME, SAWLOG (8-IN TOP)
    """
    eq_number = 39
    
    BA = 0.005454154 * DBH**2
    CVTS = 0.0125103008 * DBH**2.33089 * HT**0.46100
    CV4 = 0.0042324071 * DBH**2.53987 * HT**0.50591
    
    # no method provided in documentation to calculte FC from DBH and HT
    # using FVS default form classes to estimate diameter at 8 ft above a 1 ft stump
    # linear interpolation between BH (4.5 ft) and 16 ft (where form factor is measured)
    
    # DBH Classes at 16 ft height
    # 0<DBH<11, 11<=DBH<21, 21<=DBH<31, 31<=DBH<41, DBH>=41
    # 95, 95, 95, 86, 86                            # FVS CA Variant, Rogue River NF, Blue Oak
    # 95, 95, 86, 82, 82                            # FVS CA Variant, Siskiyou NF, Bllue Oak
    
    # define form factors for each diameter range
    if DBH <11:
        FF = 95
    elif DBH >= 11 and DBH < 21:
        FF = 95
    elif DBH >= 21 and DBH < 31:
        FF = 86
    elif DBH >= 31 and DBH < 41:
        FF = 82
    elif DBH >= 41:
        FF = 82
    
    FF_9ft = 100 + (FF - 100) * (9 - 4.5)/(16 - 4.5) # calculate form factor at 9 ft above ground by linear interpolation
    diam_9ft = FF_9ft/100.0 * DBH # calculate diameter at 9 ft
    
    # If tree height >= 9 ft and diam_9ft >= 9 in., set Pillsbury FC variable to 10, else 1
    if diam_9ft >= 9 and HT >= 9:
        FC = 10
    else:
        FC = 1
    
    CV8 = 0.0036912408 * DBH**1.79732 * HT**0.83884 * FC**0.15958
    RTS = 0.9679 - 0.1051 * 0.5523**(DBH - 1.5) # RTS is not defined in the documentation
    CVT = CVTS * RTS #  RTS appears to be proportion of cubic volume in tree above stump
    # CV4X = CVT * (0.99875 - 43.336/DBH**3 - 124.717/DBH**4 + (0.193437*HT)/DBH**3 + 479.83/(DBH**3 * HT)) 
        # this is not used in this set of equations, only in BF calculation and is calculated there
    try:
        TARIF = (CV8 * 0.912733)/((0.983 - 0.983 * 0.65**(DBH-8.6)) * (BA - 0.087266))
    except ZeroDivisionError:
        TARIF = 0.01
    
    # record these values in a dictionary
    metric_dict = {}
    for each_metric in ['CVTS', 'TARIF', 'CV4', 'CVT', 'CV8', 'DBH', 'eq_number', 'HT']:
        metric_dict[each_metric] = eval(each_metric)
    
    # if metric requested by user is a cubic volume metric, return it
    return get_metric(metric_dict, metric, 'HW')


# In[51]:

# EQUATION 40 PACIFIC MADRONE (PILLSBURY (H,D,FC), CHARLES BOLSINGER 1/3/83)

# Pillsbury, Norman H. and Michael L. Kirkley. 1984.  Equations for Total, Wood, and 
# Saw-log Volume for Thirteen California Hardwoods.  PNW Research Note, PNW-414. 
# Pacific Northwest Research Station, Portland Oregon. 52p.

def Eq_40(DBH, HT, metric):
    """
    WHERE
    DBH = DBH(CM) CONVERTED TO INCHES (DBH/2.54)
    HT = HT (M) CONVERTED TO FEET (HT/0.3048)
    BA = BASAL AREA (DBH IN INCHES) BA= .005454154 x DBH2
    FC = HARDWOOD FORM CLASS
        # in the original publication, this is actually noted as
        # IV = an indicator variable (1 = non-merchantable first segment; 10 = merchantable first segment). 
        # based on: "STRAIGHT MERCHANTABLE SECTIONS AT LEAST 8 FEET LONG TO A 9-INCH TOP OUTSIDE BARK"
    CVTS = CUBIC FOOT VOLUME, TOTAL STEM, WITH TOP AND STUMP
    TARIF = TARIF NUMBER EQUATION
    CVT = CUBIC FOOT VOLUME ABOVE STUMP
    CV4 = CUBIC FOOT VOLUME, 4-IN TOP
    CV8 = CUBIC FOOT VOLUME, SAWLOG (8-IN TOP)
    """
    eq_number = 40
    
    if HT > 120:
        HT = 120
    
    BA = 0.005454154 * DBH**2
    CVTS = 0.0067322665 * DBH**1.96628 * HT**0.83458
    CV4 = 0.0025616425 * DBH**1.99295 * HT**1.01532
    
    # no method provided in documentation to calculte FC from DBH and HT
    # using FVS default form classes to estimate diameter at 8 ft above a 1 ft stump
    # linear interpolation between BH (4.5 ft) and 16 ft (where form factor is measured)
    
    # DBH Classes at 16 ft height
    # 0<DBH<11, 11<=DBH<21, 21<=DBH<31, 31<=DBH<41, DBH>=41
    # 95, 86, 82, 79, 79                            # FVS CA Variant, Rogue River NF, Pacific madrone
    # 98, 88, 84, 81, 81                            # FVS CA Variant, Siskiyou NF, Pacific madrone
    
    # define form factors for each diameter range
    if DBH <11:
        FF = 95
    elif DBH >= 11 and DBH < 21:
        FF = 86
    elif DBH >= 21 and DBH < 31:
        FF = 82
    elif DBH >= 31 and DBH < 41:
        FF = 79
    elif DBH >= 41:
        FF = 79
    
    FF_9ft = 100 + (FF - 100) * (9 - 4.5)/(16 - 4.5) # calculate form factor at 9 ft above ground by linear interpolation
    diam_9ft = FF_9ft/100.0 * DBH # calculate diameter at 9 ft
    
    # If tree height >= 9 ft and diam_9ft >= 9 in., set Pillsbury FC variable to 10, else 1
    if diam_9ft >= 9 and HT >= 9:
        FC = 10
    else:
        FC = 1
    
    CV8 = 0.0006181530 * DBH**1.72635 * HT**1.26462 * FC**0.37868
    RTS = 0.9679 - 0.1051 * 0.5523**(DBH - 1.5) # RTS is not defined in the documentation
    CVT = CVTS * RTS #  RTS appears to be proportion of cubic volume in tree above stump
    # CV4X = CVT * (0.99875 - 43.336/DBH**3 - 124.717/DBH**4 + (0.193437*HT)/DBH**3 + 479.83/(DBH**3 * HT)) 
        # this is not used in this set of equations, only in BF calculation and is calculated there
    try:
        TARIF = (CV8 * 0.912733)/((0.983 - 0.983 * 0.65**(DBH-8.6)) * (BA - 0.087266))
    except ZeroDivisionError:
        TARIF = 0.01
    
    # record these values in a dictionary
    metric_dict = {}
    for each_metric in ['CVTS', 'TARIF', 'CV4', 'CVT', 'CV8', 'DBH', 'eq_number', 'HT']:
        metric_dict[each_metric] = eval(each_metric)
    
    # if metric requested by user is a cubic volume metric, return it
    return get_metric(metric_dict, metric, 'HW')


# In[52]:

# EQUATION 41 ORE WHITE OAK (PILLSBURY (H,D,FC), CHARLES BOLSINGER 1/3/83)

# Pillsbury, Norman H. and Michael L. Kirkley. 1984.  Equations for Total, Wood, and 
# Saw-log Volume for Thirteen California Hardwoods.  PNW Research Note, PNW-414. 
# Pacific Northwest Research Station, Portland Oregon. 52p.

def Eq_41(DBH, HT, metric):
    """
    WHERE
    DBH = DBH(CM) CONVERTED TO INCHES (DBH/2.54)
    HT = HT (M) CONVERTED TO FEET (HT/0.3048)
    BA = BASAL AREA (DBH IN INCHES) BA= .005454154 x DBH2
    FC = HARDWOOD FORM CLASS
        # in the original publication, this is actually noted as
        # IV = an indicator variable (1 = non-merchantable first segment; 10 = merchantable first segment). 
        # based on: "STRAIGHT MERCHANTABLE SECTIONS AT LEAST 8 FEET LONG TO A 9-INCH TOP OUTSIDE BARK"
    CVTS = CUBIC FOOT VOLUME, TOTAL STEM, WITH TOP AND STUMP
    TARIF = TARIF NUMBER EQUATION
    CVT = CUBIC FOOT VOLUME ABOVE STUMP
    CV4 = CUBIC FOOT VOLUME, 4-IN TOP
    CV8 = CUBIC FOOT VOLUME, SAWLOG (8-IN TOP)
    """
    eq_number = 41
    
    BA = 0.005454154 * DBH**2
    CVTS = 0.0072695058 * DBH**2.14321 * HT**0.74220
    CV4 = 0.0024277027 * DBH**2.25575 * HT**0.87108
    
    # no method provided in documentation to calculte FC from DBH and HT
    # using FVS default form classes to estimate diameter at 8 ft above a 1 ft stump
    # linear interpolation between BH (4.5 ft) and 16 ft (where form factor is measured)
    
    # DBH Classes at 16 ft height
    # 0<DBH<11, 11<=DBH<21, 21<=DBH<31, 31<=DBH<41, DBH>=41
    # 95, 95, 82, 82, 82                            # FVS PN Variant, Siuslaw NF, White Oak
    # 95, 95, 82, 82, 82                            # FVS PN Variant, Olympic NF, White Oak
    # 95, 95, 95, 95, 95                            # FVS WC Variant, Willamette NF, White Oak
    # 95, 95, 95, 95, 95                            # FVS WC Variant, Umpqua, White Oak
    # 89, 89, 89, 89, 89                            # FVS WC Variant, Rogue River, White Oak
    # 95, 95, 95, 95, 95                            # FVS WC Variant, Mt Baker/Snoqualmie, White Oak
    # 95, 95, 95, 95, 95                            # FVS WC Variant, Gifford Pinchot NF, White Oak
    # 95, 95, 95, 95, 95                            # FVS WC Variant, Mt Hood, White Oak
    # 89, 89, 89, 89, 89                            # FVS CA Variant, Rogue River NF, White Oak
    # 95, 95, 95, 95, 95                            # FVS CA Variant, Siskiyou NF, White Oak
    
    # define form factors for each diameter range
    if DBH <11:
        FF = 95
    elif DBH >= 11 and DBH < 21:
        FF = 95
    elif DBH >= 21 and DBH < 31:
        FF = 89
    elif DBH >= 31 and DBH < 41:
        FF = 89
    elif DBH >= 41:
        FF = 89
    
    FF_9ft = 100 + (FF - 100) * (9 - 4.5)/(16 - 4.5) # calculate form factor at 9 ft above ground by linear interpolation
    diam_9ft = FF_9ft/100.0 * DBH # calculate diameter at 9 ft
    
    # If tree height >= 9 ft and diam_9ft >= 9 in., set Pillsbury FC variable to 10, else 1
    if diam_9ft >= 9 and HT >= 9:
        FC = 10
    else:
        FC = 1
    
    CV8 = 0.0008281647 * DBH**2.10651 * HT**0.91215 * FC**0.32652
    RTS = 0.9679 - 0.1051 * 0.5523**(DBH - 1.5) # RTS is not defined in the documentation
    CVT = CVTS * RTS #  RTS appears to be proportion of cubic volume in tree above stump
    # CV4X = CVT * (0.99875 - 43.336/DBH**3 - 124.717/DBH**4 + (0.193437*HT)/DBH**3 + 479.83/(DBH**3 * HT)) 
        # this is not used in this set of equations, only in BF calculation and is calculated there
    try:
        TARIF = (CV8 * 0.912733)/((0.983 - 0.983 * 0.65**(DBH-8.6)) * (BA - 0.087266))
    except ZeroDivisionError:
        TARIF = 0.01
    
    # record these values in a dictionary
    metric_dict = {}
    for each_metric in ['CVTS', 'TARIF', 'CV4', 'CVT', 'CV8', 'DBH', 'eq_number', 'HT']:
        metric_dict[each_metric] = eval(each_metric)
    
    # if metric requested by user is a cubic volume metric, return it
    return get_metric(metric_dict, metric, 'HW')


# In[53]:

# EQUATION 42 CANYON LIVE OAK (PILLSBURY (H,D,FC), CHARLES BOLSINGER 1/3/83)

# Pillsbury, Norman H. and Michael L. Kirkley. 1984.  Equations for Total, Wood, and 
# Saw-log Volume for Thirteen California Hardwoods.  PNW Research Note, PNW-414. 
# Pacific Northwest Research Station, Portland Oregon. 52p.

def Eq_42(DBH, HT, metric):
    """
    WHERE
    DBH = DBH(CM) CONVERTED TO INCHES (DBH/2.54)
    HT = HT (M) CONVERTED TO FEET (HT/0.3048)
    BA = BASAL AREA (DBH IN INCHES) BA= .005454154 x DBH2
    FC = HARDWOOD FORM CLASS
        # in the original publication, this is actually noted as
        # IV = an indicator variable (1 = non-merchantable first segment; 10 = merchantable first segment). 
        # based on: "STRAIGHT MERCHANTABLE SECTIONS AT LEAST 8 FEET LONG TO A 9-INCH TOP OUTSIDE BARK"
    CVTS = CUBIC FOOT VOLUME, TOTAL STEM, WITH TOP AND STUMP
    TARIF = TARIF NUMBER EQUATION
    CVT = CUBIC FOOT VOLUME ABOVE STUMP
    CV4 = CUBIC FOOT VOLUME, 4-IN TOP
    CV8 = CUBIC FOOT VOLUME, SAWLOG (8-IN TOP)
    """
    eq_number = 42
    
    BA = 0.005454154 * DBH**2
    CVTS = 0.0097438611 * DBH**2.20527 * HT**0.61190
    CV4 = 0.0031670596 * DBH**2.32519 * HT**0.74348
    
    # no method provided in documentation to calculte FC from DBH and HT
    # using FVS default form classes to estimate diameter at 8 ft above a 1 ft stump
    # linear interpolation between BH (4.5 ft) and 16 ft (where form factor is measured)
    
    # DBH Classes at 16 ft height
    # 0<DBH<11, 11<=DBH<21, 21<=DBH<31, 31<=DBH<41, DBH>=41
    # 94, 94, 85, 80, 80                            # FVS CA Variant, Rogue River NF, Canyon live oak
    # 95, 95, 86, 82, 82                            # FVS CA Variant, Siskiyou NF, Canyon live oak
    
    # define form factors for each diameter range
    if DBH <11:
        FF = 94
    elif DBH >= 11 and DBH < 21:
        FF = 94
    elif DBH >= 21 and DBH < 31:
        FF = 85
    elif DBH >= 31 and DBH < 41:
        FF = 80
    elif DBH >= 41:
        FF = 80
    
    FF_9ft = 100 + (FF - 100) * (9 - 4.5)/(16 - 4.5) # calculate form factor at 9 ft above ground by linear interpolation
    diam_9ft = FF_9ft/100.0 * DBH # calculate diameter at 9 ft
    
    # If tree height >= 9 ft and diam_9ft >= 9 in., set Pillsbury FC variable to 10, else 1
    if diam_9ft >= 9 and HT >= 9:
        FC = 10
    else:
        FC = 1
    
    CV8 = 0.0006540144 * DBH**2.24437 * HT**0.81358 * FC**0.43381
    RTS = 0.9679 - 0.1051 * 0.5523**(DBH - 1.5) # RTS is not defined in the documentation
    CVT = CVTS * RTS #  RTS appears to be proportion of cubic volume in tree above stump
    # CV4X = CVT * (0.99875 - 43.336/DBH**3 - 124.717/DBH**4 + (0.193437*HT)/DBH**3 + 479.83/(DBH**3 * HT)) 
        # this is not used in this set of equations, only in BF calculation and is calculated there
    try:
        TARIF = (CV8 * 0.912733)/((0.983 - 0.983 * 0.65**(DBH-8.6)) * (BA - 0.087266))
    except ZeroDivisionError:
        TARIF = 0.01
    
    # record these values in a dictionary
    metric_dict = {}
    for each_metric in ['CVTS', 'TARIF', 'CV4', 'CVT', 'CV8', 'DBH', 'eq_number', 'HT']:
        metric_dict[each_metric] = eval(each_metric)
    
    # if metric requested by user is a cubic volume metric, return it
    return get_metric(metric_dict, metric, 'HW')


# In[54]:

# EQUATION 43 COAST LIVE OAK (PILLSBURY (H,D,FC), CHARLES BOLSINGER 1/3/83)

# Pillsbury, Norman H. and Michael L. Kirkley. 1984.  Equations for Total, Wood, and 
# Saw-log Volume for Thirteen California Hardwoods.  PNW Research Note, PNW-414. 
# Pacific Northwest Research Station, Portland Oregon. 52p.

def Eq_43(DBH, HT, metric):
    """
    WHERE
    DBH = DBH(CM) CONVERTED TO INCHES (DBH/2.54)
    HT = HT (M) CONVERTED TO FEET (HT/0.3048)
    BA = BASAL AREA (DBH IN INCHES) BA= .005454154 x DBH2
    FC = HARDWOOD FORM CLASS
        # in the original publication, this is actually noted as
        # IV = an indicator variable (1 = non-merchantable first segment; 10 = merchantable first segment). 
        # based on: "STRAIGHT MERCHANTABLE SECTIONS AT LEAST 8 FEET LONG TO A 9-INCH TOP OUTSIDE BARK"
    CVTS = CUBIC FOOT VOLUME, TOTAL STEM, WITH TOP AND STUMP
    TARIF = TARIF NUMBER EQUATION
    CVT = CUBIC FOOT VOLUME ABOVE STUMP
    CV4 = CUBIC FOOT VOLUME, 4-IN TOP
    CV8 = CUBIC FOOT VOLUME, SAWLOG (8-IN TOP)
    """
    eq_number = 43
    
    BA = 0.005454154 * DBH**2
    CVTS = 0.0065261029 * DBH**2.31958 * HT**0.62528
    CV4 = 0.0024574847 * DBH**2.53284 * HT**0.60764
    
    # no method provided in documentation to calculte FC from DBH and HT
    # using FVS default form classes to estimate diameter at 8 ft above a 1 ft stump
    # linear interpolation between BH (4.5 ft) and 16 ft (where form factor is measured)
    
    # DBH Classes at 16 ft height
    # 0<DBH<11, 11<=DBH<21, 21<=DBH<31, 31<=DBH<41, DBH>=41
    # 95, 95, 86, 82, 82                            # FVS CA Variant, Rogue River NF, Coast live oak
    # 95, 95, 95, 95, 95                            # FVS CA Variant, Rogue River NF, California buckeye
    # 95, 95, 86, 82, 82                            # FVS CA Variant, Siskiyou NF, Coast live oak
    # 95, 95, 95, 95, 95                            # FVS CA Variant, Siskiyou NF, California buckeye
    
    # define form factors for each diameter range
    if DBH <11:
        FF = 95
    elif DBH >= 11 and DBH < 21:
        FF = 95
    elif DBH >= 21 and DBH < 31:
        FF = 86
    elif DBH >= 31 and DBH < 41:
        FF = 82
    elif DBH >= 41:
        FF = 82
    
    FF_9ft = 100 + (FF - 100) * (9 - 4.5)/(16 - 4.5) # calculate form factor at 9 ft above ground by linear interpolation
    diam_9ft = FF_9ft/100.0 * DBH # calculate diameter at 9 ft
    
    # If tree height >= 9 ft and diam_9ft >= 9 in., set Pillsbury FC variable to 10, else 1
    if diam_9ft >= 9 and HT >= 9:
        FC = 10
    else:
        FC = 1
    
    CV8 = 0.0006540144 * DBH**2.24437 * HT**0.81358 * FC**0.43381
    RTS = 0.9679 - 0.1051 * 0.5523**(DBH - 1.5) # RTS is not defined in the documentation
    CVT = CVTS * RTS #  RTS appears to be proportion of cubic volume in tree above stump
    # CV4X = CVT * (0.99875 - 43.336/DBH**3 - 124.717/DBH**4 + (0.193437*HT)/DBH**3 + 479.83/(DBH**3 * HT)) 
        # this is not used in this set of equations, only in BF calculation and is calculated there
    try:
        TARIF = (CV8 * 0.912733)/((0.983 - 0.983 * 0.65**(DBH-8.6)) * (BA - 0.087266))
    except ZeroDivisionError:
        TARIF = 0.01
    
    # record these values in a dictionary
    metric_dict = {}
    for each_metric in ['CVTS', 'TARIF', 'CV4', 'CVT', 'CV8', 'DBH', 'eq_number', 'HT']:
        metric_dict[each_metric] = eval(each_metric)
    
    # if metric requested by user is a cubic volume metric, return it
    return get_metric(metric_dict, metric, 'HW')


# In[55]:

# EQUATION 44 INT LIVE OAK (PILLSBURY (H,D,FC), CHARLES BOLSINGER 1/3/83)

# Pillsbury, Norman H. and Michael L. Kirkley. 1984.  Equations for Total, Wood, and 
# Saw-log Volume for Thirteen California Hardwoods.  PNW Research Note, PNW-414. 
# Pacific Northwest Research Station, Portland Oregon. 52p.

def Eq_44(DBH, HT, metric):
    """
    WHERE
    DBH = DBH(CM) CONVERTED TO INCHES (DBH/2.54)
    HT = HT (M) CONVERTED TO FEET (HT/0.3048)
    BA = BASAL AREA (DBH IN INCHES) BA= .005454154 x DBH2
    FC = HARDWOOD FORM CLASS
        # in the original publication, this is actually noted as
        # IV = an indicator variable (1 = non-merchantable first segment; 10 = merchantable first segment). 
        # based on: "STRAIGHT MERCHANTABLE SECTIONS AT LEAST 8 FEET LONG TO A 9-INCH TOP OUTSIDE BARK"
    CVTS = CUBIC FOOT VOLUME, TOTAL STEM, WITH TOP AND STUMP
    TARIF = TARIF NUMBER EQUATION
    CVT = CUBIC FOOT VOLUME ABOVE STUMP
    CV4 = CUBIC FOOT VOLUME, 4-IN TOP
    CV8 = CUBIC FOOT VOLUME, SAWLOG (8-IN TOP)
    """
    eq_number = 44
    
    BA = 0.005454154 * DBH**2
    CVTS = 0.0136818837 * DBH**2.02989 * HT**0.63257
    CV4 = 0.0041192264 * DBH**2.14915 * HT**0.77843
    
    # no method provided in documentation to calculte FC from DBH and HT
    # using FVS default form classes to estimate diameter at 8 ft above a 1 ft stump
    # linear interpolation between BH (4.5 ft) and 16 ft (where form factor is measured)
    
    # DBH Classes at 16 ft height
    # 0<DBH<11, 11<=DBH<21, 21<=DBH<31, 31<=DBH<41, DBH>=41
    # 95, 95, 95, 95, 95                            # FVS CA Variant, Rogue River NF, Interior live oak
    # 95, 95, 95, 95, 95                            # FVS CA Variant, Siskiyou NF, Interior live oak
    
    # define form factors for each diameter range
    FF = 95
    
    FF_9ft = 100 + (FF - 100) * (9 - 4.5)/(16 - 4.5) # calculate form factor at 9 ft above ground by linear interpolation
    diam_9ft = FF_9ft/100.0 * DBH # calculate diameter at 9 ft
    
    # If tree height >= 9 ft and diam_9ft >= 9 in., set Pillsbury FC variable to 10, else 1
    if diam_9ft >= 9 and HT >= 9:
        FC = 10
    else:
        FC = 1
    
    CV8 = 0.0006540144 * DBH**2.24437 * HT**0.81358 * FC**0.43381
    RTS = 0.9679 - 0.1051 * 0.5523**(DBH - 1.5) # RTS is not defined in the documentation
    CVT = CVTS * RTS #  RTS appears to be proportion of cubic volume in tree above stump
    # CV4X = CVT * (0.99875 - 43.336/DBH**3 - 124.717/DBH**4 + (0.193437*HT)/DBH**3 + 479.83/(DBH**3 * HT)) 
        # this is not used in this set of equations, only in BF calculation and is calculated there
    try:
        TARIF = (CV8 * 0.912733)/((0.983 - 0.983 * 0.65**(DBH-8.6)) * (BA - 0.087266))
    except ZeroDivisionError:
        TARIF = 0.01
    
    # record these values in a dictionary
    metric_dict = {}
    for each_metric in ['CVTS', 'TARIF', 'CV4', 'CVT', 'CV8', 'DBH', 'eq_number', 'HT']:
        metric_dict[each_metric] = eval(each_metric)
    
    # if metric requested by user is a cubic volume metric, return it
    return get_metric(metric_dict, metric, 'HW')


# In[56]:

# EQUATION 45 MTN. MAHOGANY (Chojnacky, 1985)

# Chojnacky D.C., 1985.  Pinyon-Juniper Volume Equations for the Central Rocky Mountain States.
# Res. Note INT-339, USDA, Forest Service, Intermountain Res. Station, Ogden, UT 84401.

def Eq_45(DRC, HT, STEMS, metric):
    """
    WHERE:
    VOLUME = cubic foot volume from ground level to a 1.5-inch minimum branch diameter 
        (includes live wood, dead wood, and  bark)
    STEMS = number of stems 3 inches and larger within the first foot above DRC. 
        When STEMS=1 it is a single stemmed tree
    DRC (inches) = Diameter at the root collar 
    HT (feet) =  Total height of the tree
    """
    eq_number = 45
    
    if DRC >=3 and HT >0:
        Factor = DRC * DRC * HT
    
    if STEMS == 1:
        VOLUME = (-0.13363 + (0.128222 * (Factor**(1/3))) + 0.080208)**3
    elif STEMS > 1:
        VOLUME = (-0.13363 + (0.128222 * (Factor**(1/3))))**3 

    if VOLUME <= 0:
        VOLUME = 0.1
    
    # in other equations, CVTS is total cubic volume including top and stump
    # this variable name is used here to maintain consistency with other equations
    CVTS = VOLUME
    
    # record these values in a dictionary
    metric_dict = {}
    for each_metric in ['CVTS']:
        metric_dict[each_metric] = eval(each_metric)
    
    # if metric requested by user is a cubic volume metric, return it
    if metric == 'total_cubic':
        return CVTS
    else:
        try:
            return metric_dict[metric]
        # otherwise try to return a boardfoot volume metric
        except:
            return 0 # no boardfoot volume according to CAR/ARB documentation


# In[57]:

# EQUATION 46 MESQUITE (Chojnacky, 1985)

# Chojnacky D.C., 1985.  Pinyon-Juniper Volume Equations for the Central Rocky Mountain States.
# Res. Note INT-339, USDA, Forest Service, Intermountain Res. Station, Ogden, UT 84401.

def Eq_46(DRC, HT, STEMS, metric):
    """
    WHERE:
    VOLUME = cubic foot volume from ground level to a 1.5-inch minimum branch diameter 
        (includes live wood, dead wood, and  bark)
    STEMS = number of stems 3 inches and larger within the first foot above DRC. 
        When STEMS=1 it is a single stemmed tree
    DRC (inches) = Diameter at the root collar 
    HT (feet) =  Total height of the tree
    """
    eq_number = 46
    
    if DRC >= 3 and HT >0:
        Factor = DRC * DRC * HT
    
    if STEMS > 1:
        if DRC**2 * HT/1000 <= 2:
            VOLUME = 0.020 + 1.8972 * DRC**2 * HT/1000 + 0.5756 * (DRC**2 * HT/1000)**2
        else:
            VOLUME = 6.927 + 1.8972 * DRC**2 * HT/1000 - 9.210/(DRC**2 * HT/1000)
    
    elif STEMS == 1:
        if DRC**2 * HT/1000 <= 2:
            VOLUME = -0.043 + 2.3378 * DRC**2 * HT/1000 + 0.8024 * (DRC**2 * HT/1000)**2
        else:
            VOLUME =  9.586 + 2.3378 * DRC**2 * HT/1000 - 12.839/(DRC**2 * HT/1000)             
    
    if VOLUME <= 0:
        VOLUME = 0.1
    
    # in other equations, CVTS is total cubic volume including top and stump
    # this variable name is used here to maintain consistency with other equations
    CVTS = VOLUME

    # record these values in a dictionary
    metric_dict = {}
    for each_metric in ['CVTS']:
        metric_dict[each_metric] = eval(each_metric)
    
    # if metric requested by user is a cubic volume metric, return it
    if metric == 'total_cubic':
        return CVTS
    else:
        try:
            return metric_dict[metric]
        # otherwise try to return a boardfoot volume metric
        except:
            return 0 # no boardfoot volume according to CAR/ARB documentation


# In[58]:

# For calculating boardfoot volume of softwoods
def SW_BFConversion(DBH, CV4, TARIF, metric):
    """
    Where:
    B4 = BINGO FACTOR
    CUBUS = CUBIC FOOT VOLUME, UPPER-STEM PORTION
    RC6 = RATIO TO CONVERT CUBIC 4-INCH TOP TO CUBIC 6-INCH TOP
    CV6 = CUBIC FOOT VOLUME, 6-INCH TOP (SAWLOG)
    RS616 = RATIO TO CONVERT CUBIC 6-INCH TOP TO SCRIB 6-INCH TOP IN 16-FT LOGS
    RS632 = RATIO TO CONVERT SCRIB 6-INCH TOP IN 16-FT LOGS TO SCRIB 6-INCH TOP IN 32-FT LOGS (WEST-SIDE ONLY)
    SV632 = SCRIBNER VOLUME--6-INCH TOP (IN 32-FT LOGS) (WEST-SIDE ONLY)
    SV616 = SCRIBNER VOLUME--6-INCH TOP (IN 16-FT LOGS)
    RI6 = RATIO TO CONVERT CUBIC 6-INCH TOP TO INTERNATIONAL ¼ INCH 6-INCH TOP
    XINT6 =INTERNATIONAL ¼ INCH VOLUME--6-INCH TOP (IN 16-FT LOGS)
    """
    RC6 = 0.993-(0.993*0.62**(DBH-6.0))
    
    CV6 = RC6 * CV4
    if CV6 > CV4:
        CV6 = CV4
    
    CUBUS = CV4-CV6
    
    #If TARIF <0 then set it to 0.01
    if TARIF < 0.01: # this may occur for small trees (DBH or height) and create a negative logarithm in the equations below
        TARIF = 0.01 # this check was not included in original CAR/ARB equations for softwoods
    
    B4 = TARIF/0.912733
    
    # note that math.log() uses natural logarithm while math.log10() uses log base 10
    RS616L = 0.174439 + 0.117594 * math.log10(DBH) * math.log10(B4) - 8.210585/DBH**2 + 0.236693 * math.log10(B4) - 0.00001345 * (B4**2) - 0.00001937 * DBH**2
    
    RS616 = 10.0**RS616L
    
    RS632 = 1.001491 - 6.924097/TARIF + 0.00001351 * DBH**2
    
    SV616 = RS616 * CV6
    
    SV632 = RS632 * SV616
    
    # NOTE: 
    # West-side Scribner conifer volumes are based on 32 foot logs, 
    # for areas other than western Oregon and western Washington Scribner volumes are based on 16 foot logs 
    
    RI6 = -2.904154 + 3.466328 * math.log10(DBH * TARIF) - 0.02765985 * DBH - 0.00008205 * TARIF**2 + 11.29598/DBH**2
    
    XINT6 = RI6 * CV6
    
    # record these values in a dictionary
    metric_dict = {}
    for each_metric in ['RC6', 'CV6', 'CUBUS', 'B4', 'RS616L', 'RS616', 'RS632','SV616', 'SV632', 'RI6', 'XINT6']:
        metric_dict[each_metric] = eval(each_metric)
    
    # check for general types of metrics
    if metric == 'sawlog_cubic':
        return CV6
    elif metric == 'boardfoot_16ft':
        return SV616
    elif metric == 'boardfoot_32ft':
        return SV632
    
    # or if the user is requesting a specific metric
    else:
        return metric_dict[metric]


# In[59]:

# For calculating boardfoot volume of hardwoods
def HW_BFConversion(CV4, CV8, DBH, eq_number, CVT, TARIF, HT, metric):
    """
    WHERE:
    B4 = BINGO FACTOR
    CUBUS = CUBIC FOOT VOLUME, UPPER-STEM PORTION
    RC6 = RATIO TO CONVERT CUBIC 4-INCH TOP TO CUBIC 6-INCH TOP
    CV6 = CUBIC FOOT VOLUME, 6-INCH TOP (SAWLOG)
    RS616 = RATIO TO CONVERT CUBIC 6-INCH TOP TO SCRIB 6-INCH TOP IN 16-FT LOGS
    SV616 = SCRIBNER VOLUME--6-INCH TOP (IN 16-FT LOGS)
    RS816 = RATIO TO CONVERT CUBIC 6-INCH TOP TO SCRIB 8-INCH TOP IN 16-FT LOGS
    SV816 = SCRIBNER VOLUME--8-INCH TOP (IN 16-FT LOGS)
    XINT6 = INTERNATIONAL ¼ INCH VOLUME--6-INCH TOP (IN 16-FT LOGS)
    RI8 =RATIO TO CONVERT INTERNATIONAL ¼ INCH 6-INCH TOP TO INTERNATIONAL ¼ INCH 8-INCH TOP
    XINT8 = INTERNATIONAL ¼ INCH VOLUME--8-INCH TOP (IN 8-FT LOGS)
    """
    BA = 0.005454154 * DBH**2
    CUBUS = CV4 - CV8
    
    RC6 = 0.993 - 0.993 * 0.62**(DBH-6.0)
    
    # If Hardwood Equation Number is 25-31
    if eq_number >= 25 and eq_number <= 31:
        # THEN set:
        CV4X = CVT
        TARIFX = TARIF
    
    # Otherwise, 
    else:
        # for all other hardwood equation numbers, calculate CV4X and TARIFX as follows:
        CV4X = CVT * (0.99875 - 43.336/DBH**3 - 124.717/DBH**4 + 0.193437*HT/DBH**3 + 479.83/(DBH**3 * HT))
        TARIFX = CV8 * 0.912733 / (0.983 - 0.983 * 0.65**(DBH-8.6) * BA - 0.087266)
        
    #If TARIF or TARIFX are <0 then set them to 0.01
    if TARIF < 0: 
        TARIF = 0.01
    if TARIFX < 0:
        TARIFX = 0.01
    
    CV6 = RC6 * CV4X
    
    B4 = TARIFX/0.912733
    
    # note that math.log() uses natural logarithm while math.log10() uses log base 10
    RS616L = 0.174439 + 0.117594 * math.log10(B4) - 8.210585/DBH**2 + 0.236693 * math.log10(B4) - 0.00001345 * B4**2 - 0.00001937 * DBH**2
    RS616 = 10.0**RS616L
    SV616 = RS616 * CV6
    
    RI6 = -2.904154 + 3.466328 * math.log10(DBH * TARIFX) - 0.02765985 * DBH - 0.00008205 * TARIFX**2 + 11.29598/DBH**2
    XINT6 = RI6 * CV6
    
    RS816 = 0.990 - 0.58 * (0.484**(DBH-9.5))
    SV816 = RS816 * SV616
    
    RI8 = 0.990 - 0.55 * (0.485**(DBH-9.5))
    XINT8 = XINT6 * RI8 
    
    # record these values in a dictionary
    metric_dict = {}
    for each_metric in ['RC6', 'CV6', 'CV8', 'TARIFX', 'CV4X', 'CUBUS', 'B4', 'RS616L', 'RS616', 'SV616', 'RI6','XINT6',
                        'RS816', 'SV816', 'RI8', 'XINT8']:
        metric_dict[each_metric] = eval(each_metric)
    
    # check for general types of metrics
    if metric == 'sawlog_cubic':
        return CV8
    elif metric.startswith('boardfoot'): # and DBH >= 11:
        return SV816
    
    # or if the user is requesting a specific metric
    else:
        return metric_dict[metric]


# In[74]:

# Test Softwood equations
def test_softwoods():
    for eqn in [Eq_1, Eq_2, Eq_3, Eq_4, Eq_5, Eq_6, Eq_7, Eq_8, Eq_9, Eq_10, Eq_11, Eq_12, Eq_13]:
        failed = False
        print(str(eqn.__name__) + "..."),
        for metric in ['CVTS', 'TARIF', 'CV4', 'CVT', 'RC6', 'CV6', 'CUBUS', 'B4', 'RS616L', 'RS616', 'RS632','SV616', 'SV632', 'RI6','XINT6', 'sawlog_cubic', 'total_cubic', 'boardfoot_16ft', 'boardfoot_32ft']:
            try:
                eqn(12,85, metric)
            except:
                failed = True
                print("failed on " + str(metric))
        if not failed:
            print("passed.")

    for eqn in [Eq_14, Eq_141]:
        failed = False
        print(str(eqn.__name__) + "..."),
        for metric in ['CVTS', 'TARIF', 'CV4', 'CVT', 'RC6', 'CV6', 'CUBUS', 'B4', 'RS616L', 'RS616', 'RS632','SV616', 'SV632', 'RI6','XINT6', 'sawlog_cubic', 'total_cubic', 'boardfoot_16ft', 'boardfoot_32ft']:
            try:
                eqn(12,85,1,metric)
            except:
                failed = True
                print("failed on " + str(metric))
        if not failed:
            print("passed.")

    for eqn in [Eq_142, Eq_15, Eq_16, Eq_17, Eq_18, Eq_19, Eq_20, Eq_21, Eq_22, Eq_23, Eq_24]:
        print(str(eqn.__name__) + "..."),
        for metric in ['CVTS', 'TARIF', 'CV4', 'CVT', 'RC6', 'CV6', 'CUBUS', 'B4', 'RS616L', 'RS616', 'RS632','SV616', 'SV632', 'RI6','XINT6', 'sawlog_cubic', 'total_cubic', 'boardfoot_16ft', 'boardfoot_32ft']:
            try:
                eqn(12,85, metric)
            except:
                failed = True
                print("failed on " + str(metric))
                pass
        if not failed:
            print("passed.")


# In[82]:

# # Test Hardwood equations

def test_hardwoods():
    for eqn in [Eq_25, Eq_26, Eq_27, Eq_28, Eq_29, Eq_30, Eq_31, Eq_32, Eq_33, Eq_34, Eq_35, Eq_36, Eq_37, Eq_38, Eq_39, Eq_40, Eq_41, Eq_42, Eq_43, Eq_44, Eq_45, Eq_46]:
        failed = False
        print(str(eqn.__name__) + "..."),
        for metric in ['CVTS', 'TARIF', 'CV4', 'CVT', 'CV8', 'RC6', 'CV6', 'CV8', 'TARIFX', 'CV4X', 'CUBUS', 'B4', 'RS616L', 'RS616', 'SV616', 'RI6','XINT6',
                            'RS816', 'SV816', 'RI8', 'XINT8', 'total_cubic', 'sawlog_cubic', 'boardfoot_16ft']:
            try:
                eqn(12,85, metric)
            except:
                failed = True
                print("failed on " + str(metric))
        if not failed:
            print("passed.")

