import math


def cairns(aboveground_biomass):
    """
    Calculates belowground biomass as a function of aboveground biomass.
    Derived from "Equation 1" in Cairns, Brown, Helmer & Baumgardner (1997),
    available online at:
    www.arb.ca.gov/cc/capandtrade/protocols/usforest/references/cairns1997.pdf
    Aboveground biomass expected in units of kg, and returns units of kg.
    """
    if aboveground_biomass <= 0:
        return 0
    else:
        return math.exp(-1.085 + 0.9256 * math.log(aboveground_biomass))
