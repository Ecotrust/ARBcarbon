# Tree equations required by the California Air Resources Board (ARB)
# Used to calculate tree biomass for projects located in California, Oregon, or Washington

# These equations were translated from the PDF availabe on the ARB website:
# http://www.arb.ca.gov/cc/capandtrade/protocols/usforest/usforestprojects_2015.htm
# These biomass equations were accessed from this page on May 11, 2016, and downloaded as a PDF
# http://www.arb.ca.gov/cc/capandtrade/protocols/usforest/2015/biomass.equations.ca.or.wa.pdf

import math

# BARK EQUATIONS
# All equations produce Biomass of Bark in Kilograms --- to convert to tons multiply by 0.0011023

# *Log* in the equations is = NATURAL LOG
# note that math.log() uses natural logarithm while math.log10() uses log base 10

# Although only some equations utilize all the variables, all equations below take DBH, HT, and Wood Density as inputs

def BB_None(DBH = None, HT = None, wood_density = None):
    return 0


def BB_1(DBH, HT = None, wood_density = None): # BIOPAK EQUATION 379
    return math.exp(2.1069 + 2.7271 * math.log(DBH))/1000


def BB_2(DBH, HT, wood_density = None): # BIOPAK EQUATION 887
    return 0.6 + 16.4 * (DBH/100)**2 * HT


def BB_3(DBH, HT, wood_density = None): # BIOPAK EQUATION 917
    return 1.0 + 17.2 * (DBH/100)**2 * HT


def BB_4(DBH, HT = None, wood_density = None): # BIOPAK EQUATION 382
    return math.exp(1.47146 + 2.8421 * math.log(DBH))/1000


def BB_5(DBH, HT = None, wood_density = None): # BIOPAK EQUATION 251
    return math.exp(2.79189 +2.4313 * math.log(DBH))/1000


def BB_6(DBH, HT, wood_density = None): # BIOPAK EQUATION 845
    return 1.3 + 12.6 * (DBH/100)**2 * HT


def BB_7(DBH, HT, wood_density = None): # BIOPAK EQUATION 875
    return 4.5 + 9.3 * (DBH/100)**2 * HT


def BB_8(DBH, HT = None, wood_density = None): # BIOPAK EQUATION 5
    return math.exp(-4.3103 + 2.4300 * math.log(DBH))


def BB_9(DBH, HT, wood_density = None): # BIOPAK EQUATION 705
    return math.exp(-3.6263 + 1.34077 * math.log(DBH) + 0.8567 * math.log(HT))


def BB_10(DBH, HT = None, wood_density = None): # BIOPAK EQUATION 391
    return math.exp(2.183174 + 2.6610 * math.log(DBH))/1000


def BB_11(DBH, HT, wood_density = None): # BIOPAK EQUATION 899
    return 1.2 + 11.2 * (DBH/100)**2 * HT


def BB_12(DBH, HT = None, wood_density = None): # BIOPAK EQUATION 385
    return math.exp(-13.3146 + 2.8594 * math.log(DBH)) * 1000


def BB_13(DBH, HT, wood_density = None): # BIOPAK EQUATION 461
    return 0.336 + 0.00058 * DBH**2 * HT


def BB_14(DBH, HT, wood_density = None): # BIOPAK EQUATION 904
    return 3.2 + 9.1 * (DBH/100)**2 * HT


def BB_15(DBH, HT = None, wood_density = None): # BIOPAK EQUATION 174
    return math.exp(-4.371 + 2.259 * math.log(DBH))


def BB_16(DBH, HT, wood_density = None): # BIOPAK EQUATION 54
    return math.exp(-10.175 + 2.6333 * math.log(DBH * math.pi))


def BB_17(DBH, HT = None, wood_density = None): # BIOPAK EQUATION 394
    return math.exp(7.189689 + 1.5837 * math.log(DBH))/1000


