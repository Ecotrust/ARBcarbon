"""
Tests for arb_carbon/equations/volume.py
"""
import unittest
import numpy as np
from mpl_toolkits.mplot3d import axes3d
from matplotlib import pyplot as plt

from arb_carbon.equations.volume import ALL_EQNS


def graph_equations(eqns='all', metrics=['CVTS']):
    '''
    Creates 3-D graphs dipslaying the requested volume metric(s) across a
    range of tree diameters and heights.

    Parameters
    ----------
    eqns : str or list of volume equations
      equations to be tested. If 'all' (default), then all volume equations
      will be graphed. Otherwise, a list-like of uninstantiated volume
      equation classes should be passed.

    metrics : list-like
      list with strings indicating the metric(s) to be graphed.
    '''
    if equations.lower() == 'all':
        test_eq = [
            Eq_1, Eq_2, Eq_3, Eq_4, Eq_5, Eq_6, Eq_7, Eq_8, Eq_9, Eq_10,
            Eq_11, Eq_12, Eq_13, Eq_14, Eq_141, Eq_142, Eq_15, Eq_16, Eq_17,
            Eq_18, Eq_19, Eq_20, Eq_21, Eq_22, Eq_23, Eq_24, Eq_25, Eq_26,
            Eq_27, Eq_28, Eq_29, Eq_30, Eq_31, Eq_32, Eq_33, Eq_34, Eq_35,
            Eq_36, Eq_37, Eq_38, Eq_39, Eq_40, Eq_41, Eq_42, Eq_43, Eq_44,
            Eq_45, Eq_46
            ]

    else:
        test_eq = equations

    for metric in metrics:
        for eqn in test_eq:
            dbhs = np.arange(0, 100, 1)
            hts = np.arange(0, 400, 10)

            xx, yy = np.meshgrid(dbhs, hts)
            z = eqn().calc_vol(xx, yy, metric=metric)

            fig = plt.figure()
            ax = fig.gca(projection='3d')
            ax.scatter(xx, yy, z)
            ax.set_xlabel('DBH (in)')
            ax.set_ylabel('HT (ft)')
            ax.set_zlabel(metric)
            ax.set_title(eqn.__name__)
            ax.set_xlim(0, 100)
            ax.set_ylim(0, 400)
            ax.set_zlim(zmin=0)
            plt.show()


class TestVolumeEqs(unittest.TestCase):
    """Tests that evaluate the volume equations."""

    def test_negatives(self, eqns='all', metrics=['CVTS']):
        '''
        Tests whether volume equations return negative values across a range of
        diameter and height inputs.

        Parameters
        ----------
        eqns : str or list of volume equations
          equations to be tested. If 'all' (default), then all volume equations
          will be graphed. Otherwise, a list-like of uninstantiated volume
          equation classes should be passed.

        metrics : list-like
          list with strings indicating the metric(s) to be graphed.
        '''
        if eqns.lower() == 'all':
            test_eq = ALL_EQNS
        else:
            test_eq = eqns

        dbhs = np.arange(0, 100, 1)
        hts = np.arange(0, 400, 1)
        x, y = np.meshgrid(dbhs, hts)

        for metric in metrics:
            for eqn in test_eq:
                name = eqn.__name__
                # silence divide by zero warnings
                with np.errstate(divide='ignore', invalid='ignore'):
                    vols = eqn().calc_vol(x.ravel(), y.ravel(), metric=metric)
                    msg = f'{name} produced negative values for {metric}'
                    self.assertTrue((vols < 0).sum() == 0, msg)


if __name__ == '__main__':
    unittest.main()
