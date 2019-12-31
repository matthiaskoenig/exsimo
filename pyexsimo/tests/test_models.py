"""
Model related tests.
- model creation
- model validation
"""
import os
import pytest
import libsbml
import cobra
from cobra.io import read_sbml_model
from sbmlutils.validation import check_sbml

from pyexsimo.model_factory import create_liver_glucose, create_liver_glucose_const_glycogen
from pyexsimo.tests.utils import get_sbml_files, DOC, MODEL, reaction_ids, species_ids


def test_create_models(tmp_path):
    """ Testing model creation. """
    [_, _, sbml_path] = create_liver_glucose(target_dir=tmp_path)
    assert os.path.exists(sbml_path)
    doc = libsbml.readSBMLFromFile(sbml_path)  # type: libsbml.SBMLDocument
    model = doc.getModel()  # type: libsbml.Model
    assert model


    sbml_path2 = create_liver_glucose_const_glycogen(
        sbml_path=sbml_path, target_dir=tmp_path
    )
    assert os.path.exists(sbml_path2)
    doc = libsbml.readSBMLFromFile(sbml_path2)  # type: libsbml.SBMLDocument
    model = doc.getModel()  # type: libsbml.Model
    assert model


@pytest.mark.parametrize("sbml_path", get_sbml_files())
def test_model_exists(sbml_path):
    """ Testing that a model exists in the SBML file."""
    assert os.path.exists(sbml_path)
    doc = libsbml.readSBMLFromFile(sbml_path)  # type: libsbml.SBMLDocument
    model = doc.getModel()  # type: libsbml.Model
    assert model

@pytest.mark.parametrize("sbml_path", get_sbml_files())
def test_model_is_valid(sbml_path):
    """ Testing that all models in the repository are valid, i.e. no
    SBML errors. """
    _, Nerr, _ = check_sbml(sbml_path)
    assert Nerr == 0


@pytest.mark.parametrize("sbml_path", get_sbml_files())
def test_model_no_warnings(sbml_path):
    """ Testing that all models in the repository are valid, i.e. no
    SBML errors. """
    Nall, Nerr, Nwarn = check_sbml(sbml_path)
    assert Nerr == 0
    assert Nwarn == 0
    assert Nall == 0


@pytest.mark.parametrize("sid", species_ids())
def test_specie_has_formula(sid):
    specie = MODEL.getSpecies(sid)  # type: libsbml.Species
    fbc_specie = specie.getPlugin("fbc")  # type: libsbml.FbcSpeciesPlugin
    assert fbc_specie.getChemicalFormula()


@pytest.mark.parametrize("sid", species_ids())
def test_specie_has_charge(sid):
    specie = MODEL.getSpecies(sid)  # type: libsbml.Species
    fbc_specie = specie.getPlugin("fbc")  # type: libsbml.FbcSpeciesPlugin
    assert fbc_specie.getCharge() is not None


COBRA_MODEL = read_sbml_model(libsbml.writeSBMLToString(DOC))


@pytest.mark.parametrize("sid", reaction_ids())
def test_reaction_mass_balance(sid):
    """Test mass balance of all reactions."""
    if sid not in ['OAAFLX', 'CITFLX', 'ACOAFLX']:
        # don't check pseudoreactions
        reaction = COBRA_MODEL.reactions.get_by_id(sid)
        balance = reaction.check_mass_balance()
        if len(balance) > 0:
            print(reaction, balance)
        assert len(balance) == 0
