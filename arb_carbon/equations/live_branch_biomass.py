"""
Live Branch Biomass Equations

These equations are required by the California Air Resources Board (ARB) to
calculate tree biomass for forest carbon projects located in California,
Oregon, or Washington.

The equations here were translated from the PDF available on the ARB website:
http://www.arb.ca.gov/cc/capandtrade/protocols/usforest/usforestprojects_2015.htm
These equations here are based on the reported equations from this page as of
May 11, 2016, and downloaded as a PDF
http://www.arb.ca.gov/cc/capandtrade/protocols/usforest/2015/biomass.equations.ca.or.wa.pdf

All equations here calculate biomass of live tree branches in kilograms. To
convert to tons multiply by 0.0011023.

Although only some equations utilize both variables, all equations accept dbh
and height as inputs. These equations should accept individual scalar values as
inputs or arrays of inputs (for many trees).

"""
import numpy as np


class BranchBiomass(object):
    """Base class for branch biomass equations. Each live branch biomass
    equation should inherit from this class and override `calc_biomass`.
    """

    def calc_biomass(self, dbh, ht):
        """Calculates biomass in live branches using the original equation."""
        raise NotImplementedError

    def calc(self, dbh, ht):
        """Calculates biomass in live branches, clipping output from original
        equation to prevent negative biomass estimates.

        Parameters
        ----------
        dbh : numeric or array of numerics
          diameter at breast height
        ht : numeric or array of numerics
          total tree height

        Returns
        -------
        biomass : numeric or array of numerics
          estimated biomass in live branches
        """
        return self.calc_biomass(dbh, ht).clip(0, None)


class BLB_None(BranchBiomass):  
    def calc_biomass(self, dbh, ht=None):
        return np.zeros_like(dbh)
    
    
class BLB_1(BranchBiomass):  # BIOPAK EQUATION 889
    def calc_biomass(self, dbh, ht):
        return 13.0 + 12.4 * (dbh/100)**2 * ht


class BLB_2(BranchBiomass):  # BIOPAK EQUATION 919
    def calc_biomass(self, dbh, ht):
        return 3.6 + 44.2 * (dbh/100)**2 * ht


class BLB_3(BranchBiomass):  # BIOPAK EQUATION 28
    def calc_biomass(self, dbh, ht=None):
        return np.exp(-4.1817 + 2.3324 * np.log(dbh))


class BLB_4(BranchBiomass):  # BIOPAK EQUATION 877
    def calc_biomass(self, dbh, ht):
        return 16.8 + 14.4 * (dbh/100)**2 * ht


class BLB_5(BranchBiomass):  # BIOPAK EQUATION 847
    def calc_biomass(self, dbh, ht):
        return 9.7 + 22.0 * (dbh/100)**2 * ht


class BLB_6(BranchBiomass):  # BIOPAK EQUATION 2
    def calc_biomass(self, dbh, ht=None):
        return np.exp(-3.6941 + 2.1382 * np.log(dbh))


class BLB_7(BranchBiomass):  # BIOPAK EQUATION 702
    def calc_biomass(self, dbh, ht):
        return np.exp(-4.1068 + 1.5177 * np.log(dbh) + 1.0424 * np.log(ht))


class BLB_8(BranchBiomass):
    def calc_biomass(self, dbh, ht=None):
        return np.exp(-7.637 + 3.3648 * np.log(dbh))


class BLB_9(BranchBiomass):  # BIOPAK EQUATION 901
    def calc_biomass(self, dbh, ht):
        return 9.5 + 16.8 * (dbh/100)**2 * ht


class BLB_10(BranchBiomass):  # BIOPAK EQUATION 459
    def calc_biomass(self, dbh, ht):
        return 0.199 + 0.00381 * dbh**2 * ht


class BLB_11(BranchBiomass):  # BIOPAK EQUATION 907
    def calc_biomass(self, dbh, ht):
        return 7.8 + 12.3 * (dbh/100)**2 * ht


class BLB_12(BranchBiomass):
    def calc_biomass(self, dbh, ht=None):
        return np.exp(-4.570 + 2.271 * np.log(dbh))