def BB_18(DBH, HT, wood_density = None): # BIOPAK EQUATION 942
    return 1.3 + 27.6 * (DBH/100)**2 * HT


def BB_19(DBH = None, HT = None, wood_density = None):
    return 0.0


def BB_20(DBH, HT = None, wood_density = None): # BIOPAK EQUATION 275
    return math.exp(-4.6424 + 2.4617 * math.log(DBH))


def BB_21(DBH, HT, wood_density = None): # BIOPAK EQUATION 911
    return 0.9 + 27.4 * (DBH/100)**2 * HT


def BB_22(DBH, HT, wood_density = None): # BIOPAK EQUATION 881
    return 1.0 + 15.6 * (DBH/100)**2 * HT


def BB_23(DBH, HT, wood_density = None): # BIOPAK EQUATION 923
    return 1.8 + 9.6 * (DBH/100)**2 * HT


def BB_24(DBH, HT, wood_density = None): # BIOPAK EQUATION 893
    return 2.4 + 15.0 * (DBH/100)**2 * HT


def BB_25(DBH, HT, wood_density = None): # BIOPAK EQUATION 857
    return 3.6 + 18.2 * (DBH/100)**2 * HT


def BB_26(DBH, HT, wood_density = None): # BIOPAK EQUATION 455
    return -0.025 + 0.00134 * DBH**2 * HT


def BB_27(DBH, HT, wood_density = None): # BIOPAK EQUATION 948
    return -1.2 + 29.1 * (DBH/100)**2 * HT


def BB_28(DBH, HT, wood_density = None): # BIOPAK EQUATION 930
    return 1.2 + 15.5 * (DBH/100)**2 * HT


def BB_29(DBH, HT, wood_density): # Bigleaf maple
    ADBH = (DBH - 0.21235)/0.94782
    OUTERVOL = 0.0000246916 * (ADBH**2.354347 * (HT**0.69586))
    INNERVOL = 0.0000246916 * (DBH**2.354347 * (HT**0.69586))
    return (OUTERVOL - INNERVOL) * 35.30 * wood_density/2.2046


def BB_30(DBH, HT, wood_density): # California Black Oak
    ADBH = (DBH + 0.68133)/0.95767
    OUTERVOL = 0.0000386403 * (ADBH**2.12635 * (HT**0.83339))
    INNERVOL = 0.0000386403 * (DBH**2.12635 * (HT**0.83339))
    return (OUTERVOL - INNERVOL) * 35.30 * wood_density/2.2046


def BB_31(DBH, HT, wood_density): # Canyon Live Oak
    ADBH = (DBH + 0.48584)/0.96147
    OUTERVOL = 0.0000248325 * (ADBH**2.32519 * (HT**0.74348))
    INNERVOL = 0.0000248325 * (DBH**2.32519 * (HT**0.74348))
    return (OUTERVOL - INNERVOL) * 35.30 * wood_density/2.2046


def BB_32(DBH, HT, wood_density): # Golden Chinkapin
    ADBH = (DBH - 0.39534)/0.90182
    OUTERVOL = 0.000056884 * (ADBH**2.07202 * (HT**0.77467))
    INNERVOL = 0.000056884 * (DBH**2.07202 * (HT**0.77467))
    return (OUTERVOL - INNERVOL) * 35.30 * wood_density/2.2046


def BB_33(DBH, HT, wood_density): # California Laurel
    ADBH = (DBH + 0.32491)/0.96579
    OUTERVOL = 0.0000237733 * (ADBH**2.05910 * (HT**1.05293))
    INNERVOL = 0.0000237733 * (DBH**2.05910 * (HT**1.05293))
    return (OUTERVOL - INNERVOL) * 35.30 * wood_density/2.2046


def BB_34(DBH, HT, wood_density): # Pacific Madrone
    ADBH = (DBH + 0.03425)/0.98155
    OUTERVOL = 0.0000378129 * (ADBH**1.99295 * (HT**1.01532))
    INNERVOL = 0.0000378129 * (DBH**1.99295 * (HT**1.01532))
    return (OUTERVOL - INNERVOL) * 35.30 * wood_density/2.2046


