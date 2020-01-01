import pytest
import os
from sbmlsim.experiment import run_experiment

from pyexsimo.report import create_report
from pyexsimo.experiments.glycogen import GlycogenExperiment
from pyexsimo import MODEL_PATH, DATA_PATH


def test_report(tmp_path):
    results = []
    info = run_experiment(GlycogenExperiment,
                          output_path=tmp_path,
                          model_path=MODEL_PATH / "liver_glucose.xml",
                          data_path=DATA_PATH,
                          show_figures=False)
    results.append(info)

    create_report(results, tmp_path)
    assert os.path.exists(tmp_path / "index.md")
    assert os.path.exists(tmp_path / f"{info['experiment'].sid}.md")
