import pytest
from pyexsimo.model_factory import create_liver_glucose, create_liver_glucose_const_glycogen


def test_model_creation_liver_glucose(tmp_path):
    create_liver_glucose()