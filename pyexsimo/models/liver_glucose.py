# -*- coding=utf-8 -*-
"""
Hepatic glucose model (Koenig 2012).

Definition of units is done by defining the main_units of the model in
addition with the definition of the individual units of the model.

"""
from copy import deepcopy

from sbmlutils.units import *
from sbmlutils.annotation.sbo import *
from sbmlutils.factory import *

from pyexsimo.models import templates

# -----------------------------------------------------------------------------
# Liver Metabolism
# -----------------------------------------------------------------------------
mid = 'liver_glucose'
version = 8
# -----------------------------------------------------------------------------
creators = [templates.CREATORS[0]]
notes = Notes([
    """
    <h1>Koenig Human Glucose Metabolism</h1>
    <h2>Description</h2>
    <p>
        This is a metabolism model of Human glucose metabolism in <a href="http://sbml.org">SBML</a> format.
    </p>
    <p>This model is based on the model described in the article:</p>
    <div class="bibo:title">
        <a href="http://identifiers.org/pubmed/22761565" title="Access to this publication">Quantifying the
        contribution of the liver to glucose homeostasis: a detailed kinetic model of human hepatic glucose metabolism.
        </a>
    </div>
    <div class="bibo:authorList">König M., Bulik S., Holzhütter HG.</div>
    <div class="bibo:Journal">PLoS Comput Biol. 2012;8(6)</div>
    """ + templates.TERMS_OF_USE + """
    """
])

# -----------------------------------------------------------------------------
# Units
# -----------------------------------------------------------------------------
model_units = ModelUnits(
    time=UNIT_min,
    extent=UNIT_mmole,
    substance=UNIT_mmole,
    length=UNIT_m,
    area=UNIT_m2,
    volume=UNIT_KIND_LITRE
)

units = [
    UNIT_s, UNIT_min,
    UNIT_kg,
    UNIT_m,
    UNIT_m2,
    UNIT_m3,
    UNIT_mmole, UNIT_mM,
    UNIT_per_s, UNIT_per_min,
    Unit('s_per_min', [(UNIT_KIND_SECOND, 1.0),
                       (UNIT_KIND_SECOND, -1.0, 0, 60)]),
    Unit('per_mM', [(UNIT_KIND_METRE, 3.0),
                    (UNIT_KIND_MOLE, -1.0)]),
    Unit('mM2', [(UNIT_KIND_MOLE, 2.0),
                 (UNIT_KIND_METRE, -6.0)]),
    Unit('pmol', [(UNIT_KIND_MOLE, 1.0, -12, 1.0)]),
    Unit('pM', [(UNIT_KIND_MOLE, 1.0, -12, 1.0), (UNIT_KIND_LITRE, -1.0)]),
    Unit('mmole_per_min', [(UNIT_KIND_MOLE, 1.0, -3, 1.0),
                           (UNIT_KIND_SECOND, -1.0, 0, 60)]),
    Unit('mumole_per_mmole', [(UNIT_KIND_MOLE, 1.0, -6, 1.0),
                              (UNIT_KIND_MOLE, -1.0, -3, 1.0)]),
    Unit('mumole_per_mmole_kg', [(UNIT_KIND_MOLE, 1.0, -6, 1.0),
                                 (UNIT_KIND_MOLE, -1.0, -3, 1.0),
                                 (UNIT_KIND_KILOGRAM, -1.0, 0, 1.0)]),
    Unit('mumol_per_min_kg', [(UNIT_KIND_MOLE, 1.0, -6, 1.0),
                              (UNIT_KIND_SECOND, -1.0, 0, 60),
                              (UNIT_KIND_KILOGRAM, -1.0)]),
]

# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------
# not needed in SBML L3V2 any more
functions = [
    Function('max', 'lambda(x,y, piecewise(x,gt(x,y),y) )',
             name='minimum of arguments'),
    Function('min', 'lambda(x,y, piecewise(x,lt(x,y),y) )',
             name='maximum of arguments'),
]

# -----------------------------------------------------------------------------
# Compartments
# -----------------------------------------------------------------------------
compartments = [
    Compartment(sid='ext', unit=UNIT_KIND_LITRE, constant=False, value=1.0,
                name='blood', port=True),
    Compartment(sid='cyto', unit=UNIT_KIND_LITRE, constant=False,
                value='V_cyto', name='cytosol', port=True),
    Compartment(sid='mito', unit=UNIT_KIND_LITRE, constant=False,
                value='V_mito', name='mitochondrion'),
    Compartment(sid='pm', spatialDimensions=2, unit='m2', constant=True,
                value=1.0, name='plasma membrane'),
    Compartment(sid='mm', spatialDimensions=2, unit='m2', constant=True,
                value=1.0, name='mitochondrial membrane'),
]

