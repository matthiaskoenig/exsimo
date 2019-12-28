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
from sbmlutils.modelcreator import creator

from pyexsimo.model import templates
from pyexsimo.model import liver_glucose_reactions as Reactions

# -----------------------------------------------------------------------------
# Liver Metabolism
# -----------------------------------------------------------------------------
mid = 'liver_glucose'
version = 7
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

model_units = ModelUnits(time='min',
                         extent='mmole',
                         substance='mmole',
                         length='m',
                         area='m2',
                         volume=UNIT_KIND_LITRE)

units = list()
functions = list()
compartments = list()
species = list()
parameters = list()
names = list()
assignments = list()
rules = list()
reactions = list()
ports = list()

# -----------------------------------------------------------------------------
# Units
# -----------------------------------------------------------------------------
units.extend([
    Unit('l', [(UNIT_KIND_LITRE, 1.0)], port=True),
    Unit('s', [(UNIT_KIND_SECOND, 1.0)], port=True),
    Unit('kg', [(UNIT_KIND_KILOGRAM, 1.0)], port=True),
    Unit('m', [(UNIT_KIND_METRE, 1.0)], port=True),
    Unit('m2', [(UNIT_KIND_METRE, 2.0)], port=True),
    Unit('m3', [(UNIT_KIND_METRE, 3.0)], port=True),
    Unit('per_s', [(UNIT_KIND_SECOND, -1.0)], port=True),
    Unit('min', [(UNIT_KIND_SECOND, 1.0, 0, 60)], port=True),
    Unit('s_per_min', [(UNIT_KIND_SECOND, 1.0),
                          (UNIT_KIND_SECOND, -1.0, 0, 60)], port=True),
    Unit('mmole', [(UNIT_KIND_MOLE, 1.0, -3, 1.0)], port=True),
    Unit('mM', [(UNIT_KIND_MOLE, 1.0),
                   (UNIT_KIND_METRE, -3.0)], port=True),
    Unit('per_mM', [(UNIT_KIND_METRE, 3.0),
                       (UNIT_KIND_MOLE, -1.0)], port=True),
    Unit('mM2', [(UNIT_KIND_MOLE, 2.0),
                    (UNIT_KIND_METRE, -6.0)], port=True),
    Unit('pmol', [(UNIT_KIND_MOLE, 1.0, -12, 1.0)], port=True),
    Unit('pM', [(UNIT_KIND_MOLE, 1.0, -12, 1.0),
                   (UNIT_KIND_LITRE, -1.0)], port=True),
    Unit('mmole_per_min', [(UNIT_KIND_MOLE, 1.0, -3, 1.0),
                              (UNIT_KIND_SECOND, -1.0, 0, 60)], port=True),
    Unit('mumole_per_mmole', [(UNIT_KIND_MOLE, 1.0, -6, 1.0),
                              (UNIT_KIND_MOLE, -1.0, -3, 1.0)], port=True),
    Unit('mumole_per_mmole_kg', [(UNIT_KIND_MOLE, 1.0, -6, 1.0),
                              (UNIT_KIND_MOLE, -1.0, -3, 1.0), (UNIT_KIND_KILOGRAM, -1.0, 0, 1.0)], port=True),
    Unit('mumol_per_min_kg', [(UNIT_KIND_MOLE, 1.0, -6, 1.0),
                                 (UNIT_KIND_SECOND, -1.0, 0, 60), (UNIT_KIND_KILOGRAM, -1.0)], port=True),

    # consistency of submodels
    Unit('mg', [(UNIT_KIND_GRAM, 1.0, -3, 1.0)], port=True),
    Unit('ml', [(UNIT_KIND_LITRE, 1.0, -3, 1.0)], port=True),
    Unit('per_min', [(UNIT_KIND_SECOND, -1.0, 0, 60)], port=True),
    Unit('mmole_per_min_l', [(UNIT_KIND_MOLE, 1.0, -3, 1),
                               (UNIT_KIND_SECOND, -1.0, 0, 60), (UNIT_KIND_LITRE, -1.0, 0, 1.0)], port=True),
])


# --- functions ---
functions.extend([
    Function('max', 'lambda(x,y, piecewise(x,gt(x,y),y) )', name='minimum of arguments'),
    Function('min', 'lambda(x,y, piecewise(x,lt(x,y),y) )', name='maximum of arguments'),
])


# --- compartments ---
compartments.extend([
    Compartment(sid='ext', unit=UNIT_KIND_LITRE, constant=False, value=1.0, name='blood', port=True),
    Compartment(sid='cyto', unit=UNIT_KIND_LITRE, constant=False, value='V_cyto', name='cytosol', port=True),
    Compartment(sid='mito', unit=UNIT_KIND_LITRE, constant=False, value='V_mito', name='mitochondrion'),
    Compartment(sid='pm', spatialDimensions=2, unit='m2', constant=True, value=1.0, name='plasma membrane'),
    Compartment(sid='mm', spatialDimensions=2, unit='m2', constant=True, value=1.0, name='mitochondrial membrane'),
])