def BB_35(DBH, HT, wood_density): # Oregon White Oak
    ADBH = (DBH + 0.78034)/0.95956
    OUTERVOL = 0.0000236325 * (ADBH**2.25575 * (HT**0.87108))
    INNERVOL = 0.0000236325 * (DBH**2.25575 * (HT**0.87108))
    return (OUTERVOL - INNERVOL) * 35.30 * wood_density/2.2046


def BB_36(DBH, HT, wood_density): # Tanoak
    ADBH = (DBH + 4.1177)/0.95354
    OUTERVOL = 0.0000081905 * (ADBH**2.19576 * (HT**1.14078))
    INNERVOL = 0.0000081905 * (DBH**2.19576 * (HT**1.14078))
    return (OUTERVOL - INNERVOL) * 35.30 * wood_density/2.2046


def BB_37(DBH, HT, wood_density): # Blue Oak
    ADBH = (DBH + 0.44003)/0.95354
    OUTERVOL = 0.0000204864 * (ADBH**2.53987 * (HT**0.50591))
    INNERVOL = 0.0000204864 * (DBH**2.53987 * (HT**0.50591))
    return (OUTERVOL - INNERVOL) * 35.30 * wood_density/2.2046


def BB_38(DBH, HT, wood_density): # BIOPAK EQUATION ???
    return 3.3 + 9.0 * (DBH/100)**2 * HT


def BB_39(DBH, HT, wood_density): # BIOPAK EQUATION 936
    return -1.2 + 24.0 * (DBH/100)**2 * HT


# LIVE BRANCH BIOMASS EQUATIONS
# All equations produce Biomass of Live Branches in Kilograms --- to convert to tons multiply by 0.0011023

# *Log* in the equations is = NATURAL LOG
# note that math.log() uses natural logarithm while math.log10() uses log base 10

# Although only some equations utilize both DBH and HT, all equations include both as inputs


def BLB_None(DBH = None, HT = None):
    return 0


def BLB_1(DBH, HT): # BIOPAK EQUATION 889
    return 13.0 + 12.4 * (DBH/100)**2 * HT


def BLB_2(DBH, HT): # BIOPAK EQUATION 919
    return 3.6 + 44.2 * (DBH/100)**2 * HT


def BLB_3(DBH, HT = None): # BIOPAK EQUATION 28
    return math.exp(-4.1817 + 2.3324 * math.log(DBH))


def BLB_4(DBH, HT): # BIOPAK EQUATION 877
    return 16.8 + 14.4 * (DBH/100)**2 * HT


def BLB_5(DBH, HT): # BIOPAK EQUATION 847
    return 9.7 + 22.0 * (DBH/100)**2 * HT


def BLB_6(DBH, HT = None): # BIOPAK EQUATION 2
    return math.exp(-3.6941 + 2.1382 * math.log(DBH))


def BLB_7(DBH, HT): # BIOPAK EQUATION 702
    return math.exp(-4.1068 + 1.5177 * math.log(DBH) + 1.0424 * math.log(HT))


def BLB_8(DBH, HT = None):
    return math.exp(-7.637 + 3.3648 * math.log(DBH))


def BLB_9(DBH, HT): # BIOPAK EQUATION 901
    return 9.5 + 16.8 * (DBH/100)**2 * HT


def BLB_10(DBH, HT): # BIOPAK EQUATION 459
    return 0.199 + 0.00381 * DBH**2 * HT


def BLB_11(DBH, HT): # BIOPAK EQUATION 907
    return 7.8 + 12.3 * (DBH/100)**2 * HT


def BLB_12(DBH, HT = None):
    return math.exp(-4.570 + 2.271 * math.log(DBH))


def BLB_13(DBH, HT = None): # BIOPAK EQUATION 51
    return math.exp(-7.2775 + 2.3337 * math.log(DBH * math.pi))