# -----------------------------------------------------------------------------
# Species
# -----------------------------------------------------------------------------
species = [
    Species('atp', compartment='cyto', initialConcentration=2.8000,
            substanceUnit='mmole', boundaryCondition=True,
            hasOnlySubstanceUnits=False, name='ATP'),
    Species('adp', compartment='cyto', initialConcentration=0.8000,
            substanceUnit='mmole', boundaryCondition=True,
            hasOnlySubstanceUnits=False, name='ADP'),
    Species('amp', compartment='cyto', initialConcentration=0.1600,
            substanceUnit='mmole', boundaryCondition=True,
            hasOnlySubstanceUnits=False, name='AMP'),
    Species('utp', compartment='cyto', initialConcentration=0.2700,
            substanceUnit='mmole', boundaryCondition=False,
            hasOnlySubstanceUnits=False, name='UTP'),
    Species('udp', compartment='cyto', initialConcentration=0.0900,
            substanceUnit='mmole', boundaryCondition=False,
            hasOnlySubstanceUnits=False, name='UDP'),
    Species('gtp', compartment='cyto', initialConcentration=0.2900,
            substanceUnit='mmole', boundaryCondition=False,
            hasOnlySubstanceUnits=False, name='GTP'),
    Species('gdp', compartment='cyto', initialConcentration=0.1000,
            substanceUnit='mmole', boundaryCondition=False,
            hasOnlySubstanceUnits=False, name='GDP'),
    Species('nad', compartment='cyto', initialConcentration=1.2200,
            substanceUnit='mmole', boundaryCondition=True,
            hasOnlySubstanceUnits=False, name='NAD+'),
    Species('nadh', compartment='cyto', initialConcentration=0.56E-3,
            substanceUnit='mmole', boundaryCondition=True,
            hasOnlySubstanceUnits=False, name='NADH'),
    Species('phos', compartment='cyto', initialConcentration=5.0000,
            substanceUnit='mmole', boundaryCondition=True,
            hasOnlySubstanceUnits=False, name='phosphate'),
    Species('pp', compartment='cyto', initialConcentration=0.0080,
            substanceUnit='mmole', boundaryCondition=False,
            hasOnlySubstanceUnits=False, name='pyrophosphate'),
    Species('co2', compartment='cyto', initialConcentration=5.0000,
            substanceUnit='mmole', boundaryCondition=True,
            hasOnlySubstanceUnits=False, name='CO2'),
    Species('h2o', compartment='cyto', initialConcentration=0.0,
            substanceUnit='mmole', boundaryCondition=True,
            hasOnlySubstanceUnits=False, name='H2O'),
    Species('h', compartment='cyto', initialConcentration=0.0,
            substanceUnit='mmole', boundaryCondition=True,
            hasOnlySubstanceUnits=False, name='H+'),

    Species('glc1p', compartment='cyto', initialConcentration=0.0120,
            substanceUnit='mmole', boundaryCondition=False,
            hasOnlySubstanceUnits=False,
            name='glucose-1 phosphate'),
    Species('udpglc', compartment='cyto', initialConcentration=0.3800,
            substanceUnit='mmole', boundaryCondition=False,
            hasOnlySubstanceUnits=False, name='UDP-glucose'),
    Species('glyglc', compartment='cyto', initialConcentration=250.0000,
            substanceUnit='mmole', boundaryCondition=False,
            hasOnlySubstanceUnits=False, name='glycogen'),
    Species('glc', compartment='cyto', initialConcentration=5.0000,
            substanceUnit='mmole', boundaryCondition=False,
            hasOnlySubstanceUnits=False, name='glucose'),
    Species('glc6p', compartment='cyto', initialConcentration=0.1200,
            substanceUnit='mmole', boundaryCondition=False,
            hasOnlySubstanceUnits=False,
            name='glucose-6 phosphate'),
    Species('fru6p', compartment='cyto', initialConcentration=0.0500,
            substanceUnit='mmole', boundaryCondition=False,
            hasOnlySubstanceUnits=False,
            name='fructose-6 phosphate'),
    Species('fru16bp', compartment='cyto', initialConcentration=0.0200,
            substanceUnit='mmole', boundaryCondition=False,
            hasOnlySubstanceUnits=False,
            name='fructose-16 bisphosphate'),
    Species('fru26bp', compartment='cyto', initialConcentration=0.0040,
            substanceUnit='mmole', boundaryCondition=False,
            hasOnlySubstanceUnits=False,
            name='fructose-26 bisphosphate'),
    Species('grap', compartment='cyto', initialConcentration=0.1000,
            substanceUnit='mmole', boundaryCondition=False,
            hasOnlySubstanceUnits=False,
            name='glyceraldehyde 3-phosphate'),
    Species('dhap', compartment='cyto', initialConcentration=0.0300,
            substanceUnit='mmole', boundaryCondition=False,
            hasOnlySubstanceUnits=False,
            name='dihydroxyacetone phosphate'),
    Species('bpg13', compartment='cyto', initialConcentration=0.3000,
            substanceUnit='mmole', boundaryCondition=False,
            hasOnlySubstanceUnits=False,
            name='13-bisphospho-glycerate'),
    Species('pg3', compartment='cyto', initialConcentration=0.2700,
            substanceUnit='mmole', boundaryCondition=False,
            hasOnlySubstanceUnits=False, name='3-phosphoglycerate'),
    Species('pg2', compartment='cyto', initialConcentration=0.0300,
            substanceUnit='mmole', boundaryCondition=False,
            hasOnlySubstanceUnits=False, name='2-phosphoglycerate'),
    Species('pep', compartment='cyto', initialConcentration=0.1500,
            substanceUnit='mmole', boundaryCondition=False,
            hasOnlySubstanceUnits=False, name='phosphoenolpyruvate'),
    Species('pyr', compartment='cyto', initialConcentration=0.1000,
            substanceUnit='mmole', boundaryCondition=False,
            hasOnlySubstanceUnits=False, name='pyruvate'),
    Species('oaa', compartment='cyto', initialConcentration=0.0100,
            substanceUnit='mmole', boundaryCondition=False,
            hasOnlySubstanceUnits=False, name='oxaloacetate'),
    Species('lac', compartment='cyto', initialConcentration=0.5000,
            substanceUnit='mmole', boundaryCondition=False,
            hasOnlySubstanceUnits=False, name='lactate'),

    Species('glc_ext', compartment='ext', initialConcentration=3.0000,
            substanceUnit='mmole', boundaryCondition=True,
            hasOnlySubstanceUnits=False, name='glucose', port=True),
    Species('lac_ext', compartment='ext', initialConcentration=1.2000,
            substanceUnit='mmole', boundaryCondition=True,
            hasOnlySubstanceUnits=False, name='lactate', port=True),

    Species('co2_mito', compartment='mito', initialConcentration=5.0000,
            substanceUnit='mmole', boundaryCondition=True,
            hasOnlySubstanceUnits=False, name='CO2'),
    Species('phos_mito', compartment='mito', initialConcentration=5.0000,
            substanceUnit='mmole', boundaryCondition=True,
            hasOnlySubstanceUnits=False, name='phosphate'),
    Species('oaa_mito', compartment='mito', initialConcentration=0.0100,
            substanceUnit='mmole', boundaryCondition=False,
            hasOnlySubstanceUnits=False, name=' oxaloacetate'),
    Species('pep_mito', compartment='mito', initialConcentration=0.1500,
            substanceUnit='mmole', boundaryCondition=False,
            hasOnlySubstanceUnits=False,
            name='phosphoenolpyruvate'),
    Species('acoa_mito', compartment='mito', initialConcentration=0.0400,
            substanceUnit='mmole', boundaryCondition=True,
            hasOnlySubstanceUnits=False,
            name='acetyl-coenzyme A'),
    Species('pyr_mito', compartment='mito', initialConcentration=0.1000,
            substanceUnit='mmole', boundaryCondition=False,
            hasOnlySubstanceUnits=False, name='pyruvate'),
    Species('cit_mito', compartment='mito', initialConcentration=0.3200,
            substanceUnit='mmole', boundaryCondition=True,
            hasOnlySubstanceUnits=False, name='citrate'),

    Species('atp_mito', compartment='mito', initialConcentration=2.8000,
            substanceUnit='mmole', boundaryCondition=True,
            hasOnlySubstanceUnits=False, name='ATP'),
    Species('adp_mito', compartment='mito', initialConcentration=0.8000,
            substanceUnit='mmole', boundaryCondition=True,
            hasOnlySubstanceUnits=False, name='ADP'),
    Species('gtp_mito', compartment='mito', initialConcentration=0.2900,
            substanceUnit='mmole', boundaryCondition=False,
            hasOnlySubstanceUnits=False, name='GTP'),
    Species('gdp_mito', compartment='mito', initialConcentration=0.1000,
            substanceUnit='mmole', boundaryCondition=False,
            hasOnlySubstanceUnits=False, name='GDP'),
    Species('coa_mito', compartment='mito', initialConcentration=0.0550,
            substanceUnit='mmole', boundaryCondition=True,
            hasOnlySubstanceUnits=False, name='coenzyme A'),
    Species('nadh_mito', compartment='mito', initialConcentration=0.2400,
            substanceUnit='mmole', boundaryCondition=True,
            hasOnlySubstanceUnits=False, name='NADH'),
    Species('nad_mito', compartment='mito', initialConcentration=0.9800,
            substanceUnit='mmole', boundaryCondition=True,
            hasOnlySubstanceUnits=False, name='NAD+'),
    Species('h2o_mito', compartment='mito', initialConcentration=0.0,
            substanceUnit='mmole', boundaryCondition=True,
            hasOnlySubstanceUnits=False, name='H20'),
    Species('h_mito', compartment='mito', initialConcentration=0.0,
            substanceUnit='mmole', boundaryCondition=True,
            hasOnlySubstanceUnits=False, name='H+'),
]

# -----------------------------------------------------------------------------
# Parameters
# -----------------------------------------------------------------------------
parameters = [
    Parameter('scale', 1.0, 'dimensionless', True,
              name='scaling factor for rates'),
    Parameter('V_cyto', 1.0, UNIT_KIND_LITRE, True, name='cytosolic volume'),
    Parameter('f_mito', 0.2, 'dimensionless', True,
              name='mitochondrial volume factor'),
    Parameter('Vliver', 1.5, UNIT_KIND_LITRE, True, name='liver volume'),
    Parameter('fliver', 0.583333333333334, 'dimensionless', True,
              name='parenchymal fraction liver'),
    Parameter('bodyweight', 70, 'kg', True, name='bodyweight'),

    Parameter('sec_per_min', 60, 's_per_min', True, name='time conversion'),
    Parameter('mumole_per_mmole', 1000, 'mumole_per_mmole', True,
              name='amount conversion'),

    # hormonal regulation
    Parameter('x_ins1', 818.9, 'pM', True),
    Parameter('x_ins2', 0, 'pM', True),
    Parameter('x_ins3', 8.6, 'mM', True),
    Parameter('x_ins4', 4.2, 'dimensionless', True),

    Parameter('x_glu1', 190, 'pM', True),
    Parameter('x_glu2', 37.9, 'pM', True),
    Parameter('x_glu3', 3.01, 'mM', True),
    Parameter('x_glu4', 6.40, 'dimensionless', True),

    Parameter('x_epi1', 6090, 'pM', True),
    Parameter('x_epi2', 100, 'pM', True),
    Parameter('x_epi3', 3.10, 'mM', True),
    Parameter('x_epi4', 8.40, 'dimensionless', True),

    Parameter('K_val', 0.1, 'dimensionless', True),
    Parameter('epi_f', 0.8, 'dimensionless', True),
]

