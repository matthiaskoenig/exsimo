import logging
from sbmlsim.experiment import run_experiment

from pyexsimo import MODEL_PATH, DATA_PATH, RESULT_PATH
from pyexsimo.experiments.dose_response import DoseResponseExperiment
from pyexsimo.experiments.hgp_gng import PathwayExperiment
from pyexsimo.experiments.glycogen import GlycogenExperiment

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # exp_classes = [DoseResponseExperiment, PathwayExperiment, GlycogenExperiment]
    exp_classes = [PathwayExperiment]
    for exp_class in exp_classes:
        run_experiment(exp_class,
                       output_path=RESULT_PATH,
                       model_path=MODEL_PATH / "liver_glucose.xml",
                       data_path=DATA_PATH)
