import os
from sbmlutils.modelcreator import creator
from sbmlutils.report import sbmlreport
import libsbml
from pyexsimo import MODEL_PATH


def create_liver_glucose():
    """Create the SBML model"""
    return creator.create_model(
        modules=['liver_glucose'],
        filename="liver_glucose.xml",
        target_dir=MODEL_PATH,
        annotations=os.path.join(os.path.dirname(__file__), 'liver_glucose_annotations.xlsx'),
        create_report=True
    )

def create_liver_glucose_const_glycogen(sbml_path, model_dir=MODEL_PATH):
    """Modifies the model with constant glycogen."""

    suffix = "_const_glyglc"
    doc = libsbml.readSBMLFromFile(str(sbml_path))  # type: libsbml.SBMLDocument
    model = doc.getModel()

    # set glycogen constant (boundary Condition)
    s_glyglc = model.getSpecies('glyglc')
    s_glyglc.setBoundaryCondition(True)
    model.setId(model.getId() + suffix)
    sbml_path_new = str(sbml_path)[:-4] + suffix + '.xml'
    libsbml.writeSBMLToFile(doc, sbml_path_new)

    sbmlreport.create_report(sbml_path_new, report_dir=str(MODEL_PATH))


if __name__ == "__main__":
    [_, _, sbml_path] = create_liver_glucose()
    create_liver_glucose_const_glycogen(sbml_path)