# -----------------------------------------------------------------------------
# Assignment rules
# -----------------------------------------------------------------------------
rules = [
    # initial assignments
    AssignmentRule('V_mito', 'f_mito * V_cyto', 'm3',
                   name='mitochondrial volume'),
    AssignmentRule('flux_conversion', 'mumole_per_mmole/bodyweight',
                   'mumole_per_mmole_kg'),
    AssignmentRule('f_gly', 'scale', 'dimensionless',
                   name='scaling factor glycolysis'),
    AssignmentRule('f_glyglc', 'scale', 'dimensionless',
                   name='scaling factor glycogen metabolism'),

    # hormonal regulation
    AssignmentRule('ins',
                   'x_ins2 + (x_ins1-x_ins2) * glc_ext^x_ins4/(glc_ext^x_ins4 + x_ins3^x_ins4)',
                   'pM',
                   name='insulin'),
    AssignmentRule('ins_norm', 'max(0.0 pM, ins-x_ins2)', 'pM',
                   name='insulin normalized'),
    AssignmentRule('glu',
                   'x_glu2 + (x_glu1-x_glu2)*(1 dimensionless - glc_ext^x_glu4/(glc_ext^x_glu4 + x_glu3^x_glu4))',
                   'pM', name='glucagon'),
    AssignmentRule('glu_norm', 'max(0.0 pM, glu-x_glu2)', 'pM',
                   name='glucagon normalized'),
    AssignmentRule('epi',
                   'x_epi2 + (x_epi1-x_epi2) * (1 dimensionless - glc_ext^x_epi4/(glc_ext^x_epi4 + x_epi3^x_epi4))',
                   'pM', name='epinephrine'),
    AssignmentRule('epi_norm', 'max(0.0 pM, epi-x_epi2)', 'pM',
                   name='epinephrine normalized'),
    AssignmentRule('K_ins', '(x_ins1-x_ins2) * K_val', 'pM'),
    AssignmentRule('K_glu', '(x_glu1-x_glu2) * K_val', 'pM'),
    AssignmentRule('K_epi', '(x_epi1-x_epi2) * K_val', 'pM'),
    AssignmentRule('gamma',
                   '0.5 dimensionless * (1 dimensionless -ins_norm/(ins_norm+K_ins) + '
                   'max(glu_norm/(glu_norm+K_glu), epi_f*epi_norm/(epi_norm+K_epi)))',
                   'dimensionless', name='phosphorylation state'),

    # balance equations
    AssignmentRule('nadh_tot', 'nadh + nad', 'mM', name='NADH balance'),
    AssignmentRule('atp_tot', 'atp + adp + amp', 'mM', 'ATP balance'),
    AssignmentRule('utp_tot', 'utp + udp + udpglc', 'mM', name='UTP balance'),
    AssignmentRule('gtp_tot', 'gtp + gdp', 'mM', name='GTP balance'),
    AssignmentRule('nadh_mito_tot', 'nadh_mito + nad_mito', 'mM',
                   name='NADH mito balance'),
    AssignmentRule('atp_mito_tot', 'atp_mito + adp_mito', 'mM',
                   name='ATP mito balance'),
    AssignmentRule('gtp_mito_tot', 'gtp_mito + gdp_mito', 'mM',
                   name='GTP mito balance'),

    # whole liver output
    AssignmentRule('HGP', '-GLUT2 * flux_conversion', 'mumol_per_min_kg',
                   name='hepatic glucose production/utilization'),
    AssignmentRule('GNG', '-GPI * flux_conversion', 'mumol_per_min_kg',
                   name='gluconeogenesis/glycolysis'),
    AssignmentRule('GLY', 'G16PI * flux_conversion', 'mumol_per_min_kg',
                   name='glycogenolysis/glycogen synthesis'),
]

# -----------------------------------------------------------------------------
#    REACTIONS
# -----------------------------------------------------------------------------
GLUT2 = Reaction(
    sid='GLUT2',
    name='GLUT2 glucose transporter',
    equation='glc_ext <-> glc []',
    # C6H1206 (0) <-> C6H12O6 (0)
    compartment='pm',
    sboTerm=SBO_TRANSPORT_REACTION,
    pars=[
        Parameter('GLUT2_keq', 1, 'dimensionless'),
        Parameter('GLUT2_k_glc', 42, 'mM'),
        Parameter('GLUT2_Vmax', 420, 'mmole_per_min'),
    ],
    rules=[],
    formula=('f_gly * (GLUT2_Vmax/GLUT2_k_glc) * (glc_ext - glc/GLUT2_keq)/'
             '(1 dimensionless + glc_ext/GLUT2_k_glc + glc/GLUT2_k_glc)',
             'mmole_per_min')
)

GK = Reaction(
    sid='GK',
    name='Glucokinase',
    equation='glc + atp => glc6p + adp + h [glc1p, fru6p]',
    # C6H1206 (0) + C10H12N5O13P3 (-4)  <-> C6H11O9P (-2) + C10H12N5O10P2 (-3) + H (1)
    compartment='cyto',
    sboTerm=SBO_BIOCHEMICAL_REACTION,
    pars=[
        Parameter('GK_n_gkrp', 2, 'dimensionless'),
        Parameter('GK_k_glc1', 15, 'mM'),
        Parameter('GK_k_fru6p', 0.010, 'mM'),
        Parameter('GK_b', 0.7, 'dimensionless'),
        Parameter('GK_n', 1.6, 'dimensionless'),
        Parameter('GK_k_glc', 7.5, 'mM'),
        Parameter('GK_k_atp', 0.26, 'mM'),
        Parameter('GK_Vmax', 25.2, 'mmole_per_min'),
    ],
    rules=[
        AssignmentRule('GK_gc_free',
                       '(glc^GK_n_gkrp / (glc^GK_n_gkrp + GK_k_glc1^GK_n_gkrp) ) * '
                       '(1 dimensionless - GK_b*fru6p/(fru6p + GK_k_fru6p))',
                       'dimensionless'),
    ],
    formula=(
    'f_gly * GK_Vmax * GK_gc_free * (atp/(GK_k_atp + atp)) * (glc^GK_n/(glc^GK_n + GK_k_glc^GK_n))',
    'mmole_per_min')
)

G6PASE = Reaction(
    sid='G6PASE',
    name='D-Glucose-6-phosphate Phosphatase',
    equation='glc6p + h2o => glc + phos []',
    # C6H11O9P (-2) + H2O (0) -> C6H12O6 (0) + HO4P (-2)
    compartment='cyto',
    sboTerm=SBO_BIOCHEMICAL_REACTION,
    pars=[
        Parameter('G6PASE_k_glc6p', 2, 'mM'),
        Parameter('G6PASE_Vmax', 18.9, 'mmole_per_min'),
    ],
    formula=(
    'f_gly * G6PASE_Vmax * (glc6p / (G6PASE_k_glc6p + glc6p))', 'mmole_per_min')
)

GPI = Reaction(
    sid='GPI',
    name='D-Glucose-6-phosphate Isomerase',
    equation='glc6p <-> fru6p []',
    # C6H11O9P (-2) <-> C6H11O9P (-2)
    compartment='cyto',
    sboTerm=SBO_BIOCHEMICAL_REACTION,
    pars=[
        Parameter('GPI_keq', 0.517060817492925, 'dimensionless'),
        Parameter('GPI_k_glc6p', 0.182, 'mM'),
        Parameter('GPI_k_fru6p', 0.071, 'mM'),
        Parameter('GPI_Vmax', 420, 'mmole_per_min'),
    ],
    formula=('f_gly * (GPI_Vmax/GPI_k_glc6p) * (glc6p - fru6p/GPI_keq) / '
             '(1 dimensionless + glc6p/GPI_k_glc6p + fru6p/GPI_k_fru6p)',
             'mmole_per_min')
)

G16PI = Reaction(
    sid='G16PI',
    name='Glucose 1-phosphate 1,6-phosphomutase',
    equation='glc1p <-> glc6p []',
    # C6H11O9P (-2) <-> C6H11O9P (-2)
    compartment='cyto',
    sboTerm=SBO_BIOCHEMICAL_REACTION,
    pars=[
        Parameter('G16PI_keq', 15.717554082151441, 'dimensionless'),
        Parameter('G16PI_k_glc6p', 0.67, 'mM'),
        Parameter('G16PI_k_glc1p', 0.045, 'mM'),
        Parameter('G16PI_Vmax', 100, 'mmole_per_min'),
    ],
    formula=(
    'f_glyglc * (G16PI_Vmax/G16PI_k_glc1p) * (glc1p - glc6p/G16PI_keq) / '
    '(1 dimensionless + glc1p/G16PI_k_glc1p + glc6p/G16PI_k_glc6p)',
    'mmole_per_min')
)

