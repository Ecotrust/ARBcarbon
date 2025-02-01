"""Allometric equations required by the California Air Resources Board (ARB) to
calculate tree volumes for forest carbon projects located in California,
Oregon, or Washington

These equations were described in a PDF on the ARB website:
http://www.arb.ca.gov/cc/capandtrade/protocols/usforest/usforestprojects_2015.htm
These volume equations were accessed on May 11, 2016, and downloaded as a PDF:
http://www.arb.ca.gov/cc/capandtrade/protocols/usforest/2015/volume.equations.ca.or.wa.pdf

The functions in this module have been adapted from the original equation forms
to employ vectorized computation for faster execution when processing large
sets of trees. Non-vectorized versions are retained for comparative and testing
purposes.
"""
import numpy as np


class VolumeEquation(object):
    """A generic template for tree volume equations. Specific volume equations
    should be implemented as child classes, and have any formulas defined as
    methods for that class.
    """

    # TARIF NUMBER
    def calc_tarif(self, dbh, ht):
        """Tarif number is the cubic foot volume of a tree with a basal area of
        1 square foot and a given height. Trees with lots of taper have low
        tarif numbers; trees with high tarif numbers have a minimum of taper.
        """
        raise NotImplementedError(
            'This calculation is not implemented for this species.')

    # CUBIC VOLUME METRICS
    def calc_cvts(self, dbh, ht):
        """Cubic foot volume, including tree top and stump.

        Parameters
        ----------
        dbh : numeric or array of numerics
          diameter at breast height, in inches
        ht : numeric or array of numerics
          total tree height, in feet
        """
        raise NotImplementedError(
            'This calculation is not implemented for this species.')

    def calc_cvt(self, dbh, ht):
        """Cubic foot volume above stump, including top.

        Parameters
        ----------
        dbh : numeric or array of numerics
          diameter at breast height, in inches
        ht : numeric or array of numerics
          total tree height, in feet
        """
        raise NotImplementedError(
            'This calculation is not implemented for this species.')

    def calc_cv4(self, dbh, ht):
        """Cubic foot volume above stump, to 4-inch top.

        Parameters
        ----------
        dbh : numeric or array of numerics
          diameter at breast height, in inches
        ht : numeric or array of numerics
          total tree height, in feet
        """
        raise NotImplementedError(
            'This calculation is not implemented for this species.')

    def calc_cv6(self, dbh, ht):
        """Cubic foot volume, to 6-inch top (sawlog).

        Parameters
        ----------
        dbh : numeric or array of numerics
          diameter at breast height, in inches
        ht : numeric or array of numerics
          total tree height, in feet
        """
        raise NotImplementedError(
            'This calculation is not implemented for this species.')

    def calc_cv8(self, dbh, ht):
        """Cubic foot volume, to 8-inch top (sawlog).

        Parameters
        ----------
        dbh : numeric or array of numerics
          diameter at breast height, in inches
        ht : numeric or array of numerics
          total tree height, in feet
        """
        raise NotImplementedError(
            'This calculation is not implemented for this species.')

    # BOARDFOOT VOLUME METRICS
    def calc_sv616(self, dbh, ht):
        """Scribner boardfoot volume to 6-inch top with 16-foot logs.

        Parameters
        ----------
        dbh : numeric or array of numerics
          diameter at breast height, in inches
        ht : numeric or array of numerics
          total tree height, in feet
        """
        raise NotImplementedError(
            'This calculation is not implemented for this species.')

    def calc_sv632(self, dbh, ht):
        """Scribner boardfoot volume to 6-inch top with 32-foot logs.

        Parameters
        ----------
        dbh : numeric or array of numerics
          diameter at breast height, in inches
        ht : numeric or array of numerics
          total tree height, in feet
        """
        raise NotImplementedError(
            'This calculation is not implemented for this species.')

    def calc_xint6(self, dbh, ht):
        """International 1/4-inch boardfoot volume to 6-inch top with 16-foot
        logs.

        Parameters
        ----------
        dbh : numeric or array of numerics
          diameter at breast height, in inches
        ht : numeric or array of numerics
          total tree height, in feet
        """
        raise NotImplementedError(
            'This calculation is not implemented for this species.')

    def calc_sv816(self, dbh, ht):
        """Scribner boardfoot volume to 8-inch top with 16-foot logs.

        Parameters
        ----------
        dbh : numeric or array of numerics
          diameter at breast height, in inches
        ht : numeric or array of numerics
          total tree height, in feet
        """
        raise NotImplementedError(
            'This calculation is not implemented for this species.')

    def calc_xint8(self, dbh, ht):
        """International 1/4-inch boardfoot volume to 8-inch top with 8-foot
        logs.

        Parameters
        ----------
        dbh : numeric or array of numerics
          diameter at breast height, in inches
        ht : numeric or array of numerics
          total tree height, in feet
        """
        raise NotImplementedError(
            'This calculation is not implemented for this species.')

    def calc_vol(self, dbh, ht, metric='CVTS'):
        """Calculates volume (or tarif number) for a user-specified volume
        metric.

        Parameters
        ----------
        dbh : numeric or array of numerics
          diameter at breast height, in inches
        ht : numeric or array of numerics
          total tree height, in feet
        metric : str
          volume metric to calculate

        Available options for metric are:
        ======  ============
        Metric  Description
        ======  ============
        CVTS    Cubic foot volume, including top and stump
        CVT     Cubic foot volume above stump
        CV4     Cubic foot volume above stump to 4-inch top
        CV6     Cubic foot volume above stump to 6-inch top
        CV8     Cubic foot volume above stump to 8-inch top
        TARIF   Tarif number
        SV616   Scribner boardfoot volume to 6-inch top with 16-foot logs
        SV632   Scribner boardfoot volume to 6-inch top with 32-foot logs
        SV816   Scribner boardfoot volume to 8-inch top with 16-foot logs
        XINT6   International 1/4-inch boardfoot volume to 6-inch top with
                16-foot logs
        XINT8   International 1/4-inch boardfoot volume to 8-inch top with
                16-foot logs
        ======  ============
        """
        AVAILABLE_METRICS = [
            'CVTS', 'TARIF', 'CVT', 'CV4', 'CV6', 'CV8', 'SV616', 'SV816',
            'SV632', 'XINT6', 'XINT8'
        ]
        metric = metric.upper()
        if metric not in AVAILABLE_METRICS:
            raise ValueError(
                "Unrecognized metric provided. Must be one of: {}".format(
                    ', '.join(AVAILABLE_METRICS)))

        dbh = np.atleast_1d(dbh)
        ht = np.atleast_1d(ht)

        if metric == 'CVTS':
            return self.calc_cvts(dbh, ht)
        elif metric == 'TARIF':
            return self.calc_tarif(dbh, ht)
        elif metric == 'CVT':
            return self.calc_cvt(dbh, ht)
        elif metric == 'CV4':
            return self.calc_cv4(dbh, ht)
        elif metric == 'CV6':
            return self.calc_cv6(dbh, ht)
        elif metric == 'CV8':
            return self.calc_cv8(dbh, ht)
        elif metric == 'SV616':
            return self.calc_sv616(dbh, ht)
        elif metric == 'SV816':
            return self.calc_sv816(dbh, ht)
        elif metric == 'SV632':
            return self.calc_sv632(dbh, ht)
        elif metric == 'XINT6':
            return self.calc_xint6(dbh, ht)
        elif metric == 'XINT8':
            return self.calc_xint8(dbh, ht)


class SoftwoodVolumeEquation(VolumeEquation):
    def calc_cv6(self, dbh, ht):
        rc6 = 0.993 - (0.993 * 0.62**(dbh - 6.0))
        cv4 = self.calc_cv4(dbh, ht)

        cv6 = np.where((rc6 * cv4) > cv4, cv4, rc6 * cv4)
        cv6[np.logical_or(dbh < 9, ht <= 0)] = 0

        return cv6

    def calc_sv616(self, dbh, ht):
        cv6 = self.calc_cv6(dbh, ht)
        tarif = self.calc_tarif(dbh, ht)
        tarif = np.clip(tarif, 0.01, None)

        b4 = tarif / 0.912733
        rs616l = 0.174439 + 0.117594 * np.log10(dbh) * np.log10(
            b4) - 8.210585 / dbh**2 + 0.236693 * np.log10(b4) - 0.00001345 * (
                b4**2) - 0.00001937 * dbh**2
        rs616 = 10.0**rs616l

        sv616 = np.clip(rs616 * cv6, 0, None)
        sv616[np.logical_or(dbh < 9, ht <= 0)] = 0

        return sv616

    def calc_sv632(self, dbh, ht):
        tarif = self.calc_tarif(dbh, ht)
        tarif = np.clip(tarif, 0.01, None)
        sv616 = self.calc_sv616(dbh, ht)

        rs632 = 1.001491 - 6.924097 / tarif + 0.00001351 * dbh**2
        sv632 = np.clip(rs632 * sv616, 0, None)
        sv632[np.logical_or(dbh < 9, ht <= 0)] = 0

        return sv632

    def calc_xint6(self, dbh, ht):
        tarif = self.calc_tarif(dbh, ht)
        cv6 = self.calc_cv6(dbh, ht)

        ri6 = -2.904154 + 3.466328 * np.log10(
            dbh * tarif
        ) - 0.02765985 * dbh - 0.00008205 * tarif**2 + 11.29598 / dbh**2
        xint6 = np.clip(ri6 * cv6, 0, None)
        xint6[np.logical_or(dbh < 9, ht <= 0)] = 0

        return xint6


class HardwoodVolumeEquation(VolumeEquation):
    def calc_tarifx(self, dbh, ht):
        raise NotImplementedError(
            'This calculation is not implemented for this species.')

    def calc_cv4x(self, dbh, ht):
        raise NotImplementedError(
            'This calculation is not implemented for this species.')

    def calc_cv6(self, dbh, ht):
        cv4x = self.calc_cv4x(dbh, ht)

        rc6 = 0.993 - 0.993 * 0.62**(dbh - 6.0)
        cv6 = np.clip(rc6 * cv4x, 0, None)
        cv6[np.logical_or(dbh < 9, ht <= 0)] = 0

        return cv6

    def calc_sv616(self, dbh, ht):
        tarifx = self.calc_tarifx(dbh, ht)
        cv6 = self.calc_cv6(dbh, ht)
        b4 = tarifx / 0.912733

        rs616l = 0.174439 + 0.117594 * np.log10(
            b4) - 8.210585 / dbh**2 + 0.236693 * np.log10(
                b4) - 0.00001345 * b4**2 - 0.00001937 * dbh**2
        rs616 = 10.0**rs616l
        sv616 = np.clip(rs616 * cv6, 0, None)
        sv616[np.logical_or(dbh < 9, ht <= 0)] = 0

        return sv616

    def calc_sv816(self, dbh, ht):
        sv616 = self.calc_sv616(dbh, ht)

        rs816 = 0.990 - 0.58 * (0.484**(dbh - 9.5))
        sv816 = np.clip(rs816 * sv616, 0, None)
        sv816[np.logical_or(dbh < 11, ht <= 0)] = 0

        return sv816

    def calc_xint6(self, dbh, ht):
        tarifx = self.calc_tarifx(dbh, ht)
        cv6 = self.calc_cv6(dbh, ht)

        ri6 = -2.904154 + 3.466328 * np.log10(
            dbh * tarifx
        ) - 0.02765985 * dbh - 0.00008205 * tarifx**2 + 11.29598 / dbh**2
        xint6 = np.clip(ri6 * cv6, 0, None)
        xint6[np.logical_or(dbh < 9, ht <= 0)] = 0

        return xint6

    def calc_xint8(self, dbh, ht):
        xint6 = self.calc_xint6(dbh, ht)

        ri8 = 0.990 - 0.55 * (0.485**(dbh - 9.5))
        xint8 = np.clip(xint6 * ri8, 0, None)
        xint8[np.logical_or(dbh < 11, ht <= 0)] = 0

        return xint8


