"""
Bark Biomass Equations

These equations are required by the California Air Resources Board (ARB) to
calculate tree biomass for forest carbon projects located in California,
Oregon, or Washington.

The equations here were translated from the PDF available on the ARB website:
http://www.arb.ca.gov/cc/capandtrade/protocols/usforest/usforestprojects_2015.htm
These equations here are based on the reported equations from this page as of
May 11, 2016, and downloaded as a PDF
http://www.arb.ca.gov/cc/capandtrade/protocols/usforest/2015/biomass.equations.ca.or.wa.pdf

All equations here calculate biomass of bark in kilograms. To convert to tons
multiply by 0.0011023.

Although only some equations utilize all the variables, all equations accept
dbh, height, and wood density as inputs. These equations should accept
individual scalar values as inputs or arrays of inputs (for many trees).

"""
import numpy as np


class BarkBiomass(object):
    """Base class for bark biomass equations. Each bark biomass equation
    should inherit from this class and override `calc_biomass`.
    """

    def calc_biomass(self, dbh, ht, wood_density=None):
        """Calculates biomass in bark using the original equation."""
        raise NotImplementedError

    def calc(self, dbh, ht, wood_density=None):
        """Calculates biomass in bark, clipping output from original equation
        to prevent negative biomass estimates.

        Parameters
        ----------
        dbh : numeric or array of numerics
          diameter at breast height
        ht : numeric or array of numerics
          total tree height

        Returns
        -------
        biomass : numeric or array of numerics
          estimated biomass in bark
        """
        return (self.calc_biomass(dbh, ht, wood_density=wood_density)
                .clip(0, None))


class BB_1(BarkBiomass):  # BIOPAK EQUATION 379
    def calc_biomass(self, dbh, ht=None, wood_density=None):
        return np.exp(2.1069 + 2.7271 * np.log(dbh))/1000


class BB_2(BarkBiomass):  # BIOPAK EQUATION 887
    def calc_biomass(self, dbh, ht, wood_density=None):
        return 0.6 + 16.4 * (dbh/100)**2 * ht


class BB_3(BarkBiomass):  # BIOPAK EQUATION 917
    def calc_biomass(self, dbh, ht, wood_density=None):
        return 1.0 + 17.2 * (dbh/100)**2 * ht


class BB_4(BarkBiomass):  # BIOPAK EQUATION 382
    def calc_biomass(self, dbh, ht=None, wood_density=None):
        return np.exp(1.47146 + 2.8421 * np.log(dbh))/1000


class BB_5(BarkBiomass):  # BIOPAK EQUATION 251
    def calc_biomass(self, dbh, ht=None, wood_density=None):
        return np.exp(2.79189 + 2.4313 * np.log(dbh))/1000


class BB_6(BarkBiomass):  # BIOPAK EQUATION 845
    def calc_biomass(self, dbh, ht, wood_density=None):
        return 1.3 + 12.6 * (dbh/100)**2 * ht


class BB_7(BarkBiomass):  # BIOPAK EQUATION 875
    def calc_biomass(self, dbh, ht, wood_density=None):
        return 4.5 + 9.3 * (dbh/100)**2 * ht


class BB_8(BarkBiomass):  # BIOPAK EQUATION 5
    def calc_biomass(self, dbh, ht=None, wood_density=None):
        return np.exp(-4.3103 + 2.4300 * np.log(dbh))


class BB_9(BarkBiomass):  # BIOPAK EQUATION 705
    def calc_biomass(self, dbh, ht, wood_density=None):
        return np.exp(-3.6263 + 1.34077 * np.log(dbh) + 0.8567 * np.log(ht))


class BB_10(BarkBiomass):  # BIOPAK EQUATION 391
    def calc_biomass(self, dbh, ht=None, wood_density=None):
        return np.exp(2.183174 + 2.6610 * np.log(dbh))/1000


class BB_11(BarkBiomass):  # BIOPAK EQUATION 899
    def calc_biomass(self, dbh, ht, wood_density=None):
        return 1.2 + 11.2 * (dbh/100)**2 * ht


class BB_12(BarkBiomass):  # BIOPAK EQUATION 385
    def calc_biomass(self, dbh, ht=None, wood_density=None):
        return np.exp(-13.3146 + 2.8594 * np.log(dbh))


