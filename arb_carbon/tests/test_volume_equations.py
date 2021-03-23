"""
Tests for arb_carbon/equations/volume.py
"""
import unittest
import numpy as np

from arb_carbon.equations.volume import ALL_EQNS


def graph_equations(metrics=['CVTS']):
    '''
    Creates 3-D graphs dipslaying the requested volume metric(s) across a
    range of tree diameters and heights.

    Parameters
    ----------
    metrics : list-like
      list with strings indicating the metric(s) to be graphed.
    '''
    from mpl_toolkits.mplot3d import axes3d
    from matplotlib import pyplot as plt

    for metric in metrics:
        for eqn in ALL_EQNS:
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

    def test_negatives(self, metrics=['CVTS']):
        '''
        Tests whether volume equations return negative values across a range of
        diameter and height inputs.

        Parameters
        ----------
        metrics : list-like
          list with strings indicating the metric(s) should be tested.
        '''
        dbhs = np.arange(0, 100, 1)
        hts = np.arange(0, 400, 1)
        x, y = np.meshgrid(dbhs, hts)

        for metric in metrics:
            for eqn in ALL_EQNS:
                name = eqn.__name__
                # silence divide by zero warnings
                with np.errstate(divide='ignore', invalid='ignore'):
                    vols = eqn().calc_vol(x.ravel(), y.ravel(), metric=metric)
                    msg = f'{name} produced negative values for {metric}'
                    self.assertTrue((vols < 0).sum() == 0, msg)


if __name__ == '__main__':
    unittest.main()