UPGASE = Reaction(
    sid='UPGASE',
    name='UTP:Glucose-1-phosphate uridylyltransferase',
    equation='glc1p + h + utp <-> pp + udpglc []',
    # C6H11O9P (-2) + H (+1) + C9H11N2O15P3 (-4) <-> HO7P2 (-3) + C15H22N2O17P2 (-2)
    compartment='cyto',
    sboTerm=SBO_BIOCHEMICAL_REACTION,
    pars=[
        Parameter('UPGASE_keq', 0.312237619153088, 'dimensionless'),
        Parameter('UPGASE_k_utp', 0.563, 'mM'),
        Parameter('UPGASE_k_glc1p', 0.172, 'mM'),
        Parameter('UPGASE_k_udpglc', 0.049, 'mM'),
        Parameter('UPGASE_k_pp', 0.166, 'mM'),
        Parameter('UPGASE_Vmax', 80, 'mmole_per_min'),
    ],
    formula=(
    'f_glyglc * UPGASE_Vmax/(UPGASE_k_utp*UPGASE_k_glc1p) * (utp*glc1p - udpglc*pp/UPGASE_keq) / '
    '( (1 dimensionless + utp/UPGASE_k_utp)*(1 dimensionless + glc1p/UPGASE_k_glc1p) + '
    '(1 dimensionless + udpglc/UPGASE_k_udpglc)*(1 dimensionless + pp/UPGASE_k_pp) - 1 dimensionless)',
    'mmole_per_min')
)

PPASE = Reaction(
    sid='PPASE',
    name='Pyrophosphate phosphohydrolase',
    equation='pp + h2o => h + 2 phos []',
    # HO7P2 (-3) + H2O (0) -> H (+1) + HO4P (-2)
    compartment='cyto',
    sboTerm=SBO_BIOCHEMICAL_REACTION,
    pars=[
        Parameter('PPASE_k_pp', 0.005, 'mM'),
        Parameter('PPASE_Vmax', 2.4, 'mmole_per_min'),
    ],
    formula=('f_glyglc * PPASE_Vmax * pp/(pp + PPASE_k_pp)', 'mmole_per_min')
)

GS = Reaction(
    sid='GS',
    name='Glycogen synthase',
    equation='udpglc + h2o => udp + h + glyglc [glc6p]',
    # notes=[
    #  'C15H22N2O17P2 (-2) + H20 (0) => C9H11N2O12P2 (-3) + H (+1) + C6H12O6(0)',
    #  'Synthesis of glycogen from uridine diphosphate glucose in liver. '
    #  'PMID: 14415527'
    # ],
    compartment='cyto',
    sboTerm=SBO_BIOCHEMICAL_REACTION,
    pars=[
        Parameter('GS_C', 500, 'mM'),
        Parameter('GS_k1_max', 0.2, 'dimensionless'),
        Parameter('GSn_k1', 0.224, 'mM2'),
        Parameter('GSp_k1', 3.003, 'mM2'),
        Parameter('GSn_k2', 0.1504, 'mM'),
        Parameter('GSp_k2', 0.09029, 'mM'),
        Parameter('GS_Vmax', 13.2, 'mmole_per_min'),
    ],
    rules=[
        AssignmentRule('GS_fs',
                       '(1 dimensionless + GS_k1_max) * (GS_C - glyglc)/'
                       '( (GS_C - glyglc) + GS_k1_max * GS_C)',
                       'dimensionless'),
        AssignmentRule('GSn_k_udpglc', 'GSn_k1 / (glc6p + GSn_k2)', 'mM'),
        AssignmentRule('GSp_k_udpglc', 'GSp_k1 / (glc6p + GSp_k2)', 'mM'),
        AssignmentRule('GSn',
                       'f_glyglc * GS_Vmax * GS_fs * udpglc / (GSn_k_udpglc + udpglc)',
                       'mmole_per_min'),
        AssignmentRule('GSp',
                       'f_glyglc * GS_Vmax * GS_fs * udpglc / (GSp_k_udpglc + udpglc)',
                       'mmole_per_min'),
    ],
    formula=('(1 dimensionless - gamma)*GSn + gamma*GSp', 'mmole_per_min')
)

GP = Reaction(
    sid='GP',
    name='Glycogen-Phosphorylase',
    equation='glyglc + phos <-> glc1p + h2o [phos, amp, glc]',
    # C6H12O6 (0) + H04P (-2) <-> C6H11O9P (-2) + H2O (0)
    compartment='cyto',
    sboTerm=SBO_BIOCHEMICAL_REACTION,
    pars=[
        Parameter('GP_keq', 0.211826505793075, 'per_mM'),
        Parameter('GPn_k_glyglc', 4.8, 'mM'),
        Parameter('GPp_k_glyglc', 2.7, 'mM'),
        Parameter('GPn_k_glc1p', 120, 'mM'),
        Parameter('GPp_k_glc1p', 2, 'mM'),
        Parameter('GPn_k_phos', 300, 'mM'),
        Parameter('GPp_k_phos', 5, 'mM'),
        Parameter('GPp_ki_glc', 5, 'mM'),
        Parameter('GPn_ka_amp', 1, 'mM'),
        Parameter('GPn_base_amp', 0.03, 'dimensionless'),
        Parameter('GPn_max_amp', 0.30, 'dimensionless'),
        Parameter('GP_Vmax', 6.8, 'mmole_per_min'),
    ],
    rules=[
        AssignmentRule('GP_fmax',
                       '(1 dimensionless +GS_k1_max) * glyglc /( glyglc + GS_k1_max * GS_C)',
                       'dimensionless'),
        AssignmentRule('GPn_Vmax', 'f_glyglc * GP_Vmax * GP_fmax * '
                                   '(GPn_base_amp + (GPn_max_amp - GPn_base_amp) *amp/(amp+GPn_ka_amp))',
                       'mmole_per_min'),
        AssignmentRule('GPn',
                       'GPn_Vmax/(GPn_k_glyglc*GPn_k_phos) * (glyglc*phos - glc1p/GP_keq) / '
                       '( (1 dimensionless + glyglc/GPn_k_glyglc)*(1 dimensionless + phos/GPn_k_phos) + '
                       '(1 dimensionless + glc1p/GPn_k_glc1p) - 1 dimensionless)',
                       'mmole_per_min'),
        AssignmentRule('GPp_Vmax',
                       'f_glyglc * GP_Vmax * GP_fmax * exp(-log(2 dimensionless)/GPp_ki_glc * glc)',
                       'mmole_per_min'),
        AssignmentRule('GPp',
                       'GPp_Vmax/(GPp_k_glyglc*GPp_k_phos) * (glyglc*phos - glc1p/GP_keq) / '
                       '( (1 dimensionless + glyglc/GPp_k_glyglc)*(1 dimensionless + phos/GPp_k_phos) + '
                       '(1 dimensionless + glc1p/GPp_k_glc1p) - 1 dimensionless)',
                       'mmole_per_min'),
    ],
    formula=('(1 dimensionless - gamma) * GPn + gamma*GPp', 'mmole_per_min')
)

NDKGTP = Reaction(
    sid='NDKGTP',
    name='Nucleoside-diphosphate kinase (ATP, GTP)',
    equation='atp + gdp <-> adp + gtp []',
    # C10H12N5O13P3 (-4) + C10H12N5O11P2 (-3) <-> C10H12N5O10P2 (-3) + C10H12N5O14P3 (-4)
    compartment='cyto',
    sboTerm=SBO_BIOCHEMICAL_REACTION,
    pars=[
        Parameter('NDKGTP_keq', 1, 'dimensionless'),
        Parameter('NDKGTP_k_atp', 1.33, 'mM'),
        Parameter('NDKGTP_k_adp', 0.042, 'mM'),
        Parameter('NDKGTP_k_gtp', 0.15, 'mM'),
        Parameter('NDKGTP_k_gdp', 0.031, 'mM'),
        Parameter('NDKGTP_Vmax', 0, 'mmole_per_min'),
    ],
    rules=[],
    formula=(
    'f_gly * NDKGTP_Vmax/(NDKGTP_k_atp*NDKGTP_k_gdp) * (atp*gdp - adp*gtp/NDKGTP_keq) / '
    '( (1 dimensionless + atp/NDKGTP_k_atp)*(1 dimensionless + gdp/NDKGTP_k_gdp) + '
    '(1 dimensionless + adp/NDKGTP_k_adp)*(1 dimensionless + gtp/NDKGTP_k_gtp) - 1 dimensionless)',
    'mmole_per_min')
)