# --- species ---
species.extend([
    Species('Aatp', compartment='cyto', initialConcentration=2.8000, substanceUnit='mmole', boundaryCondition=True, hasOnlySubstanceUnits=True, name='ATP'),
    Species('Aadp', compartment='cyto', initialConcentration=0.8000, substanceUnit='mmole', boundaryCondition=True, hasOnlySubstanceUnits=True, name='ADP'),
    Species('Aamp', compartment='cyto', initialConcentration=0.1600, substanceUnit='mmole', boundaryCondition=True, hasOnlySubstanceUnits=True, name='AMP'),
    Species('Autp', compartment='cyto', initialConcentration=0.2700, substanceUnit='mmole', boundaryCondition=False, hasOnlySubstanceUnits=True, name='UTP'),
    Species('Audp', compartment='cyto', initialConcentration=0.0900, substanceUnit='mmole', boundaryCondition=False, hasOnlySubstanceUnits=True, name='UDP'),
    Species('Agtp', compartment='cyto', initialConcentration=0.2900, substanceUnit='mmole', boundaryCondition=False, hasOnlySubstanceUnits=True, name='GTP'),
    Species('Agdp', compartment='cyto', initialConcentration=0.1000, substanceUnit='mmole', boundaryCondition=False, hasOnlySubstanceUnits=True, name='GDP'),
    Species('Anad', compartment='cyto', initialConcentration=1.2200, substanceUnit='mmole', boundaryCondition=True, hasOnlySubstanceUnits=True, name='NAD+'),
    Species('Anadh', compartment='cyto', initialConcentration=0.56E-3, substanceUnit='mmole', boundaryCondition=True, hasOnlySubstanceUnits=True, name='NADH'),
    Species('Aphos', compartment='cyto', initialConcentration=5.0000, substanceUnit='mmole', boundaryCondition=True, hasOnlySubstanceUnits=True, name='phosphate'),
    Species('App', compartment='cyto', initialConcentration=0.0080, substanceUnit='mmole', boundaryCondition=False, hasOnlySubstanceUnits=True, name='pyrophosphate'),
    Species('Aco2', compartment='cyto', initialConcentration=5.0000, substanceUnit='mmole', boundaryCondition=True, hasOnlySubstanceUnits=True, name='CO2'),
    Species('Ah2o', compartment='cyto', initialConcentration=0.0, substanceUnit='mmole', boundaryCondition=True, hasOnlySubstanceUnits=True, name='H2O'),
    Species('Ah', compartment='cyto', initialConcentration=0.0, substanceUnit='mmole', boundaryCondition=True, hasOnlySubstanceUnits=True, name='H+'),

    Species('Aglc1p', compartment='cyto', initialConcentration=0.0120, substanceUnit='mmole', boundaryCondition=False, hasOnlySubstanceUnits=True,
               name='glucose-1 phosphate'),
    Species('Audpglc', compartment='cyto', initialConcentration=0.3800, substanceUnit='mmole', boundaryCondition=False, hasOnlySubstanceUnits=True, name='UDP-glucose'),
    Species('Aglyglc', compartment='cyto', initialConcentration=250.0000, substanceUnit='mmole', boundaryCondition=False, hasOnlySubstanceUnits=True, name='glycogen'),
    Species('Aglc', compartment='cyto', initialConcentration=5.0000, substanceUnit='mmole', boundaryCondition=False, hasOnlySubstanceUnits=True, name='glucose'),
    Species('Aglc6p', compartment='cyto', initialConcentration=0.1200, substanceUnit='mmole', boundaryCondition=False, hasOnlySubstanceUnits=True,
               name='glucose-6 phosphate'),
    Species('Afru6p', compartment='cyto', initialConcentration=0.0500, substanceUnit='mmole', boundaryCondition=False, hasOnlySubstanceUnits=True,
               name='fructose-6 phosphate'),
    Species('Afru16bp', compartment='cyto', initialConcentration=0.0200, substanceUnit='mmole', boundaryCondition=False, hasOnlySubstanceUnits=True,
               name='fructose-16 bisphosphate'),
    Species('Afru26bp', compartment='cyto', initialConcentration=0.0040, substanceUnit='mmole', boundaryCondition=False, hasOnlySubstanceUnits=True,
               name='fructose-26 bisphosphate'),
    Species('Agrap', compartment='cyto', initialConcentration=0.1000, substanceUnit='mmole', boundaryCondition=False, hasOnlySubstanceUnits=True,
               name='glyceraldehyde 3-phosphate'),
    Species('Adhap', compartment='cyto', initialConcentration=0.0300, substanceUnit='mmole', boundaryCondition=False, hasOnlySubstanceUnits=True,
               name='dihydroxyacetone phosphate'),
    Species('Abpg13', compartment='cyto', initialConcentration=0.3000, substanceUnit='mmole', boundaryCondition=False, hasOnlySubstanceUnits=True,
               name='13-bisphospho-glycerate'),
    Species('Apg3', compartment='cyto', initialConcentration=0.2700, substanceUnit='mmole', boundaryCondition=False, hasOnlySubstanceUnits=True, name='3-phosphoglycerate'),
    Species('Apg2', compartment='cyto', initialConcentration=0.0300, substanceUnit='mmole', boundaryCondition=False, hasOnlySubstanceUnits=True, name='2-phosphoglycerate'),
    Species('Apep', compartment='cyto', initialConcentration=0.1500, substanceUnit='mmole', boundaryCondition=False, hasOnlySubstanceUnits=True, name='phosphoenolpyruvate'),
    Species('Apyr', compartment='cyto', initialConcentration=0.1000, substanceUnit='mmole', boundaryCondition=False, hasOnlySubstanceUnits=True, name='pyruvate'),
    Species('Aoaa', compartment='cyto', initialConcentration=0.0100, substanceUnit='mmole', boundaryCondition=False, hasOnlySubstanceUnits=True, name='oxaloacetate'),
    Species('Alac', compartment='cyto', initialConcentration=0.5000, substanceUnit='mmole', boundaryCondition=False, hasOnlySubstanceUnits=True, name='lactate'),

    Species('Aglc_ext', compartment='ext', initialConcentration=3.0000, substanceUnit='mmole', boundaryCondition=True, hasOnlySubstanceUnits=True, name='glucose', port=True),
    Species('Alac_ext', compartment='ext', initialConcentration=1.2000, substanceUnit='mmole', boundaryCondition=True, hasOnlySubstanceUnits=True, name='lactate', port=True),

    Species('Aco2_mito', compartment='mito', initialConcentration=5.0000, substanceUnit='mmole', boundaryCondition=True, hasOnlySubstanceUnits=True, name='CO2'),
    Species('Aphos_mito', compartment='mito', initialConcentration=5.0000, substanceUnit='mmole', boundaryCondition=True, hasOnlySubstanceUnits=True, name='phosphate'),
    Species('Aoaa_mito', compartment='mito', initialConcentration=0.0100, substanceUnit='mmole', boundaryCondition=False, hasOnlySubstanceUnits=True, name=' oxaloacetate'),
    Species('Apep_mito', compartment='mito', initialConcentration=0.1500, substanceUnit='mmole', boundaryCondition=False, hasOnlySubstanceUnits=True,
               name='phosphoenolpyruvate'),
    Species('Aacoa_mito', compartment='mito', initialConcentration=0.0400, substanceUnit='mmole', boundaryCondition=True, hasOnlySubstanceUnits=True,
               name='acetyl-coenzyme A'),
    Species('Apyr_mito', compartment='mito', initialConcentration=0.1000, substanceUnit='mmole', boundaryCondition=False, hasOnlySubstanceUnits=True, name='pyruvate'),
    Species('Acit_mito', compartment='mito', initialConcentration=0.3200, substanceUnit='mmole', boundaryCondition=True, hasOnlySubstanceUnits=True, name='citrate'),

    Species('Aatp_mito', compartment='mito', initialConcentration=2.8000, substanceUnit='mmole', boundaryCondition=True, hasOnlySubstanceUnits=True, name='ATP'),
    Species('Aadp_mito', compartment='mito', initialConcentration=0.8000, substanceUnit='mmole', boundaryCondition=True, hasOnlySubstanceUnits=True, name='ADP'),
    Species('Agtp_mito', compartment='mito', initialConcentration=0.2900, substanceUnit='mmole', boundaryCondition=False, hasOnlySubstanceUnits=True, name='GTP'),
    Species('Agdp_mito', compartment='mito', initialConcentration=0.1000, substanceUnit='mmole', boundaryCondition=False, hasOnlySubstanceUnits=True, name='GDP'),
    Species('Acoa_mito', compartment='mito', initialConcentration=0.0550, substanceUnit='mmole', boundaryCondition=True, hasOnlySubstanceUnits=True, name='coenzyme A'),
    Species('Anadh_mito', compartment='mito', initialConcentration=0.2400, substanceUnit='mmole', boundaryCondition=True, hasOnlySubstanceUnits=True, name='NADH'),
    Species('Anad_mito', compartment='mito', initialConcentration=0.9800, substanceUnit='mmole', boundaryCondition=True, hasOnlySubstanceUnits=True, name='NAD+'),
    Species('Ah2o_mito', compartment='mito', initialConcentration=0.0, substanceUnit='mmole', boundaryCondition=True, hasOnlySubstanceUnits=True, name='H20'),
    Species('Ah_mito', compartment='mito', initialConcentration=0.0, substanceUnit='mmole', boundaryCondition=True, hasOnlySubstanceUnits=True, name='H+'),
])

