import unittest
import numpy as np

from arb_carbon.equations.bark_biomass import ALL_EQNS


class TestBarkEqs(unittest.TestCase):
    """Tests that evaluate the bark biomass equations."""

    def test_negatives(self):
        """
        Tests whether bark biomass equations return negative values across a
        range of diameter and height inputs.
        """
        dbhs = np.arange(0, 100, 1)
        hts = np.arange(0, 400, 1)
        x, y = np.meshgrid(dbhs, hts)
        wood_dens = np.full(x.ravel().shape, 25.0)

        for eqn in ALL_EQNS:
            name = eqn.__name__
            # silence divide by zero warnings
            with np.errstate(divide='ignore', invalid='ignore'):
                bio = eqn().calc(dbh=x.ravel(), ht=y.ravel(),
                                 wood_density=wood_dens)
                msg = f'{name} produced negative bark biomass'
                self.assertTrue((bio < 0).sum() == 0, msg=msg)


if __name__ == '__main__':
    unittest.main()