NDKUTP = Reaction(
    sid='NDKUTP',
    name='Nucleoside-diphosphate kinase (ATP, UTP)',
    equation='atp + udp <-> adp + utp []',
    # C10H12N5O13P3 (-4) + C9H11N2O12P2 (-3) <-> C10H12N5O10P2 (-3) + C9H11N2O15P3 (-4)
    compartment='cyto',
    sboTerm=SBO_BIOCHEMICAL_REACTION,
    pars=[
        Parameter('NDKUTP_keq', 1, 'dimensionless'),
        Parameter('NDKUTP_k_atp', 1.33, 'mM'),
        Parameter('NDKUTP_k_adp', 0.042, 'mM'),
        Parameter('NDKUTP_k_utp', 16, 'mM'),
        Parameter('NDKUTP_k_udp', 0.19, 'mM'),
        Parameter('NDKUTP_Vmax', 2940, 'mmole_per_min'),
    ],
    rules=[],
    formula=(
    'f_glyglc * NDKUTP_Vmax / (NDKUTP_k_atp * NDKUTP_k_udp) * (atp*udp - adp*utp/NDKUTP_keq) / '
    '( (1 dimensionless + atp/NDKUTP_k_atp)*(1 dimensionless + udp/NDKUTP_k_udp) + '
    '(1 dimensionless + adp/NDKUTP_k_adp)*(1 dimensionless + utp/NDKUTP_k_utp) - 1 dimensionless)',
    'mmole_per_min')
)

AK = Reaction(
    sid='AK',
    name='ATP:AMP phosphotransferase (Adenylatkinase)',
    equation='amp + atp <-> 2 adp []',
    # C10H12N5O7P (-2) + C10H12N5O13P3 (-4) <-> C10H12N5O10P2 (-3)
    compartment='cyto',
    sboTerm=SBO_BIOCHEMICAL_REACTION,
    pars=[
        Parameter('AK_keq', 0.247390074904985, 'dimensionless'),
        Parameter('AK_k_atp', 0.09, 'mM'),
        Parameter('AK_k_amp', 0.08, 'mM'),
        Parameter('AK_k_adp', 0.11, 'mM'),
        Parameter('AK_Vmax', 0, 'mmole_per_min'),
    ],
    rules=[],
    formula=(
    'f_gly * AK_Vmax / (AK_k_atp * AK_k_amp) * (atp*amp - adp*adp/AK_keq) / '
    '( (1 dimensionless +atp/AK_k_atp)*(1 dimensionless +amp/AK_k_amp) + '
    '(1 dimensionless +adp/AK_k_adp)*(1 dimensionless +adp/AK_k_adp) - 1 dimensionless)',
    'mmole_per_min')
)

PFK2 = Reaction(
    sid='PFK2',
    name='ATP:D-fructose-6-phosphate 2-phosphotransferase',
    equation='fru6p + atp => fru26bp + adp + h []',
    # C6H11O9P (-2) + C10H12N5O13P3 (-4) => C6H10O12P2 (-4) + C10H12N5O10P2 (-3) + H (+1)
    compartment='cyto',
    sboTerm=SBO_BIOCHEMICAL_REACTION,
    pars=[
        Parameter('PFK2n_n', 1.3, 'dimensionless'),
        Parameter('PFK2p_n', 2.1, 'dimensionless'),
        Parameter('PFK2n_k_fru6p', 0.016, 'mM'),
        Parameter('PFK2p_k_fru6p', 0.050, 'mM'),
        Parameter('PFK2n_k_atp', 0.28, 'mM'),
        Parameter('PFK2p_k_atp', 0.65, 'mM'),
        Parameter('PFK2_Vmax', 0.0042, 'mmole_per_min'),
    ],
    rules=[
        AssignmentRule('PFK2n',
                       'f_gly * PFK2_Vmax * fru6p^PFK2n_n / (fru6p^PFK2n_n + PFK2n_k_fru6p^PFK2n_n) * '
                       'atp/(atp + PFK2n_k_atp)', 'mmole_per_min'),
        AssignmentRule('PFK2p',
                       'f_gly * PFK2_Vmax * fru6p^PFK2p_n / (fru6p^PFK2p_n + PFK2p_k_fru6p^PFK2p_n) * '
                       'atp/(atp + PFK2p_k_atp)', 'mmole_per_min'),
    ],
    formula=('(1 dimensionless - gamma) * PFK2n + gamma*PFK2p', 'mmole_per_min')
)

FBP2 = Reaction(
    sid='FBP2',
    name='D-Fructose-2,6-bisphosphate 2-phosphohydrolase',
    equation='fru26bp + h2o => fru6p + phos []',
    # C6H10O12P2 (-4) + H2O (0) => C6H11O9P (-2) + HO4P (-2)
    compartment='cyto',
    sboTerm=SBO_BIOCHEMICAL_REACTION,
    pars=[
        Parameter('FBP2n_k_fru26bp', 0.010, 'mM'),
        Parameter('FBP2p_k_fru26bp', 0.0005, 'mM'),
        Parameter('FBP2n_ki_fru6p', 0.0035, 'mM'),
        Parameter('FBP2p_ki_fru6p', 0.010, 'mM'),
        Parameter('FBP2_Vmax', 0.126, 'mmole_per_min'),
    ],
    rules=[
        AssignmentRule('FBP2n',
                       'f_gly * FBP2_Vmax/(1 dimensionless + fru6p/FBP2n_ki_fru6p) * fru26bp / '
                       '( FBP2n_k_fru26bp + fru26bp)', 'mmole_per_min'),
        AssignmentRule('FBP2p',
                       'f_gly * FBP2_Vmax/(1 dimensionless + fru6p/FBP2p_ki_fru6p) * fru26bp / '
                       '( FBP2p_k_fru26bp + fru26bp)', 'mmole_per_min'),
    ],
    formula=(
    '(1 dimensionless - gamma) * FBP2n + gamma * FBP2p', 'mmole_per_min')
)
"""
Goldstein BN, Maevsky AA. (2002)
Critical switch of the metabolic fluxes by phosphofructo-2-kinase:fructose-2,6-bisphosphatase. A kinetic model.
PMID: 12482582

Rider MH, Bertrand L, Vertommen D, Michels PA, Rousseau GG, Hue L. (2004)
6-phosphofructo-2-kinase/fructose-2,6-bisphosphatase: head-to-head with a bifunctional enzyme that controls glycolysis.
PMID: 15170386

Okar DA, Live DH, Devany MH, Lange AJ. (2000)
Mechanism of the bisphosphatase reaction of 6-phosphofructo-2-kinase/fructose-2,6-bisphosphatase probed by
(1)H-(15)N NMR spectroscopy.
PMID: 10933792
"""

PFK1 = Reaction(
    sid='PFK1',
    name='ATP:D-fructose-6-phosphate 1-phosphotransferase',
    equation='fru6p + atp => fru16bp + adp + h [fru26bp]',
    # C6H11O9P (-2) + C10H12N5O13P3 (-4) => C6H10O12P2 (-4) + C10H12N5O10P2 (-3) + H (+1)
    compartment='cyto',
    sboTerm=SBO_BIOCHEMICAL_REACTION,
    pars=[
        Parameter('PFK1_k_atp', 0.111, 'mM'),
        Parameter('PFK1_k_fru6p', 0.077, 'mM'),
        Parameter('PFK1_ki_fru6p', 0.012, 'mM'),
        Parameter('PFK1_ka_fru26bp', 0.001, 'mM'),
        Parameter('PFK1_Vmax', 7.182, 'mmole_per_min'),
    ],
    formula=(
    'f_gly * PFK1_Vmax * (1 dimensionless - 1 dimensionless/(1 dimensionless + fru26bp/PFK1_ka_fru26bp)) * '
    'fru6p*atp/(PFK1_ki_fru6p*PFK1_k_atp + PFK1_k_fru6p*atp + PFK1_k_atp*fru6p + atp*fru6p)',
    'mmole_per_min')
)

FBP1 = Reaction(
    sid='FBP1',
    name='D-Fructose-1,6-bisphosphate 1-phosphohydrolase',
    equation='fru16bp + h2o => fru6p + phos [fru26bp]',
    # C6H10O12P2 (-4) + H2O (0) => C6H11O9P (-2) + HO4P (-2)
    compartment='cyto',
    sboTerm=SBO_BIOCHEMICAL_REACTION,
    pars=[
        Parameter('FBP1_ki_fru26bp', 0.001, 'mM'),
        Parameter('FBP1_k_fru16bp', 0.0013, 'mM'),
        Parameter('FBP1_Vmax', 4.326, 'mmole_per_min'),
    ],
    formula=(
    'f_gly * FBP1_Vmax / (1 dimensionless + fru26bp/FBP1_ki_fru26bp) * fru16bp/(fru16bp + FBP1_k_fru16bp)',
    'mmole_per_min')
)