def BLB_14(DBH, HT): # BIOPAK EQUATION 944
    return 1.7 + 26.2 * (DBH/100)**2 * HT


def BLB_15(DBH, HT): # BIOPAK EQUATION 932
    return 2.5 + 36.8 * (DBH/100)**2 * HT


def BLB_16(DBH, HT = None):
    BF = (math.exp(-4.5648 + 2.6232 * math.log(DBH))) * 1/(2.7638 + 0.062 * DBH**1.3364)
    return math.exp(-4.5648 + 2.6232 * math.log(DBH)) - BF


def BLB_17(DBH, HT = None):
    return math.exp(-5.2581 + 2.6045 * math.log(DBH))


def BLB_18(DBH, HT): # BIOPAK EQUATION 883
    return 4.5 + 22.7 * (DBH/100)**2 * HT


def BLB_19(DBH, HT): # BIOPAK EQUATION 925
    return 5.3 + 9.7 * (DBH/100)**2 * HT


def BLB_20(DBH, HT): # BIOPAK EQUATION 895
    return 20.4 + 7.7 * (DBH/100)**2 * HT


def BLB_21(DBH, HT): # BIOPAK EQUATION 446
    return 0.626 + 0.00079 * DBH**2 * HT


def BLB_22(DBH, HT): # BIOPAK EQUATION 859
    return 12.6 + 23.5 * (DBH/100)**2 * HT


def BLB_23(DBH, HT): # Weyerhaeuser Co Equation
    return 0.047 + 0.00413 * DBH**2 * HT


def BLB_24(DBH, HT): # BIOPAK EQUATION 913
    return 4.2 + 17.4 * (DBH/100)**2 * HT


def BLB_25(DBH, HT): # BIOPAK EQUATION 950
    return -0.6 + 45.1 * (DBH/100)**2 * HT


def BLB_26(DBH, HT): # BIOPAK EQUATION 938
    return 8.1 + 21.5 * (DBH/100)**2 * HT


def BLB_27(DBH, HT = None): # Snell et al. 1983, Bigleaf maple
    return math.exp(4.0543553 + 2.1505 * math.log(DBH))*(1-1/(4.6762 + 0.0163 * DBH**2.039))/1000


def BLB_28(DBH, HT): # Snell et al. 1983, Pacific madrone
    return math.exp(3.0136553 + 2.4839 * math.log(DBH))*(1-1/(1.6013 + 0.1060 * DBH**1.309))/1000


def BLB_29(DBH, HT): # Snell et al. 1983, Giant chinkapin
    return math.exp(3.1980553 + 2.2699 * math.log(DBH))*(1-1/(1.6048 + 0.2979 * DBH**0.6828))/1000


def check_BB(DBH = None, HT = None, wood_density = None, BB_eqn = BB_None):
    '''
    catches zeroes in DBH or HT that will cause a math error when attempting to take the log
    '''
    if DBH <= 0 or HT <=0:
        return 0
    else:
        return BB_eqn(DBH, HT, wood_density)


def check_BLB(DBH = None, HT = None, BLB_eqn = BLB_None):
    '''
    catches zeroes in DBH or HT that will cause a math error when attempting to take the log
    '''
    if DBH <= 0 or HT <=0:
        return 0
    else:
        return BLB_eqn(DBH, HT)



def cairns(aboveground_biomass):
    '''
    Calculates belowground biomass as a function of aboveground biomass.
    Derived from "Equation 1" in Cairns, Brown, Helmer & Baumgardner (1997), available online at
    http://www.arb.ca.gov/cc/capandtrade/protocols/usforest/references/cairns1997.pdf
    Aboveground biomass expected in units of kg, and returns units of kg.
    '''
    if aboveground_biomass <= 0:
        return 0
    else:
        return math.exp(-1.085 +  0.9256 * math.log(aboveground_biomass)) # note that math.log is natural log