class HardwoodVolumeEquation_NoX(HardwoodVolumeEquation):
    def calc_cv4x(self, dbh, ht):
        cvt = self.calc_cvt(dbh, ht)
        cv4x = cvt * (0.99875 - 43.336 / dbh**3 - 124.717 / dbh**4
                      + 0.193437 * ht / dbh**3 + 479.83 / (dbh**3 * ht))
        return cv4x

    def calc_tarifx(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        cv8 = self.calc_cv8(dbh, ht)

        tarifx = cv8 * 0.912733 / (0.983 - 0.983 * 0.65**(dbh - 8.6) * ba
                                   - 0.087266)

        return tarifx


class HardwoodVolumeEquation_WithX(HardwoodVolumeEquation):
    def calc_cv4x(self, dbh, ht):
        return self.calc_cvt(dbh, ht)

    def calc_tarifx(self, dbh, ht):
        return self.calc_tarif(dbh, ht)


class Eq_1(SoftwoodVolumeEquation):
    """Douglas-fir (WEYERHAUSER-DNR RPT #24, 1977)

    Brackett, M. 1973. Notes on tarif tree volume computation. Res. Management
    Report 24. WA Dept. of Nat. Resources. Olympia. 26p.

    Brackett, Michael. 1977. Notes on tarif tree-volume computation. DNR
    report #24. State of Washington, Department of Natural Resources, Olympia,
    WA. 132p.
    """

    def calc_cvts(self, dbh, ht):
        cvtsl = -3.21809 + 0.04948 * np.log10(ht) * np.log10(dbh) - 0.15664 * (
            np.log10(dbh))**2 + 2.02132 * np.log10(dbh) + 1.63408 * np.log10(
                ht) - 0.16185 * (np.log10(ht))**2

        cvts = 10**cvtsl
        cvts[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvts

    def calc_tarif(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        cvts = self.calc_cvts(dbh, ht)

        tarif = (cvts * 0.912733) / (
            (1.033 * (1.0 + 1.382937 * np.exp(-4.105292 * (dbh / 10.0))))
            * (ba + 0.087266) - 0.174533)
        tarif[np.logical_or(dbh <= 0, ht <= 0)] = 0

        return tarif

    def calc_cv4(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        tarif = self.calc_tarif(dbh, ht)

        cv4 = tarif * (ba - 0.087266) / 0.912733
        cv4[np.logical_or(dbh < 5, ht <= 0)] = 0

        return cv4

    def calc_cvt(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        tarif = self.calc_tarif(dbh, ht)

        cvt = tarif * (0.9679 - 0.1051 * 0.5523**(dbh - 1.5)) * (
            (1.033 * (1.0 + 1.382937 * np.exp(-4.015292 * (dbh / 10.0))))
            * (ba + 0.087266) - 0.174533) / 0.912733
        cvt[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvt


class Eq_2(SoftwoodVolumeEquation):
    """Douglas-fir (DNR MEMO--SUMMERFIELD, 11/7/80)

    Summerfield, Edward. 1980. In-house memo describing equations for
    Douglas-fir and ponderosa pine. State of Washington, Department of Natural
    Resources. On file with the PNW Research Station.
    """

    def calc_cvts(self, dbh, ht):
        cvtsl = -6.110493 + 1.81306 * np.log(dbh) + 1.083884 * np.log(ht)

        cvts = np.exp(cvtsl)
        cvts[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvts

    def calc_tarif(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        cvts = self.calc_cvts(dbh, ht)

        tarif = (cvts * 0.912733) / (
            (1.033 * (1.0 + 1.382937 * np.exp(-4.105292 * (dbh / 10.0))))
            * (ba + 0.087266) - 0.174533)
        tarif[np.logical_or(dbh <= 0, ht <= 0)] = 0

        return tarif

    def calc_cv4(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        tarif = self.calc_tarif(dbh, ht)

        cv4 = tarif * (ba - 0.087266) / 0.912733
        cv4[np.logical_or(dbh < 5, ht <= 0)] = 0

        return cv4

    def calc_cvt(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        tarif = self.calc_tarif(dbh, ht)

        cvt = tarif * (0.9679 - 0.1051 * 0.5523**(dbh - 1.5)) * (
            (1.033 * (1.0 + 1.382937 * np.exp(-4.015292 * (dbh / 10.0))))
            * (ba + 0.087266) - 0.174533) / 0.912733
        cvt[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvt


class Eq_3(SoftwoodVolumeEquation):
    """Douglas-fir (USDA-FS RES NOTE PNW-266)

    MacLean, Colin and John M. Berger. 1976. Softwood tree-volume equations
    for major California species. PNW Research Note, PNW-266. Pacific Northwest
    Forest and Range Experiment Station, Portland Oregon. 34p.
    """

    def calc_cvts(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        term = ((1.033 * (1.0 + 1.382937 * np.exp(-4.015292 * (dbh / 10.0))))
                * (ba + 0.087266) - 0.174533)
        tarif = self.calc_tarif(dbh, ht)
        cv4 = self.calc_cv4(dbh, ht)

        cvts = np.where(dbh < 6.0, tarif * term,
                        (cv4 * term) / (ba - 0.087266))
        cvts[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvts

    def calc_tarif(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        dbh_tmp = np.full(np.asanyarray(dbh).shape,
                          fill_value=6.0,
                          dtype=float)
        ba_tmp = 0.005454154 * (dbh_tmp**2)

        cf4 = 0.248569 + 0.0253524 * (ht / dbh) - 0.0000560175 * (ht**2 / dbh)
        cf4 = np.clip(cf4, 0.3, 0.4)

        cf4_tmp = 0.248569 + 0.0253524 * (ht / dbh_tmp) - 0.0000560175 * (
            ht**2 / dbh_tmp)
        cf4_tmp = np.clip(cf4_tmp, 0.3, 0.4)

        cv4 = self.calc_cv4(dbh, ht)
        cv4_tmp = self.calc_cv4(dbh_tmp, ht)

        tarif_tmp = np.clip((cv4_tmp * 0.912733) / (ba_tmp - 0.087266), 0.01,
                            None)

        tarif = np.where(
            dbh < 6.0,
            tarif_tmp * (0.5 * (dbh_tmp - dbh)**2 + (1.0 + 0.063
                                                     * (dbh_tmp - dbh)**2)),
            (cv4 * 0.912733) / (ba - 0.087266))
        tarif = np.clip(tarif, 0.01, None)
        tarif[np.logical_or(dbh <= 0, ht <= 0)] = 0

        return tarif

    def calc_cv4(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)

        cf4 = 0.248569 + 0.0253524 * (ht / dbh) - 0.0000560175 * (ht**2 / dbh)
        cf4 = np.clip(cf4, 0.3, 0.4)

        cv4 = cf4 * ba * ht
        cv4 = np.where(dbh < 5.0, 0, cv4)
        cv4[np.logical_or(dbh < 5, ht <= 0)] = 0

        return cv4

    def calc_cvt(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        term = ((1.033 * (1.0 + 1.382937 * np.exp(-4.015292 * (dbh / 10.0))))
                * (ba + 0.087266) - 0.174533)
        tarif = self.calc_tarif(dbh, ht)

        cvt = tarif * (0.9679 - 0.1051 * 0.5523**(dbh - 1.5)) * term / 0.912733
        cvt[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvt


class Eq_4(SoftwoodVolumeEquation):
    """Ponderosa pine (DNR MEMO--SUMMERFIELD,11/7/80)

    Summerfield, Edward. 1980. In-house memo describing equations for
    Douglas-fir and ponderosa pine. State of Washington, Department of Natural
    Resources. On file with the PNW Research Station.
    """

    def calc_cvts(self, dbh, ht):
        # ba = 0.005454154 * (dbh**2)

        cvtsl = -8.521558 + 1.977243 * np.log(dbh) - 0.105288 * (
            np.log(ht))**2 + 136.0489 / ht**2 + 1.99546 * np.log(ht)
        cvts = np.exp(cvtsl)
        cvts[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvts

    def calc_tarif(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)

        cvts = self.calc_cvts(dbh, ht)
        tarif = (cvts * 0.912733) / (
            (1.033 * (1.0 + 1.382937 * np.exp(-4.015292 * dbh)))
            * (ba + 0.087266) - 0.174533)
        tarif[np.logical_or(dbh <= 0, ht <= 0)] = 0

        return tarif

    def calc_cv4(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)

        tarif = self.calc_tarif(dbh, ht)
        cv4 = tarif * (ba - 0.087266) / 0.912733
        cv4[np.logical_or(dbh < 5, ht <= 0)] = 0

        return cv4

    def calc_cvt(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)

        tarif = self.calc_tarif(dbh, ht)
        cvt = tarif * (0.9679 - 0.1051 * 0.5523**(dbh - 1.5)) * (
            (1.033 * (1.0 + 1.382937 * np.exp(-4.015292 * (dbh / 10.0))))
            * (ba + 0.087266) - 0.174533) / 0.912733
        cvt[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvt


class Eq_5(SoftwoodVolumeEquation):
    """Ponderosa pine (USDA-FS RES NOTE PNW-266)

    MacLean, Colin and John M. Berger. 1976. Softwood tree-volume equations for
    major California species. PNW Research Note, PNW-266. Pacific Northwest
    Forest and Range Experiment Station, Portland Oregon. 34p.
    """

    def calc_cvts(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        term = ((1.033 * (1.0 + 1.382937 * np.exp(-4.015292 * (dbh / 10.0))))
                * (ba + 0.087266) - 0.174533)
        cv4 = self.calc_cv4(dbh, ht)
        tarif = self.calc_tarif(dbh, ht)

        cvts = np.where(dbh >= 6.0, (cv4 * term) / (ba - 0.087266),
                        tarif * term)
        cvts[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvts

    def calc_cvt(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        term = ((1.033 * (1.0 + 1.382937 * np.exp(-4.015292 * (dbh / 10.0))))
                * (ba + 0.087266) - 0.174533)
        tarif = self.calc_tarif(dbh, ht)

        cvt = tarif * (0.9679 - 0.1051 * 0.5523**(dbh - 1.5)) * term / 0.912733
        cvt[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvt

    def calc_tarif(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        dbh_tmp = np.full(np.asanyarray(dbh).shape,
                          fill_value=6.0,
                          dtype=float)
        ba_tmp = 0.005454154 * (dbh_tmp**2)

        cf4 = np.clip(0.402060 - 0.899914 * (1 / dbh), 0.3, 0.4)
        cv4 = cf4 * ba * ht
        cf4_tmp = np.clip(0.402060 - 0.899914 * (1 / dbh_tmp), 0.3, 0.4)
        cv4_tmp = cf4_tmp * ba_tmp * ht

        tarif_tmp = np.clip((cv4_tmp * 0.912733) / (ba_tmp - 0.087266), 0.01,
                            None)

        tarif = np.where(
            dbh < 6.0,
            tarif_tmp * (0.5 * (dbh_tmp - dbh)**2 + (1.0 + 0.063
                                                     * (dbh_tmp - dbh)**2)),
            (cv4 * 0.912733) / (ba - 0.087266))
        tarif = np.clip(tarif, 0.01, None)
        tarif[np.logical_or(dbh <= 0, ht <= 0)] = 0

        return tarif

    def calc_cv4(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        cf4 = np.clip(0.402060 - 0.899914 * (1 / dbh), 0.3, 0.4)

        cv4 = np.where(dbh >= 5.0, cf4 * ba * ht, 0)
        cv4[np.logical_or(dbh < 5, ht <= 0)] = 0

        return cv4


class Eq_6(SoftwoodVolumeEquation):
    """Western hemlock (DNR NOTE 27,4/79)

    Chambers, C.J. and Foltz, B. 1979. The tarif system -- revisions and
    additions., Resource Management Report #27. WA Dept. of Nat. Resources.
    Olympia.
    """

    def calc_cvts(self, dbh, ht):
        cvtsl = -2.72170 + 2.00857 * np.log10(dbh) + 1.08620 * np.log10(
            ht) - 0.00568 * dbh

        cvts = 10**cvtsl
        cvts[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvts

    def calc_tarif(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        cvts = self.calc_cvts(dbh, ht)

        tarif = (cvts * 0.912733) / (
            (1.033 * (1.0 + 1.382937 * np.exp(-4.015292 * dbh)))
            * (ba + 0.087266) - 0.174533)

        tarif[np.logical_or(dbh <= 0, ht <= 0)] = 0

        return tarif

    def calc_cv4(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        tarif = self.calc_tarif(dbh, ht)

        cv4 = tarif * (ba - 0.087266) / 0.912733
        cv4[np.logical_or(dbh < 5, ht <= 0)] = 0

        return cv4

    def calc_cvt(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        tarif = self.calc_tarif(dbh, ht)

        cvt = tarif * (0.9679 - 0.1051 * 0.5523**(dbh - 1.5)) * (
            (1.033 * (1.0 + 1.382937 * np.exp(-4.015292 * (dbh / 10.0))))
            * (ba + 0.087266) - 0.174533) / 0.912733
        cvt[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvt


class Eq_7(SoftwoodVolumeEquation):
    """Western hemlock (BROWN (1962) BC FOREST SERV,P33)

    Browne, J.E. 1962. Standard cubic-foot volume tables for the commercial
    tree species of British Columbia. B.C. Forest Service, Victoria. 107 p.
    """

    def calc_cvts(self, dbh, ht):
        cvtsl = -2.663834 + 1.79023 * np.log10(dbh) + 1.124873 * np.log10(ht)

        cvts = 10**cvtsl
        cvts[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvts

    def calc_tarif(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        cvts = self.calc_cvts(dbh, ht)

        tarif = (cvts * 0.912733) / (
            (1.033 * (1.0 + 1.382937 * np.exp(-4.015292 * dbh)))
            * (ba + 0.087266) - 0.174533)
        tarif[np.logical_or(dbh <= 0, ht <= 0)] = 0

        return tarif

    def calc_cv4(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        tarif = self.calc_tarif(dbh, ht)

        cv4 = tarif * (ba - 0.087266) / 0.912733
        cv4[np.logical_or(dbh < 5, ht <= 0)] = 0

        return cv4

    def calc_cvt(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        tarif = self.calc_tarif(dbh, ht)

        cvt = tarif * (0.9679 - 0.1051 * 0.5523**(dbh - 1.5)) * (
            (1.033 * (1.0 + 1.382937 * np.exp(-4.015292 * (dbh / 10.0))))
            * (ba + 0.087266) - 0.174533) / 0.912733
        cvt[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvt


class Eq_8(SoftwoodVolumeEquation):
    """Western redcedar (REDCEDAR INTERIOR--DNR RPT#24,1977)

    Brackett, M. 1973. Notes on tarif tree volume computation. Res. Management
    Report 24. WA Dept. of Nat. Resources. Olympia. 26p.

    Brackett, Michael.  1977. Notes on tarif tree-volume computation.  DNR
    report #24. State of Washington, Department of Natural Resources, Olympia,
    WA. 132p.
    """

    def calc_cvts(self, dbh, ht):
        cvtsl = -2.464614 + 1.701993 * np.log10(dbh) + 1.067038 * np.log10(ht)

        cvts = 10**cvtsl
        cvts[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvts

    def calc_tarif(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        cvts = self.calc_cvts(dbh, ht)

        tarif = (cvts * 0.912733) / (
            (1.033 * (1.0 + 1.382937 * np.exp(-4.015292 * dbh)))
            * (ba + 0.087266) - 0.174533)
        tarif[np.logical_or(dbh <= 0, ht <= 0)] = 0

        return tarif

    def calc_cv4(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        tarif = self.calc_tarif(dbh, ht)

        cv4 = tarif * (ba - 0.087266) / 0.912733
        cv4[np.logical_or(dbh < 5, ht <= 0)] = 0

        return cv4

    def calc_cvt(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        tarif = self.calc_tarif(dbh, ht)

        cvt = tarif * (0.9679 - 0.1051 * 0.5523**(dbh - 1.5)) * (
            (1.033 * (1.0 + 1.382937 * np.exp(-4.015292 * (dbh / 10.0))))
            * (ba + 0.087266) - 0.174533) / 0.912733
        cvt[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvt


class Eq_9(SoftwoodVolumeEquation):
    """Western redcedar (REDCEDAR COAST--DNR RPT#24,1977)

    Brackett, M. 1973. Notes on tarif tree volume computation. Res. Management
    Report 24. WA Dept. of Nat. Resources. Olympia. 26p.

    Brackett, Michael. 1977. Notes on tarif tree-volume computation. DNR
    report #24. State of Washington, Department of Natural Resources, Olympia,
    WA. 132p.
    """

    def calc_cvts(self, dbh, ht):
        cvtsl = -2.379642 + 1.682300 * np.log10(dbh) + 1.039712 * np.log10(ht)

        cvts = 10**cvtsl
        cvts[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvts

    def calc_tarif(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        cvts = self.calc_cvts(dbh, ht)

        tarif = (cvts * 0.912733) / (
            (1.033 * (1.0 + 1.382937 * np.exp(-4.015292 * dbh)))
            * (ba + 0.087266) - 0.174533)
        tarif[np.logical_or(dbh <= 0, ht <= 0)] = 0

        return tarif

    def calc_cv4(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        tarif = self.calc_tarif(dbh, ht)

        cv4 = tarif * (ba - 0.087266) / 0.912733
        cv4[np.logical_or(dbh < 5, ht <= 0)] = 0

        return cv4

    def calc_cvt(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        tarif = self.calc_tarif(dbh, ht)

        cvt = tarif * (0.9679 - 0.1051 * 0.5523**(dbh - 1.5)) * (
            (1.033 * (1.0 + 1.382937 * np.exp(-4.015292 * (dbh / 10.0))))
            * (ba + 0.087266) - 0.174533) / 0.912733
        cvt[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvt


class Eq_10(SoftwoodVolumeEquation):
    """True firs (INTERIOR baLSAM--DNR RPT#24,1977)

    Brackett, M. 1973. Notes on tarif tree volume computation. Res. Management
    Report 24. WA Dept. of Nat. Resources. Olympia. 26p.

    Brackett, Michael.  1977. Notes on tarif tree-volume computation. DNR
    report #24. State of Washington, Department of Natural Resources, Olympia,
    WA. 132p.
    """

    def calc_cvts(self, dbh, ht):
        cvtsl = -2.502332 + 1.864963 * np.log10(dbh) + 1.004903 * np.log10(ht)

        cvts = 10**cvtsl
        cvts[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvts

    def calc_tarif(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        cvts = self.calc_cvts(dbh, ht)

        tarif = (cvts * 0.912733) / (
            (1.033 * (1.0 + 1.382937 * np.exp(-4.015292 * dbh)))
            * (ba + 0.087266) - 0.174533)
        tarif[np.logical_or(dbh <= 0, ht <= 0)] = 0

        return tarif

    def calc_cv4(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        tarif = self.calc_tarif(dbh, ht)

        cv4 = tarif * (ba - 0.087266) / 0.912733
        cv4[np.logical_or(dbh < 5, ht <= 0)] = 0

        return cv4

    def calc_cvt(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        tarif = self.calc_tarif(dbh, ht)

        cvt = tarif * (0.9679 - 0.1051 * 0.5523**(dbh - 1.5)) * (
            (1.033 * (1.0 + 1.382937 * np.exp(-4.015292 * (dbh / 10.0))))
            * (ba + 0.087266) - 0.174533) / 0.912733
        cvt[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvt


class Eq_11(SoftwoodVolumeEquation):
    """True firs (COAST baLSAM--DNR RPT#24,1977)

    Brackett, M. 1973. Notes on tarif tree volume computation. Res. Management
    Report 24. WA Dept. of Nat. Resources. Olympia. 26p.

    Brackett, Michael.  1977. Notes on tarif tree-volume computation. DNR
    report #24. State of Washington, Department of Natural Resources, Olympia,
    WA. 132p.
    """

    def calc_cvts(self, dbh, ht):
        cvtsl = -2.575642 + 1.806775 * np.log10(dbh) + 1.094665 * np.log10(ht)

        cvts = 10**cvtsl
        cvts[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvts

    def calc_tarif(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        cvts = self.calc_cvts(dbh, ht)

        tarif = (cvts * 0.912733) / (
            (1.033 * (1.0 + 1.382937 * np.exp(-4.015292 * dbh)))
            * (ba + 0.087266) - 0.174533)
        tarif[np.logical_or(dbh <= 0, ht <= 0)] = 0

        return tarif

    def calc_cv4(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        tarif = self.calc_tarif(dbh, ht)

        cv4 = tarif * (ba - 0.087266) / 0.912733
        cv4[np.logical_or(dbh < 5, ht <= 0)] = 0

        return cv4

    def calc_cvt(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        tarif = self.calc_tarif(dbh, ht)

        cvt = tarif * (0.9679 - 0.1051 * 0.5523**(dbh - 1.5)) * (
            (1.033 * (1.0 + 1.382937 * np.exp(-4.015292 * (dbh / 10.0))))
            * (ba + 0.087266) - 0.174533) / 0.912733
        cvt[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvt


class Eq_12(SoftwoodVolumeEquation):
    """Sitka spruce (SITKA SPRUCE INTERIOR--DNR RPT#24,1977)

    Brackett, M. 1973. Notes on tarif tree volume computation. Res. Management
    Report 24. WA Dept. of Nat. Resources. Olympia. 26p.

    Brackett, Michael.  1977. Notes on tarif tree-volume computation. DNR
    report #24. State of Washington, Department of Natural Resources, Olympia,
    WA. 132p.
    """

    def calc_cvts(self, dbh, ht):
        cvtsl = -2.539944 + 1.841226 * np.log10(dbh) + 1.034051 * np.log10(ht)

        cvts = 10**cvtsl
        cvts[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvts

    def calc_tarif(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        cvts = self.calc_cvts(dbh, ht)

        tarif = (cvts * 0.912733) / (
            (1.033 * (1.0 + 1.382937 * np.exp(-4.015292 * dbh)))
            * (ba + 0.087266) - 0.174533)
        tarif[np.logical_or(dbh <= 0, ht <= 0)] = 0

        return tarif

    def calc_cv4(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        tarif = self.calc_tarif(dbh, ht)

        cv4 = tarif * (ba - 0.087266) / 0.912733
        cv4[np.logical_or(dbh < 5, ht <= 0)] = 0

        return cv4

    def calc_cvt(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        tarif = self.calc_tarif(dbh, ht)

        cvt = tarif * (0.9679 - 0.1051 * 0.5523**(dbh - 1.5)) * (
            (1.033 * (1.0 + 1.382937 * np.exp(-4.015292 * (dbh / 10.0))))
            * (ba + 0.087266) - 0.174533) / 0.912733
        cvt[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvt


class Eq_13(SoftwoodVolumeEquation):
    """ Sitka spruce (SITKA SPRUCE MATURE--DNR RPT#24,1977)

    Brackett, M. 1973. Notes on tarif tree volume computation. Res. Management
    Report 24. WA Dept. of Nat. Resources. Olympia. 26p.

    Brackett, Michael.  1977. Notes on tarif tree-volume computation. DNR
    report #24. State of Washington, Department of Natural Resources, Olympia,
    WA. 132p.
    """

    def calc_cvts(self, dbh, ht):
        cvtsl = -2.700574 + 1.754171 * np.log10(dbh) + 1.164531 * np.log10(ht)

        cvts = 10**cvtsl
        cvts[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvts

    def calc_tarif(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        cvts = self.calc_cvts(dbh, ht)

        tarif = (cvts * 0.912733) / (
            (1.033 * (1.0 + 1.382937 * np.exp(-4.015292 * dbh)))
            * (ba + 0.087266) - 0.174533)
        tarif[np.logical_or(dbh <= 0, ht <= 0)] = 0

        return tarif

    def calc_cv4(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        tarif = self.calc_tarif(dbh, ht)

        cv4 = tarif * (ba - 0.087266) / 0.912733
        cv4[np.logical_or(dbh < 5, ht <= 0)] = 0

        return cv4

    def calc_cvt(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        tarif = self.calc_tarif(dbh, ht)

        cvt = tarif * (0.9679 - 0.1051 * 0.5523**(dbh - 1.5)) * (
            (1.033 * (1.0 + 1.382937 * np.exp(-4.015292 * (dbh / 10.0))))
            * (ba + 0.087266) - 0.174533) / 0.912733
        cvt[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvt


class Eq_14(SoftwoodVolumeEquation):
    """Other junipers (CHOJNACKY, 1985)

    Chojnacky D.C., 1985.  Pinyon-Juniper Volume Equations for the Central
    Rocky Mountain States. Res. Note INT-339, USDA, Forest Service,
    Intermountain Res. Station, Ogden, UT 84401.
    """

    def calc_cvts(self, drc, ht, stems=np.array([1])):
        factor = np.where((drc >= 3) & (ht > 0), drc * drc * ht, 0)
        s = np.where(stems > 1, 0, 1)

        cvts = np.clip(
            (-0.13386 + (0.133726 * (factor**(1. / 3.))) + (0.036329 * s))**3,
            0.1, None)
        cvts[np.logical_or(drc < 1, ht <= 0)] = 0

        return cvts


class Eq_14_1(SoftwoodVolumeEquation):
    """Singleleaf pinyon (CHOJNACKY, 1985)

    Chojnacky D.C., 1985.  Pinyon-Juniper Volume Equations for the Central
    Rocky Mountain States. Res. Note INT-339, USDA, Forest Service,
    Intermountain Res. Station, Ogden, UT 84401.
    """

    def calc_cvts(self, drc, ht, stems=np.array([1])):
        factor = np.where((drc >= 3) & (ht > 0), drc * drc * ht, 0)
        s = np.where(stems > 1, 0, 1)

        cvts = np.clip(
            (-0.14240 + (0.148190 * (factor**(1. / 3.))) - (0.16712 * s))**3,
            0.1, None)
        cvts[np.logical_or(drc < 1, ht <= 0)] = 0

        return cvts


class Eq_14_2(SoftwoodVolumeEquation):
    """Rocky Mountain juniper (CHOJNACKY, 1985)

    Chojnacky D.C., 1985.  Pinyon-Juniper Volume Equations for the Central
    Rocky Mountain States. Res. Note INT-339, USDA, Forest Service,
    Intermountain Res. Station, Ogden, UT 84401.
    """

    def calc_cvts(self, drc, ht):
        factor = np.where((drc >= 3) & (ht > 0), drc * drc * ht, 0)

        cvts = np.clip((0.02434 + (0.119106 * (factor**(1. / 3.))))**3, 0.1,
                       None)
        cvts[np.logical_or(drc < 1, ht <= 0)] = 0

        return cvts


class Eq_15(SoftwoodVolumeEquation):
    """Lodgepole pine (LODGEPOLE PINE--DNR RPT#24,1977)

    Brackett, M. 1973. Notes on tarif tree volume computation. Res. Management
    Report 24. WA Dept. of Nat. Resources. Olympia. 26p.

    Brackett, Michael. 1977. Notes on tarif tree-volume computation. DNR report
    #24. State of Washington, Department of Natural Resources, Olympia, WA.
    132p.
    """

    def calc_cvts(self, dbh, ht):
        cvtsl = -2.615591 + 1.847504 * np.log10(dbh) + 1.085772 * np.log10(ht)

        cvts = 10**cvtsl
        cvts[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvts

    def calc_tarif(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        cvts = self.calc_cvts(dbh, ht)

        tarif = (cvts * 0.912733) / (
            (1.033 * (1.0 + 1.382937 * np.exp(-4.015292 * dbh)))
            * (ba + 0.087266) - 0.174533)
        tarif[np.logical_or(dbh <= 0, ht <= 0)] = 0

        return tarif

    def calc_cv4(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        tarif = self.calc_tarif(dbh, ht)

        cv4 = tarif * (ba - 0.087266) / 0.912733
        cv4[np.logical_or(dbh < 5, ht <= 0)] = 0

        return cv4

    def calc_cvt(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        tarif = self.calc_tarif(dbh, ht)

        cvt = tarif * (0.9679 - 0.1051 * 0.5523**(dbh - 1.5)) * (
            (1.033 * (1.0 + 1.382937 * np.exp(-4.015292 * (dbh / 10.0))))
            * (ba + 0.087266) - 0.174533) / 0.912733
        cvt[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvt


class Eq_16(SoftwoodVolumeEquation):
    """Lodgepole pine (USDA-FS RES NOTE PNW-266)

    MacLean, Colin and John M. Berger. 1976. Softwood tree-volume equations
    for major California species. PNW Research Note, PNW-266. Pacific Northwest
    Forest and Range Experiment Station, Portland Oregon. 34p.
    """

    def calc_cvts(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        term = ((1.033 * (1.0 + 1.382937 * np.exp(-4.015292 * (dbh / 10.0))))
                * (ba + 0.087266) - 0.174533)
        tarif = self.calc_tarif(dbh, ht)
        cv4 = self.calc_cv4(dbh, ht)

        cvts = np.where(dbh < 6.0, tarif * term,
                        (cv4 * term) / (ba - 0.087266))
        cvts[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvts

    def calc_tarif(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)

        dbh_tmp = np.full(np.asanyarray(dbh).shape,
                          fill_value=6.0,
                          dtype=float)
        ba_tmp = 0.005454154 * (dbh_tmp**2)

        cf4 = 0.422709 - 0.0000612236 * (ht**2 / dbh)
        cf4 = np.clip(cf4, 0.3, 0.4)

        cf4_tmp = 0.422709 - 0.0000612236 * (ht**2 / dbh_tmp)
        cf4_tmp = np.clip(cf4_tmp, 0.3, 0.4)

        cv4 = self.calc_cv4(dbh, ht)
        cv4_tmp = self.calc_cv4(dbh_tmp, ht)

        tarif_tmp = np.clip((cv4_tmp * 0.912733) / (ba_tmp - 0.087266), 0.01,
                            None)

        tarif = np.where(
            dbh < 6.0,
            tarif_tmp * (0.5 * (dbh_tmp - dbh)**2 + (1.0 + 0.063
                                                     * (dbh_tmp - dbh)**2)),
            (cv4 * 0.912733) / (ba - 0.087266))
        tarif = np.clip(tarif, 0.01, None)
        tarif[np.logical_or(dbh <= 0, ht <= 0)] = 0

        return tarif

    def calc_cv4(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)

        cf4 = 0.422709 - 0.0000612236 * (ht**2 / dbh)
        cf4 = np.clip(cf4, 0.3, 0.4)

        cv4 = cf4 * ba * ht
        #cv4 = np.where(dbh < 5.0, 0, cv4)
        cv4[np.logical_or(dbh < 5, ht <= 0)] = 0

        return cv4

    def calc_cvt(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        term = ((1.033 * (1.0 + 1.382937 * np.exp(-4.015292 * (dbh / 10.0))))
                * (ba + 0.087266) - 0.174533)
        tarif = self.calc_tarif(dbh, ht)

        cvt = tarif * (0.9679 - 0.1051 * 0.5523**(dbh - 1.5)) * term / 0.912733
        cvt[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvt


class Eq_17(SoftwoodVolumeEquation):
    """Mountain hemlock (BELL, OSU RES.BULL 35)

    Bell, J.F., Marshall, D.D. and Johnson G.P. 1981. Tarif tables for mountain
    hemlock: developed from an equation of total stem cubic-foot volume.
    Research Bulletin #35. OSU Forest Research Lab, School of Forestry, Oregon
    State University, Corvallis, OR.
    """

    def calc_cvts(self, dbh, ht):
        cvts = 0.001106485 * dbh**1.8140497 * ht**1.2744923
        cvts[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvts

    def calc_tarif(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        cvts = self.calc_cvts(dbh, ht)

        tarif = (cvts * 0.912733) / (
            (1.033 * (1.0 + 1.382937 * np.exp(-4.015292 * dbh)))
            * (ba + 0.087266) - 0.174533)
        tarif[np.logical_or(dbh <= 0, ht <= 0)] = 0

        return tarif

    def calc_cv4(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        tarif = self.calc_tarif(dbh, ht)

        cv4 = tarif * (ba - 0.087266) / 0.912733
        cv4[np.logical_or(dbh < 5, ht <= 0)] = 0

        return cv4

    def calc_cvt(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        tarif = self.calc_tarif(dbh, ht)

        cvt = tarif * (0.9679 - 0.1051 * 0.5523**(dbh - 1.5)) * (
            (1.033 * (1.0 + 1.382937 * np.exp(-4.015292 * (dbh / 10.0))))
            * (ba + 0.087266) - 0.174533) / 0.912733
        cvt[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvt


class Eq_18(SoftwoodVolumeEquation):
    """Shasta red fir (USDA-FS RES NOTE PNW-266)

    MacLean, Colin and John M. Berger. 1976. Softwood tree-volume equations
    for major California species. PNW Research Note, PNW-266. Pacific Northwest
    Forest and Range Experiment Station, Portland Oregon. 34p.
    """

    def calc_cvts(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        term = ((1.033 * (1.0 + 1.382937 * np.exp(-4.015292 * (dbh / 10.0))))
                * (ba + 0.087266) - 0.174533)
        tarif = self.calc_tarif(dbh, ht)
        cv4 = self.calc_cv4(dbh, ht)

        cvts = np.where(dbh < 6.0, tarif * term,
                        (cv4 * term) / (ba - 0.087266))
        cvts[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvts

    def calc_tarif(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)

        dbh_tmp = np.full(np.asanyarray(dbh).shape,
                          fill_value=6.0,
                          dtype=float)
        ba_tmp = 0.005454154 * (dbh_tmp**2)
        # cf4 = np.clip(0.231237 + 0.028176 * (ht / dbh), 0.3, 0.4)
        # cf4_tmp = np.clip(0.231237 + 0.028176 * (ht / dbh_tmp), 0.3, 0.4)
        cv4 = self.calc_cv4(dbh, ht)
        cv4_tmp = self.calc_cv4(dbh_tmp, ht)

        tarif_tmp = np.clip((cv4_tmp * 0.912733) / (ba_tmp - 0.087266), 0.01,
                            None)

        tarif = np.where(
            dbh < 6.0,
            tarif_tmp * (0.5 * (dbh_tmp - dbh)**2 + (1.0 + 0.063
                                                     * (dbh_tmp - dbh)**2)),
            (cv4 * 0.912733) / (ba - 0.087266))
        tarif = np.clip(tarif, 0.01, None)
        tarif[np.logical_or(dbh <= 0, ht <= 0)] = 0

        return tarif

    def calc_cv4(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)

        cf4 = np.clip(0.231237 + 0.028176 * (ht / dbh), 0.3, 0.4)
        cv4 = cf4 * ba * ht
        #cv4 = np.where(dbh < 5.0, 0, cv4)
        cv4[np.logical_or(dbh < 5, ht <= 0)] = 0

        return cv4

    def calc_cvt(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        term = ((1.033 * (1.0 + 1.382937 * np.exp(-4.015292 * (dbh / 10.0))))
                * (ba + 0.087266) - 0.174533)
        tarif = self.calc_tarif(dbh, ht)

        cvt = tarif * (0.9679 - 0.1051 * 0.5523**(dbh - 1.5)) * term / 0.912733
        cvt[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvt


class Eq_19(SoftwoodVolumeEquation):
    """Incense cedar (USDA-FS RES NOTE PNW-266)

    MacLean, Colin and John M. Berger. 1976. Softwood tree-volume equations
    for major California species. PNW Research Note, PNW-266. Pacific Northwest
    Forest and Range Experiment Station, Portland Oregon. 34p.
    """

    def calc_cvts(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        term = ((1.033 * (1.0 + 1.382937 * np.exp(-4.015292 * (dbh / 10.0))))
                * (ba + 0.087266) - 0.174533)
        tarif = self.calc_tarif(dbh, ht)
        cv4 = self.calc_cv4(dbh, ht)

        cvts = np.where(dbh < 6.0, tarif * term,
                        (cv4 * term) / (ba - 0.087266))
        cvts[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvts

    def calc_tarif(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)

        dbh_tmp = np.full(np.asanyarray(dbh).shape,
                          fill_value=6.0,
                          dtype=float)
        ba_tmp = 0.005454154 * (dbh_tmp**2)
        # cf4 = np.clip(0.225786 + 4.44236 * (1 / ht), 0.27, None)
        # cf4_tmp = np.clip(0.225786 + 4.44236 * (1 / ht), 0.27, None)
        cv4 = self.calc_cv4(dbh, ht)
        cv4_tmp = self.calc_cv4(dbh_tmp, ht)

        tarif_tmp = np.clip((cv4_tmp * 0.912733) / (ba_tmp - 0.087266), 0.01,
                            None)

        tarif = np.where(
            dbh < 6.0,
            tarif_tmp * (0.5 * (dbh_tmp - dbh)**2 + (1.0 + 0.063
                                                     * (dbh_tmp - dbh)**2)),
            (cv4 * 0.912733) / (ba - 0.087266))
        tarif = np.clip(tarif, 0.01, None)
        tarif[np.logical_or(dbh <= 0, ht <= 0)] = 0

        return tarif

    def calc_cv4(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)

        cf4 = np.clip(0.225786 + 4.44236 * (1 / ht), 0.27, None)
        cv4 = cf4 * ba * ht
        #cv4 = np.where(dbh < 5.0, 0, cv4)
        cv4[np.logical_or(dbh < 5, ht <= 0)] = 0

        return cv4

    def calc_cvt(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        term = ((1.033 * (1.0 + 1.382937 * np.exp(-4.015292 * (dbh / 10.0))))
                * (ba + 0.087266) - 0.174533)
        tarif = self.calc_tarif(dbh, ht)

        cvt = tarif * (0.9679 - 0.1051 * 0.5523**(dbh - 1.5)) * term / 0.912733
        cvt[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvt


class Eq_20(SoftwoodVolumeEquation):
    """Sugar pine (USDA-FS RES NOTE PNW-266)

    MacLean, Colin and John M. Berger. 1976. Softwood tree-volume equations
    for major California species. PNW Research Note, PNW-266. Pacific Northwest
    Forest and Range Experiment Station, Portland Oregon. 34p.
    """

    def calc_cvts(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        term = ((1.033 * (1.0 + 1.382937 * np.exp(-4.015292 * (dbh / 10.0))))
                * (ba + 0.087266) - 0.174533)
        tarif = self.calc_tarif(dbh, ht)
        cv4 = self.calc_cv4(dbh, ht)

        cvts = np.where(dbh < 6.0, tarif * term,
                        (cv4 * term) / (ba - 0.087266))
        cvts[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvts

    def calc_tarif(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)

        dbh_tmp = np.full(np.asanyarray(dbh).shape,
                          fill_value=6.0,
                          dtype=float)
        ba_tmp = 0.005454154 * (dbh_tmp**2)
        # cf4 = np.clip(0.358550 - 0.488134 * (1 / dbh), 0.3, 0.4)
        # cf4_tmp = np.clip(0.358550 - 0.488134 * (1 / dbh_tmp), 0.3, 0.4)
        cv4 = self.calc_cv4(dbh, ht)
        cv4_tmp = self.calc_cv4(dbh_tmp, ht)

        tarif_tmp = np.clip((cv4_tmp * 0.912733) / (ba_tmp - 0.087266), 0.01,
                            None)

        tarif = np.where(
            dbh < 6.0,
            tarif_tmp * (0.5 * (dbh_tmp - dbh)**2 + (1.0 + 0.063
                                                     * (dbh_tmp - dbh)**2)),
            (cv4 * 0.912733) / (ba - 0.087266))
        tarif = np.clip(tarif, 0.01, None)
        tarif[np.logical_or(dbh <= 0, ht <= 0)] = 0

        return tarif

    def calc_cv4(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        cf4 = np.clip(0.358550 - 0.488134 * (1 / dbh), 0.3, 0.4)

        cv4 = cf4 * ba * ht
        #cv4 = np.where(dbh < 5.0, 0, cv4)
        cv4[np.logical_or(dbh < 5, ht <= 0)] = 0

        return cv4

    def calc_cvt(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        term = ((1.033 * (1.0 + 1.382937 * np.exp(-4.015292 * (dbh / 10.0))))
                * (ba + 0.087266) - 0.174533)
        tarif = self.calc_tarif(dbh, ht)

        cvt = tarif * (0.9679 - 0.1051 * 0.5523**(dbh - 1.5)) * term / 0.912733
        cvt[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvt


class Eq_21(SoftwoodVolumeEquation):
    """Western juniper (CHITTESTER,1984)

    Chittester, Judith and Colin MacLean. 1984. Cubic-foot tree-volume
    equations and tables for western juniper. Research Note, PNW-420. Pacific
    Northwest Forest and Range Experiment Station. Portland, Oregon. 8p.
    """

    def calc_cvts(self, dbh, ht):
        cvts = (0.005454154 * (0.30708901 + 0.00086157622 * ht
                - 0.0037255243 * dbh * ht
                / (ht - 4.5)) * dbh**2 * ht * (ht / (ht - 4.5))**2).clip(0,)
        cvts[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvts

    def calc_tarif(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        cvts = self.calc_cvts(dbh, ht)

        tarif = (cvts * 0.912733) / (
            (1.033 * (1.0 + 1.382937 * np.exp(-4.015292 * dbh)))
            * (ba + 0.087266) - 0.174533)
        tarif[np.logical_or(dbh <= 0, ht <= 0)] = 0

        return tarif

    def calc_cv4(self, dbh, ht):
        cvts = self.calc_cvts(dbh, ht)

        cv4 = (cvts + 3.48) / (1.18052 + 0.32736 * np.exp(-0.1 * dbh)) - 2.948
        cv4[np.logical_or(dbh < 5, ht <= 0)] = 0

        return cv4

    def calc_cvt(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        tarif = self.calc_tarif(dbh, ht)

        cvt = tarif * (0.9679 - 0.1051 * 0.5523**(dbh - 1.5)) * (
            (1.033 * (1.0 + 1.382937 * np.exp(-4.015292 * (dbh / 10.0))))
            * (ba + 0.087266) - 0.174533) / 0.912733
        cvt[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvt


class Eq_22(SoftwoodVolumeEquation):
    """Western larch (LARCH--DNR RPT#24,1977)

    Brackett, M. 1973. Notes on tarif tree volume computation. Res. Management
    Report 24. WA Dept. of Nat. Resources. Olympia. 26p.

    Brackett, Michael. 1977. Notes on tarif tree-volume computation. DNR
    report #24. State of Washington, Department of Natural Resources, Olympia,
    WA. 132p.
    """

    def calc_cvts(self, dbh, ht):
        cvtsl = -2.624325 + 1.847123 * np.log10(dbh) + 1.044007 * np.log10(ht)

        cvts = 10**cvtsl
        cvts[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvts

    def calc_tarif(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        cvts = self.calc_cvts(dbh, ht)

        tarif = (cvts * 0.912733) / (
            (1.033 * (1.0 + 1.382937 * np.exp(-4.015292 * dbh)))
            * (ba + 0.087266) - 0.174533)
        tarif[np.logical_or(dbh <= 0, ht <= 0)] = 0

        return tarif

    def calc_cv4(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        tarif = self.calc_tarif(dbh, ht)

        cv4 = tarif * (ba - 0.087266) / 0.912733
        cv4[np.logical_or(dbh < 5, ht <= 0)] = 0

        return cv4

    def calc_cvt(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        tarif = self.calc_tarif(dbh, ht)

        cvt = tarif * (0.9679 - 0.1051 * 0.5523**(dbh - 1.5)) * (
            (1.033 * (1.0 + 1.382937 * np.exp(-4.015292 * (dbh / 10.0))))
            * (ba + 0.087266) - 0.174533) / 0.912733
        cvt[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvt


class Eq_23(SoftwoodVolumeEquation):
    """White fir (USDA-FS RES NOTE PNW-266)

    MacLean, Colin and John M. Berger. 1976. Softwood tree-volume equations
    for major California species. PNW Research Note, PNW-266. Pacific Northwest
    Forest and Range Experiment Station, Portland Oregon. 34p.
    """

    def calc_cvts(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        term = ((1.033 * (1.0 + 1.382937 * np.exp(-4.015292 * (dbh / 10.0))))
                * (ba + 0.087266) - 0.174533)
        tarif = self.calc_tarif(dbh, ht)
        cv4 = self.calc_cv4(dbh, ht)

        cvts = np.where(dbh < 6.0, tarif * term,
                        (cv4 * term) / (ba - 0.087266))
        cvts[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvts

    def calc_tarif(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        dbh_tmp = np.full(np.asanyarray(dbh).shape,
                          fill_value=6.0,
                          dtype=float)
        ba_tmp = 0.005454154 * (dbh_tmp**2)

        cf4 = 0.299039 + 1.91272 * (1 / ht) + 0.0000367217 * (ht**2 / dbh)
        cf4 = np.clip(cf4, 0.3, 0.4)

        cf4_tmp = 0.299039 + 1.91272 * (1 / ht) + 0.0000367217 * (ht**2
                                                                  / dbh_tmp)
        cf4_tmp = np.clip(cf4_tmp, 0.3, 0.4)

        cv4 = self.calc_cv4(dbh, ht)
        cv4_tmp = self.calc_cv4(dbh_tmp, ht)

        tarif_tmp = np.clip((cv4_tmp * 0.912733) / (ba_tmp - 0.087266), 0.01,
                            None)

        tarif = np.where(
            dbh < 6.0,
            tarif_tmp * (0.5 * (dbh_tmp - dbh)**2 + (1.0 + 0.063
                                                     * (dbh_tmp - dbh)**2)),
            (cv4 * 0.912733) / (ba - 0.087266))
        tarif = np.clip(tarif, 0.01, None)
        tarif[np.logical_or(dbh <= 0, ht <= 0)] = 0

        return tarif

    def calc_cv4(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)

        cf4 = 0.299039 + 1.91272 * (1 / ht) + 0.0000367217 * (ht**2 / dbh)
        cf4 = np.clip(cf4, 0.3, 0.4)

        cv4 = cf4 * ba * ht
        #cv4 = np.where(dbh < 5.0, 0, cv4)
        cv4[np.logical_or(dbh < 5, ht <= 0)] = 0

        return cv4

    def calc_cvt(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        tarif = self.calc_tarif(dbh, ht)
        term = ((1.033 * (1.0 + 1.382937 * np.exp(-4.015292 * (dbh / 10.0))))
                * (ba + 0.087266) - 0.174533)

        cvt = tarif * (0.9679 - 0.1051 * 0.5523**(dbh - 1.5)) * term / 0.912733
        cvt[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvt


class Eq_24(SoftwoodVolumeEquation):
    """Redwood (Krumland, B.E. and L.E. Wensel. 1975. And DNR RPT#24, 1977)

    Krumland, B.E. and L.E. Wensel. 1975. Preliminary young growth volume
    tables for coastal California conifers. Research Note #1. In-house memo.
    Co-op Redwood Yield Research Project. Department of Forestry and
    Conservation, College of Natural Resources, U of Cal, Berkeley. On file
    with the PNW Research Station.
    """

    def calc_cvts(self, dbh, ht):
        cvts = np.exp(-6.2597 + 1.9967 * np.log(dbh) + 0.9642 * np.log(ht))
        cvts[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvts

    def calc_tarif(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        cvts = self.calc_cvts(dbh, ht)

        tarif = (cvts * 0.912733) / (
            (1.033 * (1.0 + 1.382937 * np.exp(-4.015292 * dbh)))
            * (ba + 0.087266) - 0.174533)
        tarif[np.logical_or(dbh <= 0, ht <= 0)] = 0

        return tarif

    def calc_cv4(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        tarif = self.calc_tarif(dbh, ht)

        cv4 = tarif * (ba - 0.087266) / 0.912733
        cv4[np.logical_or(dbh < 5, ht <= 0)] = 0

        return cv4

    def calc_cvt(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        tarif = self.calc_tarif(dbh, ht)

        cvt = tarif * (0.9679 - 0.1051 * 0.5523**(dbh - 1.5)) * (
            (1.033 * (1.0 + 1.382937 * np.exp(-4.015292 * (dbh / 10.0))))
            * (ba + 0.087266) - 0.174533) / 0.912733
        cvt[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvt


class Eq_25(HardwoodVolumeEquation_NoX):
    """Red alder (CURTIS/BRUCE, PNW-56)

    Curtis, Robert O., Bruce, David, and Caryanne VanCoevering. 1968. Volume
    and taper tables for red alder.  US Forest Serv. Res. Pap. PNW-56. PNW
    Forest & Range Exp. Sta., Portland, Oregon.  35p.
    """

    def calc_cvt(self, dbh, ht):
        ht = np.clip(ht, 18, None)
        # ba = 0.005454154 * (dbh**2)
        z = (ht - 0.5 - dbh / 24.0) / (ht - 4.5)

        f = (0.3651 * z**2.5 - 7.9032 * (z**2.5) * dbh / 1000.0 + 3.295 * (
            z**2.5
        ) * ht / 1000.0 - 1.9856 * (z**2.5) * ht * dbh / 100000.0 + -2.9668 * (
            z**2.5) * (ht**2) / 1000000.0 + 1.5092 * (z**2.5) * (
                ht ** 0.5) / 1000.0 + 4.9395 * (z**4.0) * dbh
                / 1000.0 + -2.05937 * (
                        z**4.0) * ht / 1000.0 + 1.5042 * (
                            z**33.0) * ht * dbh / 1000000.0 - 1.1433 * (
                                z**33.0) * (ht**0.5) / 10000.0 + 1.809 * (
                                    z**41.0) * (ht**2) / 10000000.0)

        cvt = 0.00545415 * dbh**2 * (ht - 4.5) * f
        cvt[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvt

    def calc_tarif(self, dbh, ht):
        ht = np.clip(ht, 18, None)
        ba = 0.005454154 * (dbh**2)
        cvt = self.calc_cvt(dbh, ht)

        tarif = (cvt * 0.912733) / ((0.9679 - 0.1051 * 0.5523**(dbh - 1.5)) * (
            (1.033 * (1.0 + 1.382937 * np.exp(-4.015292 * (dbh / 10.0))))
            * (ba + 0.087266) - 0.174533))
        tarif[np.logical_or(dbh <= 0, ht <= 0)] = 0

        return tarif

    def calc_cvts(self, dbh, ht):
        ht = np.clip(ht, 18, None)
        ba = 0.005454154 * (dbh**2)
        tarif = self.calc_tarif(dbh, ht)
        cvts = (tarif
                * ((1.0330 * (1.0 + 1.382937
                    * np.exp(-4.015292 * (dbh / 10.0))))
                    * (ba + 0.087266) - 0.174533) / 0.912733)

        cvts = np.clip(cvts, 0, None)
        cvts[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvts

    def calc_cv4(self, dbh, ht):
        ht = np.clip(ht, 18, None)
        ba = 0.005454154 * (dbh**2)
        tarif = self.calc_tarif(dbh, ht)

        cv4 = tarif * (ba - 0.087266) / 0.912733
        cv4[np.logical_or(dbh < 5, ht <= 0)] = 0

        return cv4

    def calc_cv8(self, dbh, ht):
        ht = np.clip(ht, 18, None)
        rc8 = 0.983 - (0.983 * 0.65**(dbh - 8.6))
        cv4 = self.calc_cv4(dbh, ht)

        cv8 = rc8 * cv4
        cv8[np.logical_or(dbh < 11, ht <= 0)] = 0

        return cv8


class Eq_26(HardwoodVolumeEquation_NoX):
    """Red alder (BC-ALDER--DNR RPT#24,1977)

    Brackett, Michael. 1977. Notes on tarif tree-volume computation. DNR
    report #24. State of Washington, Department of Natural Resources, Olympia,
    WA. 132p.
    """

    def calc_cvts(self, dbh, ht):
        cvtsl = -2.672775 + 1.920617 * np.log10(dbh) + 1.074024 * np.log10(ht)

        cvts = 10**cvtsl
        cvts[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvts

    def calc_tarif(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        cvts = self.calc_cvts(dbh, ht)

        tarif = (cvts * 0.912733) / (
            (1.033 * (1.0 + 1.382937 * np.exp(-4.015292 * dbh)))
            * (ba + 0.087266) - 0.174533)
        tarif[np.logical_or(dbh <= 0, ht <= 0)] = 0

        return tarif

    def calc_cvt(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        tarif = self.calc_tarif(dbh, ht)

        cvt = tarif * (0.9679 - 0.1051 * 0.5523**(dbh - 1.5)) * (
            (1.033 * (1.0 + 1.382937 * np.exp(-4.015292 * (dbh / 10.0))))
            * (ba + 0.087266) - 0.174533) / 0.912733
        cvt[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvt

    def calc_cv4(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        tarif = self.calc_tarif(dbh, ht)

        cv4 = tarif * (ba - 0.087266) / 0.912733
        cv4[np.logical_or(dbh < 5, ht <= 0)] = 0

        return cv4

    def calc_cv8(self, dbh, ht):
        cv4 = self.calc_cv4(dbh, ht)

        rc8 = 0.983 - (0.983 * 0.65**(dbh - 8.6))
        cv8 = rc8 * cv4

        cv8[np.logical_or(dbh < 11, ht <= 0)] = 0

        return cv8


class Eq_27(HardwoodVolumeEquation_NoX):
    """Black cottonwood (BC-COTTONWOOD--DNR RPT#24, 1977)

    Brackett, Michael. 1977. Notes on tarif tree-volume computation. DNR
    report #24. State of Washington, Department of Natural Resources, Olympia,
    WA. 132p.
    """

    def calc_cvts(self, dbh, ht):
        cvtsl = -2.945047 + 1.803973 * np.log10(dbh) + 1.238853 * np.log10(ht)

        cvts = 10**cvtsl
        cvts[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvts

    def calc_tarif(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        cvts = self.calc_cvts(dbh, ht)

        tarif = (cvts * 0.912733) / (
            (1.033 * (1.0 + 1.382937 * np.exp(-4.015292 * dbh)))
            * (ba + 0.087266) - 0.174533)
        tarif[np.logical_or(dbh <= 0, ht <= 0)] = 0

        return tarif

    def calc_cvt(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        tarif = self.calc_tarif(dbh, ht)

        cvt = tarif * (0.9679 - 0.1051 * 0.5523**(dbh - 1.5)) * (
            (1.033 * (1.0 + 1.382937 * np.exp(-4.015292 * (dbh / 10.0))))
            * (ba + 0.087266) - 0.174533) / 0.912733
        cvt[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvt

    def calc_cv4(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        tarif = self.calc_tarif(dbh, ht)

        cv4 = tarif * (ba - 0.087266) / 0.912733
        cv4[np.logical_or(dbh < 5, ht <= 0)] = 0

        return cv4

    def calc_cv8(self, dbh, ht):
        cv4 = self.calc_cv4(dbh, ht)
        rc8 = 0.983 - (0.983 * 0.65**(dbh - 8.6))

        cv8 = rc8 * cv4
        cv8[np.logical_or(dbh < 11, ht <= 0)] = 0

        return cv8


class Eq_28(HardwoodVolumeEquation_NoX):
    """Aspen (BC-ASPEN--DNR RPT#24,1977)

    Brackett, Michael. 1977. Notes on tarif tree-volume computation. DNR
    report #24. State of Washington, Department of Natural Resources, Olympia,
    WA. 132p.
    """

    def calc_cvts(self, dbh, ht):
        cvtsl = -2.635360 + 1.946034 * np.log10(dbh) + 1.024793 * np.log10(ht)

        cvts = 10**cvtsl
        cvts[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvts

    def calc_tarif(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        cvts = self.calc_cvts(dbh, ht)

        tarif = (cvts * 0.912733) / (
            (1.033 * (1.0 + 1.382937 * np.exp(-4.015292 * dbh)))
            * (ba + 0.087266) - 0.174533)
        tarif[np.logical_or(dbh <= 0, ht <= 0)] = 0

        return tarif

    def calc_cvt(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        tarif = self.calc_tarif(dbh, ht)

        cvt = tarif * (0.9679 - 0.1051 * 0.5523**(dbh - 1.5)) * (
            (1.033 * (1.0 + 1.382937 * np.exp(-4.015292 * (dbh / 10.0))))
            * (ba + 0.087266) - 0.174533) / 0.912733
        cvt[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvt

    def calc_cv4(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        tarif = self.calc_tarif(dbh, ht)

        cv4 = tarif * (ba - 0.087266) / 0.912733
        cv4[np.logical_or(dbh < 5, ht <= 0)] = 0

        return cv4

    def calc_cv8(self, dbh, ht):
        cv4 = self.calc_cv4(dbh, ht)
        rc8 = 0.983 - (0.983 * 0.65**(dbh - 8.6))

        cv8 = rc8 * cv4
        cv8[np.logical_or(dbh < 11, ht <= 0)] = 0

        return cv8


class Eq_29(HardwoodVolumeEquation_NoX):
    """Birch (BC-BIRCH--DNR RPT#24, 1977)

    Brackett, Michael. 1977. Notes on tarif tree-volume computation. DNR
    report #24. State of Washington, Department of Natural Resources, Olympia,
    WA. 132p.
    """

    def calc_cvts(self, dbh, ht):
        cvtsl = -2.757813 + 1.911681 * np.log10(dbh) + 1.105403 * np.log10(ht)

        cvts = 10**cvtsl
        cvts[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvts

    def calc_tarif(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        cvts = self.calc_cvts(dbh, ht)

        tarif = (cvts * 0.912733) / (
            (1.033 * (1.0 + 1.382937 * np.exp(-4.015292 * dbh)))
            * (ba + 0.087266) - 0.174533)
        tarif[np.logical_or(dbh <= 0, ht <= 0)] = 0

        return tarif

    def calc_cvt(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        tarif = self.calc_tarif(dbh, ht)

        cvt = tarif * (0.9679 - 0.1051 * 0.5523**(dbh - 1.5)) * (
            (1.033 * (1.0 + 1.382937 * np.exp(-4.015292 * (dbh / 10.0))))
            * (ba + 0.087266) - 0.174533) / 0.912733
        cvt[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvt

    def calc_cv4(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        tarif = self.calc_tarif(dbh, ht)

        cv4 = tarif * (ba - 0.087266) / 0.912733
        cv4[np.logical_or(dbh < 5, ht <= 0)] = 0

        return cv4

    def calc_cv8(self, dbh, ht):
        cv4 = self.calc_cv4(dbh, ht)
        rc8 = 0.983 - (0.983 * 0.65**(dbh - 8.6))

        cv8 = rc8 * cv4
        cv8[np.logical_or(dbh < 11, ht <= 0)] = 0

        return cv8


class Eq_30(HardwoodVolumeEquation_NoX):
    """Bigleaf maple (BC-BIRCH--DNR RPT#24, 1977)

    Brackett, Michael. 1977. Notes on tarif tree-volume computation. DNR
    report #24. State of Washington, Department of Natural Resources, Olympia,
    WA. 132p.
    """

    def calc_cvts(self, dbh, ht):
        cvtsl = -2.770324 + 1.885813 * np.log10(dbh) + 1.119043 * np.log10(ht)

        cvts = 10**cvtsl
        cvts[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvts

    def calc_tarif(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        cvts = self.calc_cvts(dbh, ht)

        tarif = (cvts * 0.912733) / (
            (1.033 * (1.0 + 1.382937 * np.exp(-4.015292 * dbh)))
            * (ba + 0.087266) - 0.174533)
        tarif[np.logical_or(dbh <= 0, ht <= 0)] = 0

        return tarif

    def calc_cvt(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        tarif = self.calc_tarif(dbh, ht)

        cvt = tarif * (0.9679 - 0.1051 * 0.5523**(dbh - 1.5)) * (
            (1.033 * (1.0 + 1.382937 * np.exp(-4.015292 * (dbh / 10.0))))
            * (ba + 0.087266) - 0.174533) / 0.912733
        cvt[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvt

    def calc_cv4(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        tarif = self.calc_tarif(dbh, ht)

        cv4 = tarif * (ba - 0.087266) / 0.912733
        cv4[np.logical_or(dbh < 5, ht <= 0)] = 0

        return cv4

    def calc_cv8(self, dbh, ht):
        cv4 = self.calc_cv4(dbh, ht)
        rc8 = 0.983 - (0.983 * 0.65**(dbh - 8.6))

        cv8 = rc8 * cv4
        cv8[np.logical_or(dbh < 11, ht <= 0)] = 0

        return cv8


class Eq_31(HardwoodVolumeEquation_NoX):
    """Eucalyptus (MEMO, COLIN D. MacLEAN 1/27/83, (REVISED 2/7/83))

    Colin MacLean and Tom Farrenkopf. 1983. Eucalyptus volume equation.
    In-house memo describing the volume equation for CVTS, to be used for all
    species of Eucalyptus. The equation was developed from 111 trees. On file
    at the PNW Research Station, Portland, OR.
    """

    def calc_cvts(self, dbh, ht):
        cvts = 0.0016144 * dbh**2 * ht
        cvts[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvts

    def calc_tarif(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        cvts = self.calc_cvts(dbh, ht)

        tarif = (cvts * 0.912733) / (
            (1.033 * (1.0 + 1.382937 * np.exp(-4.015292 * dbh)))
            * (ba + 0.087266) - 0.174533)
        tarif[np.logical_or(dbh <= 0, ht <= 0)] = 0

        return tarif

    def calc_cvt(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        tarif = self.calc_tarif(dbh, ht)

        cvt = tarif * (0.9679 - 0.1051 * 0.5523**(dbh - 1.5)) * (
            (1.033 * (1.0 + 1.382937 * np.exp(-4.015292 * (dbh / 10.0))))
            * (ba + 0.087266) - 0.174533) / 0.912733
        cvt[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvt

    def calc_cv4(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        tarif = self.calc_tarif(dbh, ht)

        cv4 = tarif * (ba - 0.087266) / 0.912733
        cv4[np.logical_or(dbh < 5, ht <= 0)] = 0

        return cv4

    def calc_cv8(self, dbh, ht):
        cv4 = self.calc_cv4(dbh, ht)
        rc8 = 0.983 - (0.983 * 0.65**(dbh - 8.6))

        cv8 = rc8 * cv4
        cv8[np.logical_or(dbh < 11, ht <= 0)] = 0

        return cv8


class Eq_32(HardwoodVolumeEquation_WithX):
    """Giant chinquapin (PILLSBURY (H,D), CHARLES BOLSINGER 1/3/83)

    Pillsbury, Norman H. and Michael L. Kirkley. 1984. Equations for Total,
    Wood, and Saw-log Volume for Thirteen California Hardwoods. PNW Research
    Note, PNW-414. Pacific Northwest Research Station, Portland Oregon. 52p.
    """

    def calc_cvts(self, dbh, ht):
        cvts = 0.0120372263 * dbh**2.02232 * ht**0.68638
        cvts[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvts

    def calc_cv4(self, dbh, ht):
        cv4 = 0.0055212937 * dbh**2.07202 * ht**0.77467
        cv4[np.logical_or(dbh < 5, ht <= 0)] = 0

        return cv4

    def calc_cv8(self, dbh, ht):
        cv8 = 0.0018985111 * dbh**2.38285 * ht**0.77105
        cv8[np.logical_or(dbh < 11, ht <= 0)] = 0

        return cv8

    def calc_cvt(self, dbh, ht):
        cvts = self.calc_cvts(dbh, ht)
        rts = 0.9679 - 0.1051 * 0.5523**(dbh - 1.5)

        cvt = cvts * rts
        cvt[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvt

    def calc_tarif(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        cv8 = self.calc_cv8(dbh, ht)

        tarif = (cv8 * 0.912733) / ((0.983 - 0.983 * 0.65**(dbh - 8.6))
                                    * (ba - 0.087266))
        tarif[np.logical_or(dbh <= 0, ht <= 0)] = 0
        return tarif


class Eq_33(HardwoodVolumeEquation_WithX):
    """California laurel (PILLSBURY (H,D), CHARLES BOLSINGER 1/3/83)

    Pillsbury, Norman H. and Michael L. Kirkley. 1984. Equations for Total,
    Wood, and Saw-log Volume for Thirteen California Hardwoods. PNW Research
    Note, PNW-414. Pacific Northwest Research Station, Portland Oregon. 52p.
    """

    def calc_cvts(self, dbh, ht):
        cvts = 0.0057821322 * dbh**1.94553 * ht**0.88389
        cvts[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvts

    def calc_cv4(self, dbh, ht):
        cv4 = 0.0016380753 * dbh**2.05910 * ht**1.05293
        cv4[np.logical_or(dbh < 5, ht <= 0)] = 0

        return cv4

    def calc_cv8(self, dbh, ht):
        cv8 = 0.0018985111 * dbh**2.38285 * ht**0.77105
        cv8[np.logical_or(dbh < 11, ht <= 0)] = 0

        return cv8

    def calc_cvt(self, dbh, ht):
        cvts = self.calc_cvts(dbh, ht)
        rts = 0.9679 - 0.1051 * 0.5523**(dbh - 1.5)

        cvt = cvts * rts
        cvt[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvt

    def calc_tarif(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        cv8 = self.calc_cv8(dbh, ht)

        tarif = (cv8 * 0.912733) / ((0.983 - 0.983 * 0.65**(dbh - 8.6))
                                    * (ba - 0.087266))
        tarif[np.logical_or(dbh <= 0, ht <= 0)] = 0
        return tarif


class Eq_34(HardwoodVolumeEquation_WithX):
    """Tanoak (PILLSBURY (H,D), CHARLES BOLSINGER 1/3/83)

    Pillsbury, Norman H. and Michael L. Kirkley. 1984. Equations for Total,
    Wood, and Saw-log Volume for Thirteen California Hardwoods. PNW Research
    Note, PNW-414. Pacific Northwest Research Station, Portland Oregon. 52p.
    """

    def calc_cvts(self, dbh, ht):
        cvts = 0.0058870024 * dbh**1.94165 * ht**0.86562
        cvts[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvts

    def calc_cv4(self, dbh, ht):
        cv4 = 0.0005774970 * dbh**2.19576 * ht**1.14078
        cv4[np.logical_or(dbh < 5, ht <= 0)] = 0

        return cv4

    def calc_cv8(self, dbh, ht):
        cv8 = 0.0002526443 * dbh**2.30949 * ht**1.21069
        cv8[np.logical_or(dbh < 11, ht <= 0)] = 0

        return cv8

    def calc_cvt(self, dbh, ht):
        cvts = self.calc_cvts(dbh, ht)
        rts = 0.9679 - 0.1051 * 0.5523**(dbh - 1.5)

        cvt = cvts * rts
        cvt[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvt

    def calc_tarif(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        cv8 = self.calc_cv8(dbh, ht)

        tarif = (cv8 * 0.912733) / ((0.983 - 0.983 * 0.65**(dbh - 8.6))
                                    * (ba - 0.087266))
        tarif[np.logical_or(dbh <= 0, ht <= 0)] = 0
        return tarif


class Eq_35(HardwoodVolumeEquation_WithX):
    """California white oak (PILLSBURY (H,D), CHARLES BOLSINGER 1/3/83)

    Pillsbury, Norman H. and Michael L. Kirkley. 1984. Equations for Total,
    Wood, and Saw-log Volume for Thirteen California Hardwoods. PNW Research
    Note, PNW-414. Pacific Northwest Research Station, Portland Oregon. 52p.
    """

    def calc_cvts(self, dbh, ht):
        cvts = 0.0042870077 * dbh**2.33631 * ht**0.74872
        cvts[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvts

    def calc_cv4(self, dbh, ht):
        cv4 = 0.0009684363 * dbh**2.39565 * ht**0.98878
        cv4[np.logical_or(dbh < 5, ht <= 0)] = 0

        return cv4

    def calc_cv8(self, dbh, ht):
        cv8 = 0.0001880044 * dbh**1.87346 * ht**1.62443
        cv8[np.logical_or(dbh < 11, ht <= 0)] = 0

        return cv8

    def calc_cvt(self, dbh, ht):
        cvts = self.calc_cvts(dbh, ht)
        rts = 0.9679 - 0.1051 * 0.5523**(dbh - 1.5)

        cvt = cvts * rts
        cvt[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvt

    def calc_tarif(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        cv8 = self.calc_cv8(dbh, ht)

        tarif = (cv8 * 0.912733) / ((0.983 - 0.983 * 0.65**(dbh - 8.6))
                                    * (ba - 0.087266))
        tarif[np.logical_or(dbh <= 0, ht <= 0)] = 0
        return tarif


class Eq_36(HardwoodVolumeEquation_WithX):
    """Engelmann oak (PILLSBURY (H,D), CHARLES BOLSINGER 1/3/83)

    Pillsbury, Norman H. and Michael L. Kirkley. 1984. Equations for Total,
    Wood, and Saw-log Volume for Thirteen California Hardwoods. PNW Research
    Note, PNW-414. Pacific Northwest Research Station, Portland Oregon. 52p.
    """

    def calc_cvts(self, dbh, ht):
        cvts = 0.0191453191 * dbh**2.40248 * ht**0.28060
        cvts[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvts

    def calc_cv4(self, dbh, ht):
        cv4 = 0.0053866353 * dbh**2.61268 * ht**0.31103
        cv4[np.logical_or(dbh < 5, ht <= 0)] = 0

        return cv4

    def calc_cv8(self, dbh, ht):
        cv8 = self.calc_cv4(dbh, ht)
        cv8[np.logical_or(dbh < 11, ht <= 0)] = 0

        return cv8

    def calc_cvt(self, dbh, ht):
        cvts = self.calc_cvts(dbh, ht)
        rts = 0.9679 - 0.1051 * 0.5523**(dbh - 1.5)

        cvt = cvts * rts
        cvt[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvt

    def calc_tarif(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        cv8 = self.calc_cv8(dbh, ht)

        tarif = (cv8 * 0.912733) / ((0.983 - 0.983 * 0.65**(dbh - 8.6))
                                    * (ba - 0.087266))
        tarif[np.logical_or(dbh <= 0, ht <= 0)] = 0
        return tarif


class Eq_37(HardwoodVolumeEquation_WithX):
    """Bigleaf maple (PILLSBURY (H,D,FC), CHARLES BOLSINGER 1/3/83)

    Pillsbury, Norman H. and Michael L. Kirkley. 1984. Equations for Total,
    Wood, and Saw-log Volume for Thirteen California Hardwoods. PNW Research
    Note, PNW-414. Pacific Northwest Research Station, Portland Oregon. 52p.
    """

    def calc_cvts(self, dbh, ht):
        cvts = 0.0101786350 * dbh**2.22462 * ht**0.57561
        cvts[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvts

    def calc_cv4(self, dbh, ht):
        cv4 = 0.0034214162 * dbh**2.35347 * ht**0.69586
        cv4[np.logical_or(dbh < 5, ht <= 0)] = 0

        return cv4

    def calc_cv8(self, dbh, ht):
        ff = np.piecewise(dbh,
                          condlist=[
                              dbh < 11, (dbh >= 11) & (dbh < 21),
                              (dbh >= 21) & (dbh < 31),
                              (dbh >= 31) & (dbh < 41), dbh >= 41
                          ],
                          funclist=[84, 84, 82, 81, 80])
        ff9ft = 100 + (ff - 100) * (9 - 4.5) / (16 - 4.5)
        diam_9ft = ff9ft / 100.0 * dbh
        fc = np.where((diam_9ft >= 9) & (ht >= 9), 10, 1)

        cv8 = 0.0004236332 * dbh**2.10316 * ht**1.08584 * fc**0.40017
        cv8[np.logical_or(dbh < 11, ht <= 0)] = 0

        return cv8

    def calc_cvt(self, dbh, ht):
        cvts = self.calc_cvts(dbh, ht)
        rts = 0.9679 - 0.1051 * 0.5523**(dbh - 1.5)

        cvt = cvts * rts
        cvt[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvt

    def calc_tarif(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        cv8 = self.calc_cv8(dbh, ht)

        tarif = (cv8 * 0.912733) / ((0.983 - 0.983 * 0.65**(dbh - 8.6))
                                    * (ba - 0.087266))
        tarif[np.logical_or(dbh <= 0, ht <= 0)] = 0
        return tarif


class Eq_38(HardwoodVolumeEquation_WithX):
    """California black oak (PILLSBURY (H,D,FC), CHARLES BOLSINGER 1/3/83)

    Pillsbury, Norman H. and Michael L. Kirkley. 1984. Equations for Total,
    Wood, and Saw-log Volume for Thirteen California Hardwoods. PNW Research
    Note, PNW-414. Pacific Northwest Research Station, Portland Oregon. 52p.
    """

    def calc_cvts(self, dbh, ht):
        cvts = 0.0070538108 * dbh**1.97437 * ht**0.85034
        cvts[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvts

    def calc_cv4(self, dbh, ht):
        cv4 = 0.0036795695 * dbh**2.12635 * ht**0.83339
        cv4[np.logical_or(dbh < 5, ht <= 0)] = 0

        return cv4

    def calc_cv8(self, dbh, ht):
        ff = np.piecewise(dbh,
                          condlist=[
                              dbh < 11, (dbh >= 11) & (dbh < 21),
                              (dbh >= 21) & (dbh < 31),
                              (dbh >= 31) & (dbh < 41), dbh >= 41
                          ],
                          funclist=[95, 95, 84, 82, 82])
        ff9ft = 100 + (ff - 100) * (9 - 4.5) / (16 - 4.5)
        diam_9ft = ff9ft / 100.0 * dbh
        fc = np.where((diam_9ft >= 9) & (ht >= 9), 10, 1)

        cv8 = 0.0012478663 * dbh**2.68099 * ht**0.42441 * fc**0.28385
        cv8[np.logical_or(dbh < 11, ht <= 0)] = 0

        return cv8

    def calc_cvt(self, dbh, ht):
        cvts = self.calc_cvts(dbh, ht)
        rts = 0.9679 - 0.1051 * 0.5523**(dbh - 1.5)

        cvt = cvts * rts
        cvt[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvt

    def calc_tarif(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        cv8 = self.calc_cv8(dbh, ht)

        tarif = (cv8 * 0.912733) / ((0.983 - 0.983 * 0.65**(dbh - 8.6))
                                    * (ba - 0.087266))
        tarif[np.logical_or(dbh <= 0, ht <= 0)] = 0
        return tarif


class Eq_39(HardwoodVolumeEquation_WithX):
    """Blue oak (PILLSBURY (H,D,FC), CHARLES BOLSINGER 1/3/83)

    Pillsbury, Norman H. and Michael L. Kirkley. 1984. Equations for Total,
    Wood, and Saw-log Volume for Thirteen California Hardwoods. PNW Research
    Note, PNW-414. Pacific Northwest Research Station, Portland Oregon. 52p.
    """

    def calc_cvts(self, dbh, ht):
        cvts = 0.0125103008 * dbh**2.33089 * ht**0.46100
        cvts[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvts

    def calc_cv4(self, dbh, ht):
        cv4 = 0.0042324071 * dbh**2.53987 * ht**0.50591
        cv4[np.logical_or(dbh < 5, ht <= 0)] = 0

        return cv4

    def calc_cv8(self, dbh, ht):
        ff = np.piecewise(dbh,
                          condlist=[
                              dbh < 11, (dbh >= 11) & (dbh < 21),
                              (dbh >= 21) & (dbh < 31),
                              (dbh >= 31) & (dbh < 41), dbh >= 41
                          ],
                          funclist=[95, 95, 86, 82, 82])
        ff9ft = 100 + (ff - 100) * (9 - 4.5) / (16 - 4.5)
        diam_9ft = ff9ft / 100.0 * dbh
        fc = np.where((diam_9ft >= 9) & (ht >= 9), 10, 1)

        cv8 = 0.0036912408 * dbh**1.79732 * ht**0.83884 * fc**0.15958
        cv8[np.logical_or(dbh < 11, ht <= 0)] = 0

        return cv8

    def calc_cvt(self, dbh, ht):
        cvts = self.calc_cvts(dbh, ht)
        rts = 0.9679 - 0.1051 * 0.5523**(dbh - 1.5)

        cvt = cvts * rts
        cvt[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvt

    def calc_tarif(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        cv8 = self.calc_cv8(dbh, ht)

        tarif = (cv8 * 0.912733) / ((0.983 - 0.983 * 0.65**(dbh - 8.6))
                                    * (ba - 0.087266))
        tarif[np.logical_or(dbh <= 0, ht <= 0)] = 0
        return tarif


class Eq_40(HardwoodVolumeEquation_WithX):
    """Pacific madrone (PILLSBURY (H,D,FC), CHARLES BOLSINGER 1/3/83)

    Pillsbury, Norman H. and Michael L. Kirkley. 1984. Equations for Total,
    Wood, and Saw-log Volume for Thirteen California Hardwoods. PNW Research
    Note, PNW-414. Pacific Northwest Research Station, Portland Oregon. 52p.
    """

    def calc_cvts(self, dbh, ht):
        cvts = 0.0067322665 * dbh**1.96628 * ht**0.83458
        cvts[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvts

    def calc_cv4(self, dbh, ht):
        cv4 = 0.0025616425 * dbh**1.99295 * ht**1.01532
        cv4[np.logical_or(dbh < 5, ht <= 0)] = 0

        return cv4

    def calc_cv8(self, dbh, ht):
        ff = np.piecewise(dbh,
                          condlist=[
                              dbh < 11, (dbh >= 11) & (dbh < 21),
                              (dbh >= 21) & (dbh < 31),
                              (dbh >= 31) & (dbh < 41), dbh >= 41
                          ],
                          funclist=[95, 86, 82, 79, 79])
        ff9ft = 100 + (ff - 100) * (9 - 4.5) / (16 - 4.5)
        diam_9ft = ff9ft / 100.0 * dbh
        fc = np.where((diam_9ft >= 9) & (ht >= 9), 10, 1)

        cv8 = 0.0006181530 * dbh**1.72635 * ht**1.26462 * fc**0.37868
        cv8[np.logical_or(dbh < 11, ht <= 0)] = 0

        return cv8

    def calc_cvt(self, dbh, ht):
        cvts = self.calc_cvts(dbh, ht)
        rts = 0.9679 - 0.1051 * 0.5523**(dbh - 1.5)

        cvt = cvts * rts
        cvt[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvt

    def calc_tarif(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        cv8 = self.calc_cv8(dbh, ht)

        tarif = (cv8 * 0.912733) / ((0.983 - 0.983 * 0.65**(dbh - 8.6))
                                    * (ba - 0.087266))
        tarif[np.logical_or(dbh <= 0, ht <= 0)] = 0
        return tarif


class Eq_41(HardwoodVolumeEquation_WithX):
    """Oregon white oak (PILLSBURY (H,D,FC), CHARLES BOLSINGER 1/3/83)

    Pillsbury, Norman H. and Michael L. Kirkley. 1984. Equations for Total,
    Wood, and Saw-log Volume for Thirteen California Hardwoods. PNW Research
    Note, PNW-414. Pacific Northwest Research Station, Portland Oregon. 52p.
    """

    def calc_cvts(self, dbh, ht):
        cvts = 0.0072695058 * dbh**2.14321 * ht**0.74220
        cvts[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvts

    def calc_cv4(self, dbh, ht):
        cv4 = 0.0024277027 * dbh**2.25575 * ht**0.87108
        cv4[np.logical_or(dbh < 5, ht <= 0)] = 0

        return cv4

    def calc_cv8(self, dbh, ht):
        ff = np.piecewise(dbh,
                          condlist=[
                              dbh < 11, (dbh >= 11) & (dbh < 21),
                              (dbh >= 21) & (dbh < 31),
                              (dbh >= 31) & (dbh < 41), dbh >= 41
                          ],
                          funclist=[95, 95, 89, 89, 89])
        ff9ft = 100 + (ff - 100) * (9 - 4.5) / (16 - 4.5)
        diam_9ft = ff9ft / 100.0 * dbh
        fc = np.where((diam_9ft >= 9) & (ht >= 9), 10, 1)

        cv8 = 0.0008281647 * dbh**2.10651 * ht**0.91215 * fc**0.32652
        cv8[np.logical_or(dbh < 11, ht <= 0)] = 0

        return cv8

    def calc_cvt(self, dbh, ht):
        cvts = self.calc_cvts(dbh, ht)
        rts = 0.9679 - 0.1051 * 0.5523**(dbh - 1.5)

        cvt = cvts * rts
        cvt[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvt

    def calc_tarif(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        cv8 = self.calc_cv8(dbh, ht)

        tarif = (cv8 * 0.912733) / ((0.983 - 0.983 * 0.65**(dbh - 8.6))
                                    * (ba - 0.087266))
        tarif[np.logical_or(dbh <= 0, ht <= 0)] = 0
        return tarif


class Eq_42(HardwoodVolumeEquation_WithX):
    """Canyon live oak (PILLSBURY (H,D,FC), CHARLES BOLSINGER 1/3/83)

    Pillsbury, Norman H. and Michael L. Kirkley. 1984. Equations for Total,
    Wood, and Saw-log Volume for Thirteen California Hardwoods. PNW Research
    Note, PNW-414. Pacific Northwest Research Station, Portland Oregon. 52p.
    """

    def calc_cvts(self, dbh, ht):
        cvts = 0.0097438611 * dbh**2.20527 * ht**0.61190
        cvts[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvts

    def calc_cv4(self, dbh, ht):
        cv4 = 0.0031670596 * dbh**2.32519 * ht**0.74348
        cv4[np.logical_or(dbh < 5, ht <= 0)] = 0

        return cv4

    def calc_cv8(self, dbh, ht):
        ff = np.piecewise(dbh,
                          condlist=[
                              dbh < 11, (dbh >= 11) & (dbh < 21),
                              (dbh >= 21) & (dbh < 31),
                              (dbh >= 31) & (dbh < 41), dbh >= 41
                          ],
                          funclist=[94, 94, 85, 80, 80])
        ff9ft = 100 + (ff - 100) * (9 - 4.5) / (16 - 4.5)
        diam_9ft = ff9ft / 100.0 * dbh
        fc = np.where((diam_9ft >= 9) & (ht >= 9), 10, 1)

        cv8 = 0.0006540144 * dbh**2.24437 * ht**0.81358 * fc**0.43381
        cv8[np.logical_or(dbh < 11, ht <= 0)] = 0

        return cv8

    def calc_cvt(self, dbh, ht):
        cvts = self.calc_cvts(dbh, ht)
        rts = 0.9679 - 0.1051 * 0.5523**(dbh - 1.5)

        cvt = cvts * rts
        cvt[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvt

    def calc_tarif(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        cv8 = self.calc_cv8(dbh, ht)

        tarif = (cv8 * 0.912733) / ((0.983 - 0.983 * 0.65**(dbh - 8.6))
                                    * (ba - 0.087266))
        tarif[np.logical_or(dbh <= 0, ht <= 0)] = 0
        return tarif


class Eq_43(HardwoodVolumeEquation_WithX):
    """Coast live oak (PILLSBURY (H,D,FC), CHARLES BOLSINGER 1/3/83)

    Pillsbury, Norman H. and Michael L. Kirkley. 1984. Equations for Total,
    Wood, and Saw-log Volume for Thirteen California Hardwoods. PNW Research
    Note, PNW-414. Pacific Northwest Research Station, Portland Oregon. 52p.
    """

    def calc_cvts(self, dbh, ht):
        cvts = 0.0065261029 * dbh**2.31958 * ht**0.62528
        cvts[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvts

    def calc_cv4(self, dbh, ht):
        cv4 = 0.0024574847 * dbh**2.53284 * ht**0.60764
        cv4[np.logical_or(dbh < 5, ht <= 0)] = 0

        return cv4

    def calc_cv8(self, dbh, ht):
        ff = np.piecewise(dbh,
                          condlist=[
                              dbh < 11, (dbh >= 11) & (dbh < 21),
                              (dbh >= 21) & (dbh < 31),
                              (dbh >= 31) & (dbh < 41), dbh >= 41
                          ],
                          funclist=[95, 95, 86, 82, 82])
        ff9ft = 100 + (ff - 100) * (9 - 4.5) / (16 - 4.5)
        diam_9ft = ff9ft / 100.0 * dbh
        fc = np.where((diam_9ft >= 9) & (ht >= 9), 10, 1)

        cv8 = 0.0006540144 * dbh**2.24437 * ht**0.81358 * fc**0.43381
        cv8[np.logical_or(dbh < 11, ht <= 0)] = 0

        return cv8

    def calc_cvt(self, dbh, ht):
        cvts = self.calc_cvts(dbh, ht)
        rts = 0.9679 - 0.1051 * 0.5523**(dbh - 1.5)

        cvt = cvts * rts
        cvt[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvt

    def calc_tarif(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        cv8 = self.calc_cv8(dbh, ht)

        tarif = (cv8 * 0.912733) / ((0.983 - 0.983 * 0.65**(dbh - 8.6))
                                    * (ba - 0.087266))
        tarif[np.logical_or(dbh <= 0, ht <= 0)] = 0
        return tarif


class Eq_44(HardwoodVolumeEquation_WithX):
    """Interior live oak (PILLSBURY (H,D,FC), CHARLES BOLSINGER 1/3/83)

    Pillsbury, Norman H. and Michael L. Kirkley. 1984. Equations for Total,
    Wood, and Saw-log Volume for Thirteen California Hardwoods. PNW Research
    Note, PNW-414. Pacific Northwest Research Station, Portland Oregon. 52p.
    """

    def calc_cvts(self, dbh, ht):
        cvts = 0.0136818837 * dbh**2.02989 * ht**0.63257
        cvts[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvts

    def calc_cv4(self, dbh, ht):
        cv4 = 0.0041192264 * dbh**2.14915 * ht**0.77843
        cv4[np.logical_or(dbh < 5, ht <= 0)] = 0

        return cv4

    def calc_cv8(self, dbh, ht):
        ff = np.piecewise(dbh,
                          condlist=[
                              dbh < 11, (dbh >= 11) & (dbh < 21),
                              (dbh >= 21) & (dbh < 31),
                              (dbh >= 31) & (dbh < 41), dbh >= 41
                          ],
                          funclist=[95, 95, 95, 95, 95])
        ff9ft = 100 + (ff - 100) * (9 - 4.5) / (16 - 4.5)
        diam_9ft = ff9ft / 100.0 * dbh
        fc = np.where((diam_9ft >= 9) & (ht >= 9), 10, 1)

        cv8 = 0.0006540144 * dbh**2.24437 * ht**0.81358 * fc**0.43381
        cv8[np.logical_or(dbh < 11, ht <= 0)] = 0

        return cv8

    def calc_cvt(self, dbh, ht):
        cvts = self.calc_cvts(dbh, ht)
        rts = 0.9679 - 0.1051 * 0.5523**(dbh - 1.5)

        cvt = cvts * rts
        cvt[np.logical_or(dbh < 1, ht <= 0)] = 0

        return cvt

    def calc_tarif(self, dbh, ht):
        ba = 0.005454154 * (dbh**2)
        cv8 = self.calc_cv8(dbh, ht)

        tarif = (cv8 * 0.912733) / ((0.983 - 0.983 * 0.65**(dbh - 8.6))
                                    * (ba - 0.087266))
        tarif[np.logical_or(dbh <= 0, ht <= 0)] = 0
        return tarif


class Eq_45(HardwoodVolumeEquation_WithX):
    """Mountain mahogany (CHOJNACKY, 1985)

    Chojnacky D.C., 1985.  Pinyon-Juniper Volume Equations for the Central
    Rocky Mountain States. Res. Note INT-339, USDA, Forest Service,
    Intermountain Res. Station, Ogden, UT 84401.
    """

    def calc_cvts(self, drc, ht, stems=None):
        if stems is None:
            stems = np.ones_like(drc)
        factor = np.where((drc >= 3) & (ht > 0), drc * drc * ht, 1)
        cvts = np.where(
            stems > 1, (-0.13363 + (0.128222 * (factor**(1. / 3.))))**3,
            (-0.13363 + (0.128222 * (factor**(1. / 3.))) + 0.080208)**3)

        cvts = np.clip(cvts, 0.1, None)
        cvts[np.logical_or(drc < 1, ht <= 0)] = 0

        return cvts


class Eq_46(HardwoodVolumeEquation_WithX):
    """Mesquite (CHOJNACKY, 1985)

    Chojnacky D.C., 1985.  Pinyon-Juniper Volume Equations for the Central
    Rocky Mountain States. Res. Note INT-339, USDA, Forest Service,
    Intermountain Res. Station, Ogden, UT 84401.
    """

    def calc_cvts(self, drc, ht, stems=None):
        if stems is None:
            stems = np.ones_like(drc)
        cvts = np.where(
            drc**2 * ht / 1000 <= 2,
            (-0.043 + 2.3378 * drc**2 * ht / 1000 + 0.8024
             * (drc**2 * ht / 1000)**2),
            9.586 + 2.3378 * drc**2 * ht / 1000 - 12.839 / (drc**2 * ht / 1000)
            )

        mask = np.logical_and(stems > 1, (drc**2 * ht / 1000) <= 2)
        cvts[mask] = (0.020 + 1.8972 * drc[mask]**2 * ht[mask] / 1000 + 0.5756
                      * (drc[mask]**2 * ht[mask] / 1000)**2)

        mask = np.logical_and(stems > 1, (drc**2 * ht / 1000) > 2)
        cvts[mask] = (9.586 + 2.3378 * drc[mask]**2 * ht[mask] / 1000 - 12.839
                      / (drc[mask]**2 * ht[mask] / 1000))

        cvts = np.clip(cvts, 0.1, None)
        cvts[np.logical_or(drc < 1, ht <= 0)] = 0

        return cvts


ALL_EQNS = [
    Eq_1, Eq_2, Eq_3, Eq_4, Eq_5, Eq_6, Eq_7, Eq_8, Eq_9, Eq_10,
    Eq_11, Eq_12, Eq_13, Eq_14, Eq_14_1, Eq_14_2, Eq_15, Eq_16, Eq_17,
    Eq_18, Eq_19, Eq_20, Eq_21, Eq_22, Eq_23, Eq_24, Eq_25, Eq_26,
    Eq_27, Eq_28, Eq_29, Eq_30, Eq_31, Eq_32, Eq_33, Eq_34, Eq_35,
    Eq_36, Eq_37, Eq_38, Eq_39, Eq_40, Eq_41, Eq_42, Eq_43, Eq_44,
    Eq_45, Eq_46
]