ALD = Reaction(
    sid='ALD',
    name='Aldolase',
    equation='fru16bp <-> grap + dhap []',
    # C6H10O12P2 (-4) <-> C3H5O6P (-2) + C3H5O6P (-2)
    compartment='cyto',
    sboTerm=SBO_BIOCHEMICAL_REACTION,
    pars=[
        Parameter('ALD_keq', 9.762988973629690E-5, 'mM'),
        Parameter('ALD_k_fru16bp', 0.0071, 'mM'),
        Parameter('ALD_k_dhap', 0.0364, 'mM'),
        Parameter('ALD_k_grap', 0.0071, 'mM'),
        Parameter('ALD_ki1_grap', 0.0572, 'mM'),
        Parameter('ALD_ki2_grap', 0.176, 'mM'),
        Parameter('ALD_Vmax', 420, 'mmole_per_min'),
    ],
    formula=('f_gly * ALD_Vmax/ALD_k_fru16bp * (fru16bp - grap*dhap/ALD_keq) / '
             '(1 dimensionless + fru16bp/ALD_k_fru16bp + grap/ALD_ki1_grap + '
             'dhap*(grap + ALD_k_grap)/(ALD_k_dhap*ALD_ki1_grap) + (fru16bp*grap)/(ALD_k_fru16bp*ALD_ki2_grap))',
             'mmole_per_min')
)

TPI = Reaction(
    sid='TPI',
    name='Triosephosphate Isomerase',
    equation='dhap <-> grap []',
    # C3H5O6P (-2) <-> C3H5O6P (-2)
    compartment='cyto',
    sboTerm=SBO_BIOCHEMICAL_REACTION,
    pars=[
        Parameter('TPI_keq', 0.054476985386756, 'dimensionless'),
        Parameter('TPI_k_dhap', 0.59, 'mM'),
        Parameter('TPI_k_grap', 0.42, 'mM'),
        Parameter('TPI_Vmax', 420, 'mmole_per_min'),
    ],
    formula=('f_gly * TPI_Vmax/TPI_k_dhap * (dhap - grap/TPI_keq) / '
             '(1 dimensionless + dhap/TPI_k_dhap + grap/TPI_k_grap)',
             'mmole_per_min')
)

GAPDH = Reaction(
    sid='GAPDH',
    name='D-Glyceraldehyde-3-phosphate:NAD+ oxidoreductase',
    equation='grap + nad + phos <-> bpg13 + nadh + h []',
    # C3H5O6P (-2) + C21H26N7O14P2 (-1) + HO4P (-2) <-> C3H4O10P2 (-4) + C21H27N7O14P2 (-2) + H (+1)
    compartment='cyto',
    sboTerm=SBO_BIOCHEMICAL_REACTION,
    pars=[
        Parameter('GAPDH_keq', 0.086779866194594, 'per_mM'),
        Parameter('GAPDH_k_nad', 0.05, 'mM'),
        Parameter('GAPDH_k_grap', 0.005, 'mM'),
        Parameter('GAPDH_k_phos', 3.9, 'mM'),
        Parameter('GAPDH_k_nadh', 0.0083, 'mM'),
        Parameter('GAPDH_k_bpg13', 0.0035, 'mM'),
        Parameter('GAPDH_Vmax', 420, 'mmole_per_min'),
    ],
    formula=(
    'f_gly * GAPDH_Vmax / (GAPDH_k_nad*GAPDH_k_grap*GAPDH_k_phos) * (nad*grap*phos - bpg13*nadh/GAPDH_keq) / '
    '( (1 dimensionless + nad/GAPDH_k_nad) * (1 dimensionless +grap/GAPDH_k_grap) * '
    '(1 dimensionless + phos/GAPDH_k_phos) + '
    '(1 dimensionless +nadh/GAPDH_k_nadh)*(1 dimensionless +bpg13/GAPDH_k_bpg13) - 1 dimensionless)',
    'mmole_per_min')
)

PGK = Reaction(
    sid='PGK',
    name='Phosphoglycerate Kinase',
    equation='adp + bpg13 <-> atp + pg3 []',
    # C10H12N5O10P2 (-3) + C3H4O10P2 (-4) <-> C10H12N5O13P3 (-4) + C3H4O7P (-3)
    compartment='cyto',
    sboTerm=SBO_BIOCHEMICAL_REACTION,
    pars=[
        Parameter('PGK_keq', 6.958644052488538, 'dimensionless'),
        Parameter('PGK_k_adp', 0.35, 'mM'),
        Parameter('PGK_k_atp', 0.48, 'mM'),
        Parameter('PGK_k_bpg13', 0.002, 'mM'),
        Parameter('PGK_k_pg3', 1.2, 'mM'),
        Parameter('PGK_Vmax', 420, 'mmole_per_min'),
    ],
    formula=(
    'f_gly * PGK_Vmax / (PGK_k_adp*PGK_k_bpg13) * (adp*bpg13 - atp*pg3/PGK_keq) / '
    '((1 dimensionless + adp/PGK_k_adp)*(1 dimensionless +bpg13/PGK_k_bpg13) + '
    '(1 dimensionless +atp/PGK_k_atp)*(1 dimensionless +pg3/PGK_k_pg3) - 1 dimensionless)',
    'mmole_per_min')
)

PGM = Reaction(
    sid='PGM',
    name='2-Phospho-D-glycerate 2,3-phosphomutase',
    equation='pg3 <-> pg2 []',
    # C3H4O7P (-3) <-> C3H4O7P (-3)
    compartment='cyto',
    sboTerm=SBO_BIOCHEMICAL_REACTION,
    pars=[
        Parameter('PGM_keq', 0.181375378837397, 'dimensionless'),
        Parameter('PGM_k_pg3', 5, 'mM'),
        Parameter('PGM_k_pg2', 1, 'mM'),
        Parameter('PGM_Vmax', 420, 'mmole_per_min'),
    ],
    formula=(
    'f_gly * PGM_Vmax * (pg3 - pg2/PGM_keq) / (pg3 + PGM_k_pg3 *(1 dimensionless + pg2/PGM_k_pg2))',
    'mmole_per_min')
)

EN = Reaction(
    sid='EN',
    name='2-Phospho-D-glycerate hydro-lyase (enolase)',
    equation='pg2 <-> h2o + pep []',
    # C3H4O7P (-3) <-> H2O (0) + C3H2O6P (-3)
    compartment='cyto',
    sboTerm=SBO_BIOCHEMICAL_REACTION,
    pars=[
        Parameter('EN_keq', 0.054476985386756, 'dimensionless'),
        Parameter('EN_k_pep', 1, 'mM'),
        Parameter('EN_k_pg2', 1, 'mM'),
        Parameter('EN_Vmax', 35.994, 'mmole_per_min'),
    ],
    formula=(
        'f_gly * EN_Vmax * (pg2 - pep/EN_keq) '
        '/ (pg2 + EN_k_pg2 *(1 dimensionless + pep/EN_k_pep))',
        'mmole_per_min'
    )
)

