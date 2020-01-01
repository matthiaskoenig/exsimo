"""
Create markdown report of simulation experiments.
"""
import sys
import os
import logging
import jinja2

from pyexsimo import TEMPLATE_PATH, BASE_PATH
from pyexsimo import __version__

logger = logging.getLogger(__name__)


def create_report(results, output_path):
    """ Creates markdown files results."""
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(str(TEMPLATE_PATH)),
                             extensions=['jinja2.ext.autoescape'],
                             trim_blocks=True,
                             lstrip_blocks=True)

    exp_ids = []
    for item in results:
        exp = item['experiment']
        exp_id = exp.sid
        exp_ids.append(exp_id)

        # relative paths to output path
        model_path = os.path.relpath(str(item['model_path']), output_path)
        report_path = f"{model_path[:-4]}.html"
        data_path = os.path.relpath(str(item['data_path']), output_path)

        code_path = sys.modules[exp.__module__].__file__
        with open(code_path, "r") as f_code:
            code = f_code.read()
        code_path = os.path.relpath(code_path, BASE_PATH.parent)
        code_path = "https:/" + os.path.join("/github.com/matthiaskoenig/exsimo/tree/master/", code_path)
        print(code_path)

        context = {
            'exp_id': exp_id,
            'model_path': model_path,
            'report_path': report_path,
            'data_path': data_path,
            'datasets': sorted(exp.datasets.keys()),
            'figures': sorted(exp.figures.keys()),
            'code_path': code_path,
            'code': code,
        }
        template = env.get_template('experiment.md')
        md = template.render(context)
        md_file = output_path / f'{exp_id}.md'
        with open(md_file, "w") as f_index:
            f_index.write(md)
            logger.info(f"Create '{md_file}'")

    context = {
        'version': __version__,
        'exp_ids': exp_ids,
    }
    template = env.get_template('index.md')
    md = template.render(context)
    md_file = output_path / 'index.md'
    with open(md_file, "w") as f_index:
        f_index.write(md)
        logger.info(f"Create '{md_file}'")


if __name__ == "__main__":

    from pyexsimo.experiments.glycogen import GlycogenExperiment
    from pyexsimo import RESULT_PATH, MODEL_PATH, DATA_PATH

    from sbmlsim.experiment import run_experiment

    results = []
    info = run_experiment(GlycogenExperiment,
                   output_path=RESULT_PATH,
                   model_path=MODEL_PATH / "liver_glucose.xml",
                   data_path=DATA_PATH,
                   show_figures=False)
    results.append(info)

    create_report(results, output_path=RESULT_PATH)



