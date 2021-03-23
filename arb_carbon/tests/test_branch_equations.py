import unittest
import numpy as np

from arb_carbon.equations.live_branch_biomass import ALL_EQNS


class TestBranchEqs(unittest.TestCase):
    """Tests that evaluate the branch biomass equations."""

    def test_negatives(self, eqns='all'):
        """
        Tests whether branch biomass equations return negative values across a
        range of diameter and height inputs.

        Parameters
        ----------
        eqns : str or list of volume equations
          equations to be tested. If 'all' (default), then all volume equations
          will be graphed. Otherwise, a list-like of uninstantiated equation
          classes should be passed.
        """
        if eqns.lower() == 'all':
            test_eq = ALL_EQNS
        else:
            test_eq = eqns

        dbhs = np.arange(0, 100, 1)
        hts = np.arange(0, 400, 1)
        x, y = np.meshgrid(dbhs, hts)

        for eqn in test_eq:
            name = eqn.__name__
            # silence divide by zero warnings
            with np.errstate(divide='ignore', invalid='ignore'):
                bio = eqn().calc(x.ravel(), y.ravel())
                msg = f'{name} produced negative branch biomass'
                self.assertTrue((bio < 0).sum() == 0, msg=msg)


if __name__ == '__main__':
    unittest.main()
