"""
Check that all models are simulatable.
"""
import os
import pytest
import roadrunner
import pandas as pd

from pyexsimo import BASE_PATH
from pyexsimo.tests.utils import get_sbml_files
GLUCOSE_MODEL = BASE_PATH / "liver_glucose.xml"


@pytest.mark.parametrize("sbml_path", get_sbml_files())
def test_simulate_timecourse(sbml_path):
    """ Test that all models allow timecourse simulations."""

    r = roadrunner.RoadRunner(sbml_path)
    s = r.simulate(0, 100, steps=100)
    assert s

@pytest.mark.parametrize("sbml_path", get_sbml_files())
def test_species_nonnegative(sbml_path):
    """ Test that all model species are non-negative."""

    r = roadrunner.RoadRunner(sbml_path)  # type: roadrunner.RoadRunner
    s = r.simulate(0, 100, steps=100)
    df = pd.DataFrame(s, columns=s.colnames)
    model = r.model  # type: roadrunner.ExecutableModel
    for sid in [model.getFloatingSpeciesIds() + model.getBoundarySpeciesIds()]:
        # check that no negative values in timecourse for species
        assert sum(df[sid] < 0.0) == 0


@pytest.mark.parametrize("sid_tot", ['nadh_tot', 'atp_tot', 'utp_tot', 'gtp_tot', 'nadh_mito_tot', 'atp_mito_tot', 'gtp_mito_tot'])
def test_cofactor_bilances(sid_tot):
    """ Test that main cofactors are bilanced during timecourse simulation."""
    r = roadrunner.RoadRunner(str(GLUCOSE_MODEL))  # type: roadrunner.RoadRunner
    s = r.simulate(0, 100, steps=100)
    df = pd.DataFrame(s, columns=s.colnames)

    for k in range(len(df)):
        assert df[sid_tot].values[0] == df[sid_tot].values[k]

