"""
Entry point to run the complete analysis
"""
from pyexsimo import MODEL_PATH
from pyexsimo import __version__
from pyexsimo.model_factory import create_liver_glucose, \
    create_liver_glucose_const_glycogen
from pyexsimo.report import create_report

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
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


def run_experiments(output_path, show_figures=False, ):
    """Run all simulation experiments"""
    results = []
    for exp_class in [DoseResponseExperiment, PathwayExperiment,
                      GlycogenExperiment]:
        info = run_experiment(exp_class,
                              output_path=output_path,
                              model_path=MODEL_PATH / "liver_glucose.xml",
                              data_path=DATA_PATH,
                              show_figures=show_figures)
        results.append(info)

    info = run_experiment(PathwaySSExperiment,
                          output_path=output_path,
                          model_path=MODEL_PATH / "liver_glucose_const_glyglc.xml",
                          data_path=DATA_PATH,
                          show_figures=show_figures)
    results.append(info)
    return results


def execute(output_path=RESULT_PATH, model_output_path=MODEL_PATH,
            show_figures=False):
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
    [_, _, sbml_path] = create_liver_glucose(target_dir=model_output_path)
    create_liver_glucose_const_glycogen(sbml_path, target_dir=model_output_path)

    # run experiments
    logger.info("-" * 80)
    logger.info("Run simulation experiments")
    logger.info("-" * 80)
    results = run_experiments(output_path=output_path,
                              show_figures=show_figures)

    # create report
    logger.info("-" * 80)
    logger.info("Create report")
    logger.info("-" * 80)
    create_report(results, output_path=output_path)

    logger.info('-' * 80)
    logger.info(
        f"{bcolors.OKGREEN}Successfully executed simulation model{bcolors.ENDC}")
    logger.info('-' * 80)


if __name__ == "__main__":
    execute(show_figures=True)
