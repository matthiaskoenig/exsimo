"""
Helper functions for testing.
"""
import os
from pyexsimo import MODEL_PATH


def get_sbml_files(model_dir=MODEL_PATH):
    """Get all SBML files from given directory path."""
    sbml_files = []
    for f in os.listdir(model_dir):
        path = os.path.join(model_dir, f)
        if os.path.isfile(path) and f.endswith('.xml'):
            sbml_files.append(path)
    return sbml_files