class BLB_13(BranchBiomass):  # BIOPAK EQUATION 51
    def calc_biomass(self, dbh, ht=None):
        return np.exp(-7.2775 + 2.3337 * np.log(dbh * np.pi))


class BLB_14(BranchBiomass):  # BIOPAK EQUATION 944
    def calc_biomass(self, dbh, ht):
        return 1.7 + 26.2 * (dbh/100)**2 * ht


class BLB_15(BranchBiomass):  # BIOPAK EQUATION 932
    def calc_biomass(self, dbh, ht):
        return 2.5 + 36.8 * (dbh/100)**2 * ht


class BLB_16(BranchBiomass):
    def calc_biomass(self, dbh, ht=None):
        bf = ((np.exp(-4.5648 + 2.6232 * np.log(dbh)))
              * 1/(2.7638 + 0.062 * dbh**1.3364))
        return np.exp(-4.5648 + 2.6232 * np.log(dbh)) - bf


class BLB_17(BranchBiomass):
    def calc_biomass(self, dbh, ht=None):
        return np.exp(-5.2581 + 2.6045 * np.log(dbh))


class BLB_18(BranchBiomass):  # BIOPAK EQUATION 883
    def calc_biomass(self, dbh, ht):
        return 4.5 + 22.7 * (dbh/100)**2 * ht


class BLB_19(BranchBiomass):  # BIOPAK EQUATION 925
    def calc_biomass(self, dbh, ht):
        return 5.3 + 9.7 * (dbh/100)**2 * ht


class BLB_20(BranchBiomass):  # BIOPAK EQUATION 895
    def calc_biomass(self, dbh, ht):
        return 20.4 + 7.7 * (dbh/100)**2 * ht


class BLB_21(BranchBiomass):  # BIOPAK EQUATION 446
    def calc_biomass(self, dbh, ht):
        return 0.626 + 0.00079 * dbh**2 * ht


class BLB_22(BranchBiomass):  # BIOPAK EQUATION 859
    def calc_biomass(self, dbh, ht):
        return 12.6 + 23.5 * (dbh/100)**2 * ht


class BLB_23(BranchBiomass):  # Weyerhaeuser Co Equation
    def calc_biomass(self, dbh, ht):
        return 0.047 + 0.00413 * dbh**2 * ht


class BLB_24(BranchBiomass):  # BIOPAK EQUATION 913
    def calc_biomass(self, dbh, ht):
        return 4.2 + 17.4 * (dbh/100)**2 * ht


class BLB_25(BranchBiomass):  # BIOPAK EQUATION 950
    def calc_biomass(self, dbh, ht):
        return -0.6 + 45.1 * (dbh/100)**2 * ht


class BLB_26(BranchBiomass):  # BIOPAK EQUATION 938
    def calc_biomass(self, dbh, ht):
        return 8.1 + 21.5 * (dbh/100)**2 * ht


class BLB_27(BranchBiomass):  # Snell et al. 1983, Bigleaf maple
    def calc_biomass(self, dbh, ht=None):
        return (np.exp(4.0543553 + 2.1505 * np.log(dbh))
                * (1 - 1 / (4.6762 + 0.0163 * dbh**2.039))/1000)


class BLB_28(BranchBiomass):  # Snell et al. 1983, Pacific madrone
    def calc_biomass(self, dbh, ht):
        return (np.exp(3.0136553 + 2.4839 * np.log(dbh))
                * (1 - 1 / (1.6013 + 0.1060 * dbh**1.309)) / 1000)


class BLB_29(BranchBiomass):  # Snell et al. 1983, Giant chinkapin
    def calc_biomass(self, dbh, ht):
        return (np.exp(3.1980553 + 2.2699 * np.log(dbh))
                * (1 - 1 / (1.6048 + 0.2979 * dbh**0.6828)) / 1000)


ALL_EQNS = [
    BLB_1, BLB_2, BLB_3, BLB_4, BLB_5, BLB_6, BLB_7, BLB_8, BLB_9, BLB_10,
    BLB_11, BLB_12, BLB_13, BLB_14, BLB_15, BLB_16, BLB_17, BLB_18, BLB_19,
    BLB_20, BLB_21, BLB_22, BLB_23, BLB_24, BLB_25, BLB_26, BLB_27, BLB_28,
    BLB_29
]
