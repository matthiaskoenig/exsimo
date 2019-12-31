"""Model factory.

Creates all SBML models from model definitions in sbmlutils.
"""
import os
from sbmlutils.modelcreator import creator
from sbmlutils.report import sbmlreport
import libsbml
from pyexsimo import MODEL_PATH


def create_liver_glucose(target_dir):
    """Create the SBML model"""

    # external annotation file
    annotations_path = os.path.join(
        os.path.dirname(__file__),
        'liver_glucose_annotations.xlsx'
    )

    return creator.create_model(
        modules=['pyexsimo.models.liver_glucose'],
        filename="liver_glucose.xml",
        target_dir=target_dir,
        annotations=annotations_path,
        create_report=True
    )


def create_liver_glucose_const_glycogen(sbml_path, target_dir=MODEL_PATH):
    """Modifies the glucose model with constant glycogen.

    For some of the simulations the glycogen concentration ([glyglc])
    is clamped in the model. In SBML this requires a model modification via
    setting the boundaryCondition=True.
    The original model is modified accordingly and a second model is
    generated.
    """
    suffix = "_const_glyglc"
    doc = libsbml.readSBMLFromFile(str(sbml_path))  # type: libsbml.SBMLDocument
    model = doc.getModel()

    # set glycogen constant (boundary Condition)
    s_glyglc = model.getSpecies('glyglc')
    s_glyglc.setBoundaryCondition(True)
    model.setId(model.getId() + suffix)

    # FIXME: get folder
    _, filename = os.path.split(str(sbml_path))
    sbml_path_new = os.path.join(target_dir, f"{filename[:-4]}{suffix}.xml")
    libsbml.writeSBMLToFile(doc, sbml_path_new)

    sbmlreport.create_report(sbml_path_new, report_dir=str(MODEL_PATH))


if __name__ == "__main__":

    [_, _, sbml_path] = create_liver_glucose(target_dir=MODEL_PATH)
    create_liver_glucose_const_glycogen(sbml_path, target_dir=MODEL_PATH)
