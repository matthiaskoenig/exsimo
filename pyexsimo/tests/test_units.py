"""
Check existence of units.
Integrative unit tests are performed as part of the model validation,
i.e., complete unit checking of all math.
"""
import pytest
import libsbml

from pyexsimo.tests.utils import MODEL, compartment_ids, species_ids, parameter_ids


@pytest.mark.parametrize("sid", species_ids())
def test_specie_has_substance_units(sid):
    specie = MODEL.getSpecies(sid)  # type: libsbml.Species
    assert specie.getSubstanceUnits()


@pytest.mark.parametrize("sid", compartment_ids())
def test_compartment_has_units(sid):
    compartment = MODEL.getCompartment(sid)  # type: libsbml.Compartment
    assert compartment.getUnits()


@pytest.mark.parametrize("sid", parameter_ids())
def test_parameter_has_units(sid):
    parameter = MODEL.getParameter(sid)  # type: libsbml.Parameter
    assert parameter.getUnits()
