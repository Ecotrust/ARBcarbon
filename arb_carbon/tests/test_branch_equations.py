import unittest
import numpy as np

from arb_carbon.equations.live_branch_biomass import ALL_EQNS


class TestBranchEqs(unittest.TestCase):
    """Tests that evaluate the branch biomass equations."""

    def test_negatives(self):
        """
        Tests whether branch biomass equations return negative values across a
        range of diameter and height inputs.
        """
        dbhs = np.arange(0, 100, 1)
        hts = np.arange(0, 400, 1)
        x, y = np.meshgrid(dbhs, hts)

        for eqn in ALL_EQNS:
            name = eqn.__name__
            # silence divide by zero warnings
            with np.errstate(divide='ignore', invalid='ignore'):
                bio = eqn().calc(x.ravel(), y.ravel())
                msg = f'{name} produced negative branch biomass'
                self.assertTrue((bio < 0).sum() == 0, msg=msg)


if __name__ == '__main__':
    unittest.main()