class BB_13(BarkBiomass):  # BIOPAK EQUATION 461
    def calc_biomass(self, dbh, ht, wood_density=None):
        return 0.336 + 0.00058 * dbh**2 * ht


class BB_14(BarkBiomass):  # BIOPAK EQUATION 904
    def calc_biomass(self, dbh, ht, wood_density=None):
        return 3.2 + 9.1 * (dbh/100)**2 * ht


class BB_15(BarkBiomass):  # BIOPAK EQUATION 174
    def calc_biomass(self, dbh, ht=None, wood_density=None):
        return np.exp(-4.371 + 2.259 * np.log(dbh))


class BB_16(BarkBiomass):  # BIOPAK EQUATION 54
    def calc_biomass(self, dbh, ht, wood_density=None):
        return np.exp(-10.175 + 2.6333 * np.log(dbh * np.pi))


class BB_17(BarkBiomass):  # BIOPAK EQUATION 394
    def calc_biomass(self, dbh, ht=None, wood_density=None):
        return np.exp(7.189689 + 1.5837 * np.log(dbh))/1000


class BB_18(BarkBiomass):  # BIOPAK EQUATION 942
    def calc_biomass(self, dbh, ht, wood_density=None):
        return 1.3 + 27.6 * (dbh/100)**2 * ht


class BB_19(BarkBiomass):
    def calc_biomass(self, dbh=None, ht=None, wood_density=None):
        return np.zeros_like(dbh)


class BB_20(BarkBiomass):  # BIOPAK EQUATION 275
    def calc_biomass(self, dbh, ht=None, wood_density=None):
        return np.exp(-4.6424 + 2.4617 * np.log(dbh))


class BB_21(BarkBiomass):  # BIOPAK EQUATION 911
    def calc_biomass(self, dbh, ht, wood_density=None):
        return 0.9 + 27.4 * (dbh/100)**2 * ht


class BB_22(BarkBiomass):  # BIOPAK EQUATION 881
    def calc_biomass(self, dbh, ht, wood_density=None):
        return 1.0 + 15.6 * (dbh/100)**2 * ht


class BB_23(BarkBiomass):  # BIOPAK EQUATION 923
    def calc_biomass(self, dbh, ht, wood_density=None):
        return 1.8 + 9.6 * (dbh/100)**2 * ht


class BB_24(BarkBiomass):  # BIOPAK EQUATION 893
    def calc_biomass(self, dbh, ht, wood_density=None):
        return 2.4 + 15.0 * (dbh/100)**2 * ht


class BB_25(BarkBiomass):  # BIOPAK EQUATION 857
    def calc_biomass(self, dbh, ht, wood_density=None):
        return 3.6 + 18.2 * (dbh/100)**2 * ht


class BB_26(BarkBiomass):  # BIOPAK EQUATION 455
    def calc_biomass(self, dbh, ht, wood_density=None):
        return -0.025 + 0.00134 * dbh**2 * ht


class BB_27(BarkBiomass):  # BIOPAK EQUATION 948
    def calc_biomass(self, dbh, ht, wood_density=None):
        return -1.2 + 29.1 * (dbh/100)**2 * ht


class BB_28(BarkBiomass):  # BIOPAK EQUATION 930
    def calc_biomass(self, dbh, ht, wood_density=None):
        return 1.2 + 15.5 * (dbh/100)**2 * ht


class BB_29(BarkBiomass):  # Bigleaf maple
    def calc_biomass(self, dbh, ht, wood_density):
        adbh = (dbh - 0.21235)/0.94782
        outer_vol = 0.0000246916 * (adbh**2.354347 * (ht**0.69586))
        inner_vol = 0.0000246916 * (dbh**2.354347 * (ht**0.69586))
        return (outer_vol - inner_vol) * 35.30 * wood_density/2.2046


class BB_30(BarkBiomass):  # California Black Oak
    def calc_biomass(self, dbh, ht, wood_density):
        adbh = (dbh + 0.68133)/0.95767
        outer_vol = 0.0000386403 * (adbh**2.12635 * (ht**0.83339))
        inner_vol = 0.0000386403 * (dbh**2.12635 * (ht**0.83339))
        return (outer_vol - inner_vol) * 35.30 * wood_density/2.2046


