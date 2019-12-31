"""
Helper functions for testing.
"""
import os
import libsbml

from pyexsimo import MODEL_PATH
DOC = libsbml.readSBMLFromFile(str(MODEL_PATH / "liver_glucose.xml"))  # type: libsbml.SBMLDocument
MODEL = DOC.getModel()  # type: libsbml.Model


def compartment_ids():
    return [sbase.getId() for sbase in MODEL.getListOfCompartments()]

def species_ids():
    return [sbase.getId() for sbase in MODEL.getListOfSpecies()]

def parameter_ids():
    return [sbase.getId() for sbase in MODEL.getListOfParameters()]

def reaction_ids():
    return [sbase.getId() for sbase in MODEL.getListOfReactions()]


def get_sbml_files(model_dir=MODEL_PATH):
    """Get all SBML files from given directory path."""
    sbml_files = []
    for f in os.listdir(model_dir):
        path = os.path.join(model_dir, f)
        if os.path.isfile(path) and f.endswith('.xml'):
            sbml_files.append(path)
    return sbml_files
