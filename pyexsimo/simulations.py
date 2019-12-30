import logging
from sbmlsim.experiment import run_experiment

from pyexsimo import MODEL_PATH, DATA_PATH, RESULT_PATH
from pyexsimo.experiments.dose_response import DoseResponseExperiment
from pyexsimo.experiments.hgp_gng import PathwayExperiment
from pyexsimo.experiments.glycogen import GlycogenExperiment
from pyexsimo.experiments.hgp_gng_ss import PathwaySSExperiment

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    if False:
        for exp_class in [DoseResponseExperiment, PathwayExperiment, GlycogenExperiment]:
            run_experiment(exp_class,
                           output_path=RESULT_PATH,
                           model_path=MODEL_PATH / "liver_glucose.xml",
                           data_path=DATA_PATH)

    run_experiment(PathwaySSExperiment,
                   output_path=RESULT_PATH,
                   model_path=MODEL_PATH / "liver_glucose_const_glyglc.xml",
                   data_path=DATA_PATH)
