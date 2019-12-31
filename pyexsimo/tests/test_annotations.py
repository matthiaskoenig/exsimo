"""
Check annotations of the model objects.
"""
import pytest
import libsbml
from pyexsimo import MODEL_PATH

DOC = libsbml.readSBMLFromFile(str(MODEL_PATH / "liver_glucose.xml"))  # type: libsbml.SBMLDocument
MODEL = DOC.getModel()  # type: libsbml.Model


def species_ids():
    return [specie.getId() for specie in MODEL.getListOfSpecies()]

def reaction_ids():
    return [reaction.getId() for reaction in MODEL.getListOfReactions()]

def test_document_has_sbo():
    assert DOC.isSetSBOTerm()
    assert DOC.getSBOTerm() == 293

@pytest.mark.parametrize("sid", species_ids())
def test_specie_has_sbo(sid):
    assert MODEL.getSpecies(sid).isSetSBOTerm()


@pytest.mark.parametrize("sid", reaction_ids())
def test_reaction_has_sbo(sid):
    assert MODEL.getReaction(sid).isSetSBOTerm()


def test_model_has_cvterms():
    assert MODEL.getNumCVTerms() > 0


@pytest.mark.parametrize("sid", species_ids())
def test_specie_has_cvterms(sid):
    assert MODEL.getSpecies(sid).getNumCVTerms() > 0


@pytest.mark.parametrize("sid", reaction_ids())
def test_reaction_has_cvterms(sid):
    if sid in ['OAAFLX', 'ACOAFLX', 'CITFLX']:
        # pseudo-reactions do not need cvterms
        pass
    else:
        assert MODEL.getReaction(sid).getNumCVTerms() > 0


def _check_annotation(sbase: libsbml.SBase, resource: str):
    """Checks if SBase object has given annotation."""
    # f = lambda s: s.startswith(f"https://identifiers.org/{resource}/")
    f = lambda s: resource in s
    for cvterm in sbase.getCVTerms():
        for k in range(cvterm.getNumResources()):
            resource_uri = cvterm.getResourceURI(k)
            if f(resource_uri):
                return

    assert False


@pytest.mark.parametrize("sid", species_ids())
def test_specie_has_chebi(sid):
    _check_annotation(MODEL.getSpecies(sid), "chebi")

@pytest.mark.parametrize("sid", species_ids())
def test_specie_has_inchikey(sid):
    if sid not in ["glyglc"]:
        _check_annotation(MODEL.getSpecies(sid), "inchikey")

@pytest.mark.parametrize("sid", species_ids())
def test_specie_has_kegg_compound(sid):
    _check_annotation(MODEL.getSpecies(sid), "kegg.compound")

@pytest.mark.parametrize("sid", reaction_ids())
def test_reaction_has_uniprot(sid):
    if sid not in ["NDKGTP", "NDKUTP", "AK", "PYRTM", "PEPTM", "NDKGTPM", "OAAFLX", "ACOAFLX", "CITFLX"]:
        # many isoforms, transporters, pseudoreactions not annotated
        _check_annotation(MODEL.getReaction(sid), "uniprot")

@pytest.mark.parametrize("sid", reaction_ids())
def test_reaction_has_go(sid):
    if sid not in ["OAAFLX", "ACOAFLX", "CITFLX"]:
        # pseudoreactions not annotated
        _check_annotation(MODEL.getReaction(sid), "go")

@pytest.mark.parametrize("sid", reaction_ids())
def test_reaction_has_ec(sid):
    if sid not in ["GLUT2", "LACT", "PYRTM", "PEPTM", "OAAFLX", "ACOAFLX", "CITFLX"]:
        # transporters, pseudoreactions not annotated
        _check_annotation(MODEL.getReaction(sid), "ec-code")

@pytest.mark.parametrize("sid", reaction_ids())
def test_reaction_has_rhea(sid):
    if sid not in ["GLUT2", "LACT", "PYRTM", "PEPTM", "OAAFLX", "ACOAFLX", "CITFLX"]:
        # transporters, pseudoreactions not annotated
        _check_annotation(MODEL.getReaction(sid), "rhea")

@pytest.mark.parametrize("sid", reaction_ids())
def test_reaction_has_pr(sid):
    if sid not in ["NDKGTP", "NDKUTP", "AK", "PYRTM", "PEPTM", "NDKGTPM", "OAAFLX", "ACOAFLX", "CITFLX"]:
        # many isoforms, transporters, pseudoreactions not annotated
        _check_annotation(MODEL.getReaction(sid), "pr/PR:")