PK = Reaction(
    sid='PK',
    name='Pyruvatkinase',
    equation='pep + adp + h => pyr + atp [fru16bp]',
    # C3H2O6P (-3) + C10H12N5O10P2 (-3) + H (+1) => C10H12N5O13P3 (-4) + C3H3O3 (-1)
    compartment='cyto',
    sboTerm=SBO_BIOCHEMICAL_REACTION,
    pars=[
        Parameter('PKn_n', 3.5, 'dimensionless'),
        Parameter('PKp_n', 3.5, 'dimensionless'),
        Parameter('PKn_n_fbp', 1.8, 'dimensionless'),
        Parameter('PKp_n_fbp', 1.8, 'dimensionless'),
        Parameter('PKn_alpha', 1.0, 'dimensionless'),
        Parameter('PKp_alpha', 1.1, 'dimensionless'),
        Parameter('PKn_k_fbp', 0.16E-3, 'mM'),
        Parameter('PKp_k_fbp', 0.35E-3, 'mM'),
        Parameter('PKn_k_pep', 0.58, 'mM'),
        Parameter('PKp_k_pep', 1.10, 'mM'),
        Parameter('PKn_ba', 0.08, 'dimensionless'),
        Parameter('PKp_ba', 0.04, 'dimensionless'),

        Parameter('PK_ae', 1.0, 'dimensionless'),
        Parameter('PKn_k_pep_end', 0.08, 'mM'),
        Parameter('PK_k_adp', 2.3, 'mM'),

        Parameter('PK_Vmax', 46.2, 'mmole_per_min'),
    ],
    rules=[
        AssignmentRule('PKn_f',
                       'fru16bp^PKn_n_fbp / (PKn_k_fbp^PKn_n_fbp + fru16bp^PKn_n_fbp)',
                       'dimensionless'),
        AssignmentRule('PKp_f',
                       'fru16bp^PKp_n_fbp / (PKp_k_fbp^PKp_n_fbp + fru16bp^PKp_n_fbp)',
                       'dimensionless'),
        AssignmentRule('PKn_alpha_inp',
                       '(1 dimensionless - PKn_f) * (PKn_alpha - PK_ae) + PK_ae',
                       'dimensionless'),
        AssignmentRule('PKp_alpha_inp',
                       '(1 dimensionless - PKp_f) * (PKp_alpha - PK_ae) + PK_ae',
                       'dimensionless'),
        AssignmentRule('PKn_pep_inp',
                       '(1 dimensionless - PKn_f) *(PKn_k_pep - PKn_k_pep_end) + PKn_k_pep_end',
                       'mM'),
        AssignmentRule('PKp_pep_inp',
                       '(1 dimensionless - PKp_f) *(PKp_k_pep - PKn_k_pep_end) + PKn_k_pep_end',
                       'mM'),
        AssignmentRule('PKn',
                       'f_gly * PK_Vmax * PKn_alpha_inp * pep^PKn_n/(PKn_pep_inp^PKn_n + pep^PKn_n) * '
                       'adp/(adp + PK_k_adp) * ( PKn_ba + (1 dimensionless - PKn_ba) * PKn_f )',
                       'mmole_per_min'),
        AssignmentRule('PKp',
                       'f_gly * PK_Vmax * PKp_alpha_inp * pep^PKp_n/(PKp_pep_inp^PKp_n + pep^PKp_n) * '
                       'adp/(adp + PK_k_adp) * ( PKp_ba + (1 dimensionless - PKp_ba) * PKp_f )',
                       'mmole_per_min'),
    ],
    formula=('(1 dimensionless - gamma)* PKn + gamma * PKp', 'mmole_per_min')
)

PEPCK = Reaction(
    sid='PEPCK',
    name='PEPCK cyto',
    equation='gtp + oaa <-> co2 + gdp + pep []',
    # C10H12N5O14P3 (-4) + C4H2O5 (-2) <-> CO2 (0) + C10H12N5O11P2 (-3) + C3H2O6P (-3)
    compartment='cyto',
    sboTerm=SBO_BIOCHEMICAL_REACTION,
    pars=[
        Parameter('PEPCK_keq', 3.369565215864287E2, 'mM'),
        Parameter('PEPCK_k_pep', 0.237, 'mM'),
        Parameter('PEPCK_k_gdp', 0.0921, 'mM'),
        Parameter('PEPCK_k_co2', 25.5, 'mM'),
        Parameter('PEPCK_k_oaa', 0.0055, 'mM'),
        Parameter('PEPCK_k_gtp', 0.0222, 'mM'),
        Parameter('PEPCK_Vmax', 0, 'mmole_per_min'),
    ],
    formula=(
    'f_gly * PEPCK_Vmax / (PEPCK_k_oaa * PEPCK_k_gtp) * (oaa*gtp - pep*gdp*co2/PEPCK_keq) / '
    '( (1 dimensionless + oaa/PEPCK_k_oaa)*(1 dimensionless +gtp/PEPCK_k_gtp) + '
    '(1 dimensionless + pep/PEPCK_k_pep)*(1 dimensionless + gdp/PEPCK_k_gdp)*'
    '(1 dimensionless +co2/PEPCK_k_co2) - 1 dimensionless)', 'mmole_per_min')
)

PEPCKM = Reaction(
    sid='PEPCKM',
    name='PEPCK mito',
    equation='gtp_mito + oaa_mito <-> co2_mito + gdp_mito + pep_mito []',
    # C10H12N5O14P3 (-4) + C4H2O5 (-2) <-> CO2 (0) + C10H12N5O11P2 (-3) + C3H2O6P (-3)
    compartment='mito',
    sboTerm=SBO_BIOCHEMICAL_REACTION,
    pars=[
        Parameter('PEPCKM_Vmax', 546, 'mmole_per_min'),
    ],
    formula=('f_gly * PEPCKM_Vmax / (PEPCK_k_oaa * PEPCK_k_gtp) * '
             '(oaa_mito*gtp_mito - pep_mito*gdp_mito*co2_mito/PEPCK_keq) / ( (1 dimensionless + oaa_mito/PEPCK_k_oaa)*'
             '(1 dimensionless + gtp_mito/PEPCK_k_gtp) + '
             '(1 dimensionless + pep_mito/PEPCK_k_pep)*(1 dimensionless + gdp_mito/PEPCK_k_gdp)*'
             '(1 dimensionless +co2_mito/PEPCK_k_co2) - 1 dimensionless)',
             'mmole_per_min')
)

PC = Reaction(
    sid='PC',
    name='Pyruvate Carboxylase',
    equation='atp_mito + pyr_mito + co2_mito + h2o_mito => adp_mito + oaa_mito + phos_mito + 2 h [acoa_mito]',
    # C10H12N5O13P3 (-4) + C3H3O3 (-1) + CO2 (0) + H2O (0) => C10H12N5O10P2 (-3) + C4H2O5 (-2) + HO4P (-2) + 2H (+2)
    compartment='mito',
    sboTerm=SBO_BIOCHEMICAL_REACTION,
    pars=[
        Parameter('PC_k_atp', 0.22, 'mM'),
        Parameter('PC_k_pyr', 0.22, 'mM'),
        Parameter('PC_k_co2', 3.2, 'mM'),
        Parameter('PC_k_acoa', 0.015, 'mM'),
        Parameter('PC_n', 2.5, 'dimensionless'),
        Parameter('PC_Vmax', 168, 'mmole_per_min'),
    ],
    formula=(
    'f_gly * PC_Vmax * atp_mito/(PC_k_atp + atp_mito) * pyr_mito/(PC_k_pyr + pyr_mito) * '
    'co2_mito/(PC_k_co2 + co2_mito) * acoa_mito^PC_n / (acoa_mito^PC_n + PC_k_acoa^PC_n)',
    'mmole_per_min')
)

LDH = Reaction(
    sid='LDH',
    name='Lactate Dehydrogenase',
    equation='pyr + nadh + h <-> lac + nad []',
    # C3H3O3 (-1) + C21H27N7O14P2 (-2) + H (+1) <-> C3H5O3 (-1) + C21H26N7O14P2 (-1)
    compartment='cyto',
    pars=[
        Parameter('LDH_keq', 2.783210760047520E-004, 'dimensionless'),
        Parameter('LDH_k_pyr', 0.495, 'mM'),
        Parameter('LDH_k_lac', 31.98, 'mM'),
        Parameter('LDH_k_nad', 0.984, 'mM'),
        Parameter('LDH_k_nadh', 0.027, 'mM'),
        Parameter('LDH_Vmax', 12.6, 'mmole_per_min'),
    ],
    formula=(
    'f_gly * LDH_Vmax / (LDH_k_pyr * LDH_k_nadh) * (pyr*nadh - lac*nad/LDH_keq) / '
    '( (1 dimensionless +nadh/LDH_k_nadh)*(1 dimensionless +pyr/LDH_k_pyr) + '
    '(1 dimensionless +lac/LDH_k_lac) * (1 dimensionless +nad/LDH_k_nad) - 1 dimensionless)',
    'mmole_per_min')
)

LACT = Reaction(
    sid='LACT',
    name='Lactate transport (import)',
    equation='lac_ext <-> lac []',
    # C3H5O3 (-1) <-> C3H5O3 (-1)
    compartment='pm',
    sboTerm=SBO_TRANSPORT_REACTION,
    pars=[
        Parameter('LACT_keq', 1, 'dimensionless'),
        Parameter('LACT_k_lac', 0.8, 'mM'),
        Parameter('LACT_Vmax', 5.418, 'mmole_per_min'),
    ],
    formula=('f_gly * LACT_Vmax/LACT_k_lac * (lac_ext - lac/LACT_keq) / '
             '(1 dimensionless + lac_ext/LACT_k_lac + lac/LACT_k_lac)',
             'mmole_per_min')
)

