"""
Test running all simulation experiments.
These tests reproduce the complete analysis.
"""
import pytest

from sbmlsim.experiment import run_experiment

from pyexsimo import MODEL_PATH, DATA_PATH
from pyexsimo.experiments.dose_response import DoseResponseExperiment
from pyexsimo.experiments.hgp_gng import PathwayExperiment
from pyexsimo.experiments.glycogen import GlycogenExperiment
from pyexsimo.experiments.hgp_gng_ss import PathwaySSExperiment


@pytest.mark.parametrize("exp_class", [DoseResponseExperiment, PathwayExperiment, GlycogenExperiment])
def test_experiments(exp_class, tmp_path):
    run_experiment(
        exp_class,
        output_path=tmp_path,
        model_path=MODEL_PATH / "liver_glucose.xml",
        data_path=DATA_PATH
    )


@pytest.mark.parametrize("exp_class", [PathwaySSExperiment])
def test_experiments_const_glycogen(exp_class, tmp_path):
    run_experiment(
        exp_class,
        output_path=tmp_path,
        model_path=MODEL_PATH / "liver_glucose_const_glyglc.xml",
        data_path=DATA_PATH
    )
