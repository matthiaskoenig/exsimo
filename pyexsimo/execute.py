"""
Entry point to run the complete analysis
"""
from pyexsimo import MODEL_PATH
from pyexsimo import __version__
from pyexsimo.model_factory import create_liver_glucose, create_liver_glucose_const_glycogen

import logging
from sbmlsim.experiment import run_experiment

from pyexsimo import MODEL_PATH, DATA_PATH, RESULT_PATH
from pyexsimo.experiments.dose_response import DoseResponseExperiment
from pyexsimo.experiments.hgp_gng import PathwayExperiment
from pyexsimo.experiments.glycogen import GlycogenExperiment
from pyexsimo.experiments.hgp_gng_ss import PathwaySSExperiment

logger = logging.getLogger(__name__)

class bcolors:
    """ Colors for styling log. """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BGWHITE = '\033[47m'
    BGBLACK = '\033[49m'
    WHITE = '\033[37m'
    BLACK = '\033[30m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def run_experiments(show_figures=False):
    """Run all simulation experiments"""
    for exp_class in [DoseResponseExperiment, PathwayExperiment, GlycogenExperiment]:
        run_experiment(exp_class,
                       output_path=RESULT_PATH,
                       model_path=MODEL_PATH / "liver_glucose.xml",
                       data_path=DATA_PATH,
                       show_figures=show_figures)

    run_experiment(PathwaySSExperiment,
                   output_path=RESULT_PATH,
                   model_path=MODEL_PATH / "liver_glucose_const_glyglc.xml",
                   data_path=DATA_PATH,
                   show_figures=show_figures)


def execute(show_figures=False):
    """ Execute simulation model.

    Creates all SBML model and runs all simulation experiments defined for the
    model. Creates models in ./models folder and results in ./results folder.
    """
    logger.info("#" * 80)
    logger.info(f"Execute simulation model: Version {__version__}")
    logger.info("#" * 80)

    # create models
    logger.info("-" * 80)
    logger.info("Create models")
    logger.info("-" * 80)
    [_, _, sbml_path] = create_liver_glucose(target_dir=MODEL_PATH)
    create_liver_glucose_const_glycogen(sbml_path, target_dir=MODEL_PATH)

    # run experiments
    logger.info("-" * 80)
    logger.info("Run simulation experiments")
    logger.info("-" * 80)

    run_experiments(show_figures=show_figures)

    logger.info('-' * 80)
    logger.info(f"{bcolors.OKGREEN}Successfully executed simulation model{bcolors.ENDC}")
    logger.info('-' * 80)


if __name__ == "__main__":
    execute(show_figures=True)