PYRTM = Reaction(
    sid='PYRTM',
    name='Pyruvate transport (mito)',
    equation='pyr <-> pyr_mito []',
    # C3H3O3 (-1) <-> C3H3O3 (-1)
    compartment='mm',
    sboTerm=SBO_TRANSPORT_REACTION,
    pars=[
        Parameter('PYRTM_keq', 1, 'dimensionless'),
        Parameter('PYRTM_k_pyr', 0.1, 'mM'),
        Parameter('PYRTM_Vmax', 42, 'mmole_per_min'),
    ],
    formula=('f_gly * PYRTM_Vmax/PYRTM_k_pyr * (pyr - pyr_mito/PYRTM_keq) / '
             '(1 dimensionless + pyr/PYRTM_k_pyr + pyr_mito/PYRTM_k_pyr)',
             'mmole_per_min')
)

PEPTM = Reaction(
    sid='PEPTM',
    name='PEP Transport (export mito)',
    equation='pep_mito <-> pep []',
    # C3H2O6P (-3) <-> C3H2O6P (-3)
    compartment='mm',
    sboTerm=SBO_TRANSPORT_REACTION,
    pars=[
        Parameter('PEPTM_keq', 1, 'dimensionless'),
        Parameter('PEPTM_k_pep', 0.1, 'mM'),
        Parameter('PEPTM_Vmax', 33.6, 'mmole_per_min'),
    ],
    formula=('f_gly * PEPTM_Vmax/PEPTM_k_pep * (pep_mito - pep/PEPTM_keq) / '
             '(1 dimensionless + pep/PEPTM_k_pep + pep_mito/PEPTM_k_pep)',
             'mmole_per_min')
)

PDH = Reaction(
    sid='PDH',
    name='Pyruvate Dehydrogenase',
    equation='pyr_mito + coa_mito + nad_mito => acoa_mito + co2_mito + nadh_mito []',
    # C3H3O3 (-1) + C21H32N7O16P3S (-4) + C21H26N7O14P2 (-1) => C23H34N7O17P3S (-4) + CO2 (0) + C21H27N7O14P2 (-2)
    compartment='mito',
    sboTerm=SBO_BIOCHEMICAL_REACTION,
    pars=[
        Parameter('PDH_k_pyr', 0.025, 'mM'),
        Parameter('PDH_k_coa', 0.013, 'mM'),
        Parameter('PDH_k_nad', 0.050, 'mM'),
        Parameter('PDH_ki_acoa', 0.035, 'mM'),
        Parameter('PDH_ki_nadh', 0.036, 'mM'),
        Parameter('PDHn_alpha', 5, 'dimensionless'),
        Parameter('PDHp_alpha', 1, 'dimensionless'),
        Parameter('PDH_Vmax', 13.44, 'mmole_per_min'),
    ],
    rules=[
        AssignmentRule('PDH_base',
                       'f_gly * PDH_Vmax * pyr_mito/(pyr_mito + PDH_k_pyr) * '
                       'nad_mito/(nad_mito + PDH_k_nad*(1 dimensionless + nadh_mito/PDH_ki_nadh)) * '
                       'coa_mito/(coa_mito + PDH_k_coa*(1 dimensionless +acoa_mito/PDH_ki_acoa))',
                       'mmole_per_min'),
        AssignmentRule('PDHn', 'PDH_base * PDHn_alpha', 'mmole_per_min'),
        AssignmentRule('PDHp', 'PDH_base * PDHp_alpha', 'mmole_per_min'),
    ],
    formula=('(1 dimensionless - gamma) * PDHn + gamma*PDHp', 'mmole_per_min')
)

CS = Reaction(
    sid='CS',
    name='Citrate Synthase',
    equation='acoa_mito + oaa_mito + h2o_mito <-> cit_mito + coa_mito + h_mito []',
    # C23H34N7O17P3S (-4) + H2O (0) + C4H2O5 (-2) <-> C6H5O7 (-3) + C21H32N7O16P3S (-4) + H (+1)
    compartment='mito',
    sboTerm=SBO_BIOCHEMICAL_REACTION,
    pars=[
        Parameter('CS_keq', 2.665990308427589E5, 'dimensionless'),
        Parameter('CS_k_oaa', 0.002, 'mM'),
        Parameter('CS_k_acoa', 0.016, 'mM'),
        Parameter('CS_k_cit', 0.420, 'mM'),
        Parameter('CS_k_coa', 0.070, 'mM'),
        Parameter('CS_Vmax', 4.2, 'mmole_per_min'),
    ],
    formula=(
    'f_gly * CS_Vmax/(CS_k_oaa * CS_k_acoa) * (acoa_mito*oaa_mito - cit_mito*coa_mito/CS_keq) / '
    '( (1 dimensionless +acoa_mito/CS_k_acoa)*(1 dimensionless +oaa_mito/CS_k_oaa) + '
    '(1 dimensionless +cit_mito/CS_k_cit)*(1 dimensionless +coa_mito/CS_k_coa) -1 dimensionless)',
    'mmole_per_min')
)

NDKGTPM = Reaction(
    sid='NDKGTPM',
    name='Nucleoside-diphosphate kinase (ATP, GTP) mito',
    equation='atp_mito + gdp_mito <-> adp_mito + gtp_mito []',
    # C10H12N5O13P3 (-4) + C10H12N5O11P2 (-3) <-> C10H12N5O10P2 (-3) + C10H12N5O14P3 (-4)
    compartment='mito',
    sboTerm=SBO_BIOCHEMICAL_REACTION,
    pars=[
        Parameter('NDKGTPM_keq', 1, 'dimensionless'),
        Parameter('NDKGTPM_k_atp', 1.33, 'mM'),
        Parameter('NDKGTPM_k_adp', 0.042, 'mM'),
        Parameter('NDKGTPM_k_gtp', 0.15, 'mM'),
        Parameter('NDKGTPM_k_gdp', 0.031, 'mM'),
        Parameter('NDKGTPM_Vmax', 420, 'mmole_per_min'),
    ],
    formula=('f_gly * NDKGTPM_Vmax / (NDKGTPM_k_atp * NDKGTPM_k_gdp) * '
             '(atp_mito*gdp_mito - adp_mito*gtp_mito/NDKGTPM_keq) / '
             '( (1 dimensionless + atp_mito/NDKGTPM_k_atp)*(1 dimensionless + gdp_mito/NDKGTPM_k_gdp) + '
             '(1 dimensionless + adp_mito/NDKGTPM_k_adp)*(1 dimensionless + gtp_mito/NDKGTPM_k_gtp) - 1 dimensionless)',
             'mmole_per_min')
)

OAAFLX = Reaction(
    sid='OAAFLX',
    name='oxalacetate influx',
    equation='=> oaa_mito []',
    # ->
    compartment='mito',
    sboTerm=SBO_EXCHANGE_REACTION,
    pars=[
        Parameter('OAAFLX_Vmax', 0, 'mmole_per_min'),
    ],
    formula=('f_gly * OAAFLX_Vmax', 'mmole_per_min')
)

ACOAFLX = Reaction(
    sid='ACOAFLX',
    name='acetyl-coa efflux',
    equation='acoa_mito => []',
    sboTerm=SBO_EXCHANGE_REACTION,
    compartment='mito',
    pars=[
        Parameter('ACOAFLX_Vmax', 0, 'mmole_per_min'),
    ],
    formula=('f_gly * ACOAFLX_Vmax', 'mmole_per_min')
)

CITFLX = Reaction(
    sid='CITFLX',
    name='citrate efflux',
    equation='cit_mito => []',
    sboTerm=SBO_EXCHANGE_REACTION,
    compartment='mito',
    pars=[
        Parameter('CITFLX_Vmax', 0, 'mmole_per_min'),
    ],
    formula=('f_gly * CITFLX_Vmax', 'mmole_per_min')
)

reactions = [
    GLUT2,
    GK,
    G6PASE,
    GPI,
    G16PI,
    UPGASE,
    PPASE,
    GS,
    GP,
    NDKGTP,
    NDKUTP,
    AK,
    PFK2,
    FBP2,
    PFK1,
    FBP1,
    ALD,
    TPI,
    GAPDH,
    PGK,
    PGM,
    EN,
    PK,
    PEPCK,
    PEPCKM,
    PC,
    LDH,
    LACT,
    PYRTM,
    PEPTM,
    PDH,
    CS,
    NDKGTPM,
    OAAFLX,
    ACOAFLX,
    CITFLX,
]