class BB_31(BarkBiomass):  # Canyon Live Oak
    def calc_biomass(self, dbh, ht, wood_density):
        adbh = (dbh + 0.48584)/0.96147
        outer_vol = 0.0000248325 * (adbh**2.32519 * (ht**0.74348))
        inner_vol = 0.0000248325 * (dbh**2.32519 * (ht**0.74348))
        return (outer_vol - inner_vol) * 35.30 * wood_density/2.2046


class BB_32(BarkBiomass):  # Golden Chinkapin
    def calc_biomass(self, dbh, ht, wood_density):
        adbh = (dbh - 0.39534)/0.90182
        outer_vol = 0.000056884 * (adbh**2.07202 * (ht**0.77467))
        inner_vol = 0.000056884 * (dbh**2.07202 * (ht**0.77467))
        return (outer_vol - inner_vol) * 35.30 * wood_density/2.2046


class BB_33(BarkBiomass):  # California Laurel
    def calc_biomass(self, dbh, ht, wood_density):
        adbh = (dbh + 0.32491)/0.96579
        outer_vol = 0.0000237733 * (adbh**2.05910 * (ht**1.05293))
        inner_vol = 0.0000237733 * (dbh**2.05910 * (ht**1.05293))
        return (outer_vol - inner_vol) * 35.30 * wood_density/2.2046


class BB_34(BarkBiomass):  # Pacific Madrone
    def calc_biomass(self, dbh, ht, wood_density):
        adbh = (dbh + 0.03425)/0.98155
        outer_vol = 0.0000378129 * (adbh**1.99295 * (ht**1.01532))
        inner_vol = 0.0000378129 * (dbh**1.99295 * (ht**1.01532))
        return (outer_vol - inner_vol) * 35.30 * wood_density/2.2046


class BB_35(BarkBiomass):  # Oregon White Oak
    def calc_biomass(self, dbh, ht, wood_density):
        adbh = (dbh + 0.78034)/0.95956
        outer_vol = 0.0000236325 * (adbh**2.25575 * (ht**0.87108))
        inner_vol = 0.0000236325 * (dbh**2.25575 * (ht**0.87108))
        return (outer_vol - inner_vol) * 35.30 * wood_density/2.2046


class BB_36(BarkBiomass):  # Tanoak
    def calc_biomass(self, dbh, ht, wood_density):
        adbh = (dbh + 4.1177)/0.95354
        outer_vol = 0.0000081905 * (adbh**2.19576 * (ht**1.14078))
        inner_vol = 0.0000081905 * (dbh**2.19576 * (ht**1.14078))
        return (outer_vol - inner_vol) * 35.30 * wood_density/2.2046


class BB_37(BarkBiomass):  # Blue Oak
    def calc_biomass(self, dbh, ht, wood_density):
        adbh = (dbh + 0.44003)/0.95354
        outer_vol = 0.0000204864 * (adbh**2.53987 * (ht**0.50591))
        inner_vol = 0.0000204864 * (dbh**2.53987 * (ht**0.50591))
        return (outer_vol - inner_vol) * 35.30 * wood_density/2.2046


class BB_38(BarkBiomass):  # BIOPAK EQUATION ???
    def calc_biomass(self, dbh, ht, wood_density=None):
        return 3.3 + 9.0 * (dbh/100)**2 * ht


class BB_39(BarkBiomass):  # BIOPAK EQUATION 936
    def calc_biomass(self, dbh, ht, wood_density=None):
        return -1.2 + 24.0 * (dbh/100)**2 * ht


ALL_EQNS = [
    BB_1, BB_2, BB_3, BB_4, BB_5, BB_6, BB_7, BB_8, BB_9, BB_10,
    BB_11, BB_12, BB_13, BB_14, BB_15, BB_16, BB_17, BB_18, BB_19, BB_20,
    BB_21, BB_22, BB_23, BB_24, BB_25, BB_26, BB_27, BB_28, BB_29, BB_30,
    BB_31, BB_32, BB_33, BB_34, BB_35, BB_36, BB_37, BB_38, BB_39
]