# Concentration
for s in species:
    aid = s.sid[1:]
    rules.append(
        AssignmentRule(f'{aid}', f'{s.sid}/{s.compartment}', 'mM', name=f'{s.name} concentration'),
    )


# --- parameters ---
parameters.extend([
    Parameter('scale', 1.0, 'dimensionless', True, name='scaling factor for rates'),
    Parameter('V_cyto', 1.0, UNIT_KIND_LITRE, True, name='cytosolic volume'),
    Parameter('f_mito', 0.2, 'dimensionless', True, name='mitochondrial volume factor'),
    Parameter('Vliver', 1.5, UNIT_KIND_LITRE, True, name='liver volume'),
    Parameter('fliver', 0.583333333333334, 'dimensionless', True, name='parenchymal fraction liver'),
    Parameter('bodyweight', 70, 'kg', True, name='bodyweight'),

    Parameter('sec_per_min', 60, 's_per_min', True, name='time conversion'),
    Parameter('mumole_per_mmole', 1000, 'mumole_per_mmole', True, name='amount conversion'),

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
])

# --- assignment rules ---
rules.extend([

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
    AssignmentRule('ins', 'x_ins2 + (x_ins1-x_ins2) * glc_ext^x_ins4/(glc_ext^x_ins4 + x_ins3^x_ins4)', 'pM',
                      name='insulin'),
    AssignmentRule('ins_norm', 'max(0.0 pM, ins-x_ins2)', 'pM', name='insulin normalized'),
    AssignmentRule('glu',
                      'x_glu2 + (x_glu1-x_glu2)*(1 dimensionless - glc_ext^x_glu4/(glc_ext^x_glu4 + x_glu3^x_glu4))',
                      'pM', name='glucagon'),
    AssignmentRule('glu_norm', 'max(0.0 pM, glu-x_glu2)', 'pM', name='glucagon normalized'),
    AssignmentRule('epi',
                      'x_epi2 + (x_epi1-x_epi2) * (1 dimensionless - glc_ext^x_epi4/(glc_ext^x_epi4 + x_epi3^x_epi4))',
                      'pM', name='epinephrine'),
    AssignmentRule('epi_norm', 'max(0.0 pM, epi-x_epi2)', 'pM', name='epinephrine normalized'),
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
    AssignmentRule('nadh_mito_tot', 'nadh_mito + nad_mito', 'mM', name='NADH mito balance'),
    AssignmentRule('atp_mito_tot', 'atp_mito + adp_mito', 'mM', name='ATP mito balance'),
    AssignmentRule('gtp_mito_tot', 'gtp_mito + gdp_mito', 'mM', name='GTP mito balance'),

    # whole liver output
    AssignmentRule('HGP', 'GLUT2 * flux_conversion', 'mumol_per_min_kg', name='hepatic glucose production/utilization'),
    AssignmentRule('GNG', 'GPI * flux_conversion', 'mumol_per_min_kg', name='gluconeogenesis/glycolysis'),
    AssignmentRule('GLY', '-G16PI * flux_conversion', 'mumol_per_min_kg', name='glycogenolysis/glycogen synthesis'),
])


# --- reactions ---
reactions.extend([
    Reactions.GLUT2,
    Reactions.GK,
    Reactions.G6PASE,
    Reactions.GPI,
    Reactions.G16PI,
    Reactions.UPGASE,
    Reactions.PPASE,
    Reactions.GS,
    Reactions.GP,
    Reactions.NDKGTP,
    Reactions.NDKUTP,
    Reactions.AK,
    Reactions.PFK2,
    Reactions.FBP2,
    Reactions.PFK1,
    Reactions.FBP1,
    Reactions.ALD,
    Reactions.TPI,
    Reactions.GAPDH,
    Reactions.PGK,
    Reactions.PGM,
    Reactions.EN,
    Reactions.PK,
    Reactions.PEPCK,
    Reactions.PEPCKM,
    Reactions.PC,
    Reactions.LDH,
    Reactions.LACT,
    Reactions.PYRTM,
    Reactions.PEPTM,
    Reactions.PDH,
    Reactions.CS,
    Reactions.NDKGTPM,
    Reactions.OAAFLX,
    Reactions.ACOAFLX,
    Reactions.CITFLX,
])
