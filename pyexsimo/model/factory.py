import os
from sbmlutils.modelcreator import creator
from pyexsimo import MODEL_PATH


def create_liver_glucose():
    """Create the SBML model"""
    return creator.create_model(
        modules=['liver_glucose'],
        filename="liver_glucose.xml",
        target_dir=MODEL_PATH,
        annotations=os.path.join(os.path.dirname(__file__), 'liver_model_detailed.xlsx'),
        create_report=True
    )


if __name__ == "__main__":
    create_liver_glucose()
