"""
Reactions and transporters of glucose metabolism.
"""
from sbmlutils.units import *
from sbmlutils.annotation.sbo import *
from sbmlutils.factory import *

# -----------------------------------------------------------------------------
#    REACTIONS
# -----------------------------------------------------------------------------
GLUT2 = Reaction(
    sid='GLUT2',
    name='GLUT2 glucose transporter',
    equation='Aglc_ext <-> Aglc []',
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
             '(1 dimensionless + glc_ext/GLUT2_k_glc + glc/GLUT2_k_glc)', 'mmole_per_min')
)

GK = Reaction(
    sid='GK',
    name='Glucokinase',
    equation='Aglc + Aatp => Aglc6p + Aadp + Ah [Aglc1p, Afru6p]',
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
       AssignmentRule('GK_gc_free', '(glc^GK_n_gkrp / (glc^GK_n_gkrp + GK_k_glc1^GK_n_gkrp) ) * '
                                       '(1 dimensionless - GK_b*fru6p/(fru6p + GK_k_fru6p))', 'dimensionless'),
    ],
    formula=('f_gly * GK_Vmax * GK_gc_free * (atp/(GK_k_atp + atp)) * (glc^GK_n/(glc^GK_n + GK_k_glc^GK_n))',
             'mmole_per_min')
)

G6PASE = Reaction(
    sid='G6PASE',
    name='D-Glucose-6-phosphate Phosphatase',
    equation='Aglc6p + Ah2o => Aglc + Aphos []',
    # C6H11O9P (-2) + H2O (0) -> C6H12O6 (0) + HO4P (-2)
    compartment='cyto',
    sboTerm=SBO_BIOCHEMICAL_REACTION,
    pars=[
        Parameter('G6PASE_k_glc6p', 2, 'mM'),
        Parameter('G6PASE_Vmax', 18.9, 'mmole_per_min'),
    ],
    formula=('f_gly * G6PASE_Vmax * (glc6p / (G6PASE_k_glc6p + glc6p))', 'mmole_per_min')
)

GPI = Reaction(
    sid='GPI',
    name='D-Glucose-6-phosphate Isomerase',
    equation='Aglc6p <-> Afru6p []',
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
             '(1 dimensionless + glc6p/GPI_k_glc6p + fru6p/GPI_k_fru6p)', 'mmole_per_min')
)

G16PI = Reaction(
    sid='G16PI',
    name='Glucose 1-phosphate 1,6-phosphomutase',
    equation='Aglc1p <-> Aglc6p []',
    # C6H11O9P (-2) <-> C6H11O9P (-2)
    compartment='cyto',
    sboTerm=SBO_BIOCHEMICAL_REACTION,
    pars=[
       Parameter('G16PI_keq', 15.717554082151441, 'dimensionless'),
       Parameter('G16PI_k_glc6p', 0.67, 'mM'),
       Parameter('G16PI_k_glc1p', 0.045, 'mM'),
       Parameter('G16PI_Vmax', 100, 'mmole_per_min'),
    ],
    formula=('f_glyglc * (G16PI_Vmax/G16PI_k_glc1p) * (glc1p - glc6p/G16PI_keq) / '
             '(1 dimensionless + glc1p/G16PI_k_glc1p + glc6p/G16PI_k_glc6p)', 'mmole_per_min')
)

UPGASE = Reaction(
    sid='UPGASE',
    name='UTP:Glucose-1-phosphate uridylyltransferase',
    equation='Aglc1p + Ah + Autp <-> App + Audpglc []',
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
    formula=('f_glyglc * UPGASE_Vmax/(UPGASE_k_utp*UPGASE_k_glc1p) * (utp*glc1p - udpglc*pp/UPGASE_keq) / '
             '( (1 dimensionless + utp/UPGASE_k_utp)*(1 dimensionless + glc1p/UPGASE_k_glc1p) + '
             '(1 dimensionless + udpglc/UPGASE_k_udpglc)*(1 dimensionless + pp/UPGASE_k_pp) - 1 dimensionless)',
             'mmole_per_min')
)

PPASE = Reaction(
    sid='PPASE',
    name='Pyrophosphate phosphohydrolase',
    equation='App + Ah2o => Ah + 2 Aphos []',
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
    equation='Audpglc + Ah2o => Audp + Ah + Aglyglc [Aglc6p]',
    # C15H22N2O17P2 (-2) + H20 (0) => C9H11N2O12P2 (-3) + H (+1) + C6H12O6(0)
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
       AssignmentRule('GS_fs', '(1 dimensionless + GS_k1_max) * (GS_C - glyglc)/'
                                  '( (GS_C - glyglc) + GS_k1_max * GS_C)', 'dimensionless'),
       AssignmentRule('GSn_k_udpglc', 'GSn_k1 / (glc6p + GSn_k2)', 'mM'),
       AssignmentRule('GSp_k_udpglc', 'GSp_k1 / (glc6p + GSp_k2)', 'mM'),
       AssignmentRule('GSn', 'f_glyglc * GS_Vmax * GS_fs * udpglc / (GSn_k_udpglc + udpglc)', 'mmole_per_min'),
       AssignmentRule('GSp', 'f_glyglc * GS_Vmax * GS_fs * udpglc / (GSp_k_udpglc + udpglc)', 'mmole_per_min'),
    ],
    formula=('(1 dimensionless - gamma)*GSn + gamma*GSp', 'mmole_per_min')
)
"""
Synthesis of glycogen from uridine diphosphate glucose in liver.
PMID: 14415527
"""

GP = Reaction(
    sid='GP',
    name='Glycogen-Phosphorylase',
    equation='Aglyglc + Aphos <-> Aglc1p + Ah2o [Aphos, Aamp, Aglc]',
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
       AssignmentRule('GP_fmax', '(1 dimensionless +GS_k1_max) * glyglc /( glyglc + GS_k1_max * GS_C)',
                         'dimensionless'),
       AssignmentRule('GPn_Vmax', 'f_glyglc * GP_Vmax * GP_fmax * '
                                     '(GPn_base_amp + (GPn_max_amp - GPn_base_amp) *amp/(amp+GPn_ka_amp))',
                         'mmole_per_min'),
       AssignmentRule('GPn', 'GPn_Vmax/(GPn_k_glyglc*GPn_k_phos) * (glyglc*phos - glc1p/GP_keq) / '
                                '( (1 dimensionless + glyglc/GPn_k_glyglc)*(1 dimensionless + phos/GPn_k_phos) + '
                                '(1 dimensionless + glc1p/GPn_k_glc1p) - 1 dimensionless)', 'mmole_per_min'),
       AssignmentRule('GPp_Vmax', 'f_glyglc * GP_Vmax * GP_fmax * exp(-log(2 dimensionless)/GPp_ki_glc * glc)',
                         'mmole_per_min'),
       AssignmentRule('GPp', 'GPp_Vmax/(GPp_k_glyglc*GPp_k_phos) * (glyglc*phos - glc1p/GP_keq) / '
                                '( (1 dimensionless + glyglc/GPp_k_glyglc)*(1 dimensionless + phos/GPp_k_phos) + '
                                '(1 dimensionless + glc1p/GPp_k_glc1p) - 1 dimensionless)', 'mmole_per_min'),
    ],
    formula=('(1 dimensionless - gamma) * GPn + gamma*GPp', 'mmole_per_min')
)

NDKGTP = Reaction(
    sid='NDKGTP',
    name='Nucleoside-diphosphate kinase (ATP, GTP)',
    equation='Aatp + Agdp <-> Aadp + Agtp []',
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
    formula=('f_gly * NDKGTP_Vmax/(NDKGTP_k_atp*NDKGTP_k_gdp) * (atp*gdp - adp*gtp/NDKGTP_keq) / '
             '( (1 dimensionless + atp/NDKGTP_k_atp)*(1 dimensionless + gdp/NDKGTP_k_gdp) + '
             '(1 dimensionless + adp/NDKGTP_k_adp)*(1 dimensionless + gtp/NDKGTP_k_gtp) - 1 dimensionless)',
             'mmole_per_min')
)

NDKUTP = Reaction(
    sid='NDKUTP',
    name='Nucleoside-diphosphate kinase (ATP, UTP)',
    equation='Aatp + Audp <-> Aadp + Autp []',
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
    formula=('f_glyglc * NDKUTP_Vmax / (NDKUTP_k_atp * NDKUTP_k_udp) * (atp*udp - adp*utp/NDKUTP_keq) / '
             '( (1 dimensionless + atp/NDKUTP_k_atp)*(1 dimensionless + udp/NDKUTP_k_udp) + '
             '(1 dimensionless + adp/NDKUTP_k_adp)*(1 dimensionless + utp/NDKUTP_k_utp) - 1 dimensionless)',
             'mmole_per_min')
)

AK = Reaction(
    sid='AK',
    name='ATP:AMP phosphotransferase (Adenylatkinase)',
    equation='Aamp + Aatp <-> 2 Aadp []',
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
    formula=('f_gly * AK_Vmax / (AK_k_atp * AK_k_amp) * (atp*amp - adp*adp/AK_keq) / '
             '( (1 dimensionless +atp/AK_k_atp)*(1 dimensionless +amp/AK_k_amp) + '
             '(1 dimensionless +adp/AK_k_adp)*(1 dimensionless +adp/AK_k_adp) - 1 dimensionless)', 'mmole_per_min')
)

PFK2 = Reaction(
    sid='PFK2',
    name='ATP:D-fructose-6-phosphate 2-phosphotransferase',
    equation='Afru6p + Aatp => Afru26bp + Aadp + Ah []',
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
       AssignmentRule('PFK2n', 'f_gly * PFK2_Vmax * fru6p^PFK2n_n / (fru6p^PFK2n_n + PFK2n_k_fru6p^PFK2n_n) * '
                                  'atp/(atp + PFK2n_k_atp)', 'mmole_per_min'),
       AssignmentRule('PFK2p', 'f_gly * PFK2_Vmax * fru6p^PFK2p_n / (fru6p^PFK2p_n + PFK2p_k_fru6p^PFK2p_n) * '
                                  'atp/(atp + PFK2p_k_atp)', 'mmole_per_min'),
    ],
    formula=('(1 dimensionless - gamma) * PFK2n + gamma*PFK2p', 'mmole_per_min')
)

FBP2 = Reaction(
    sid='FBP2',
    name='D-Fructose-2,6-bisphosphate 2-phosphohydrolase',
    equation='Afru26bp + Ah2o => Afru6p + Aphos []',
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
       AssignmentRule('FBP2n', 'f_gly * FBP2_Vmax/(1 dimensionless + fru6p/FBP2n_ki_fru6p) * fru26bp / '
                                  '( FBP2n_k_fru26bp + fru26bp)', 'mmole_per_min'),
       AssignmentRule('FBP2p', 'f_gly * FBP2_Vmax/(1 dimensionless + fru6p/FBP2p_ki_fru6p) * fru26bp / '
                                  '( FBP2p_k_fru26bp + fru26bp)', 'mmole_per_min'),
    ],
    formula=('(1 dimensionless - gamma) * FBP2n + gamma * FBP2p', 'mmole_per_min')
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
    equation='Afru6p + Aatp => Afru16bp + Aadp + Ah [Afru26bp]',
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
    formula=('f_gly * PFK1_Vmax * (1 dimensionless - 1 dimensionless/(1 dimensionless + fru26bp/PFK1_ka_fru26bp)) * '
             'fru6p*atp/(PFK1_ki_fru6p*PFK1_k_atp + PFK1_k_fru6p*atp + PFK1_k_atp*fru6p + atp*fru6p)', 'mmole_per_min')
)

FBP1 = Reaction(
    sid='FBP1',
    name='D-Fructose-1,6-bisphosphate 1-phosphohydrolase',
    equation='Afru16bp + Ah2o => Afru6p + Aphos [Afru26bp]',
    # C6H10O12P2 (-4) + H2O (0) => C6H11O9P (-2) + HO4P (-2)
    compartment='cyto',
    sboTerm=SBO_BIOCHEMICAL_REACTION,
    pars=[
       Parameter('FBP1_ki_fru26bp', 0.001, 'mM'),
       Parameter('FBP1_k_fru16bp', 0.0013, 'mM'),
       Parameter('FBP1_Vmax', 4.326, 'mmole_per_min'),
    ],
    formula=('f_gly * FBP1_Vmax / (1 dimensionless + fru26bp/FBP1_ki_fru26bp) * fru16bp/(fru16bp + FBP1_k_fru16bp)',
             'mmole_per_min')
)

ALD = Reaction(
    sid='ALD',
    name='Aldolase',
    equation='Afru16bp <-> Agrap + Adhap []',
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
    equation='Adhap <-> Agrap []',
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
             '(1 dimensionless + dhap/TPI_k_dhap + grap/TPI_k_grap)', 'mmole_per_min')
)

GAPDH = Reaction(
    sid='GAPDH',
    name='D-Glyceraldehyde-3-phosphate:NAD+ oxidoreductase',
    equation='Agrap + Anad + Aphos <-> Abpg13 + Anadh + Ah []',
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
    formula=('f_gly * GAPDH_Vmax / (GAPDH_k_nad*GAPDH_k_grap*GAPDH_k_phos) * (nad*grap*phos - bpg13*nadh/GAPDH_keq) / '
             '( (1 dimensionless + nad/GAPDH_k_nad) * (1 dimensionless +grap/GAPDH_k_grap) * '
             '(1 dimensionless + phos/GAPDH_k_phos) + '
             '(1 dimensionless +nadh/GAPDH_k_nadh)*(1 dimensionless +bpg13/GAPDH_k_bpg13) - 1 dimensionless)',
             'mmole_per_min')
)

PGK = Reaction(
    sid='PGK',
    name='Phosphoglycerate Kinase',
    equation='Aadp + Abpg13 <-> Aatp + Apg3 []',
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
    formula=('f_gly * PGK_Vmax / (PGK_k_adp*PGK_k_bpg13) * (adp*bpg13 - atp*pg3/PGK_keq) / '
             '((1 dimensionless + adp/PGK_k_adp)*(1 dimensionless +bpg13/PGK_k_bpg13) + '
             '(1 dimensionless +atp/PGK_k_atp)*(1 dimensionless +pg3/PGK_k_pg3) - 1 dimensionless)', 'mmole_per_min')
)

PGM = Reaction(
    sid='PGM',
    name='2-Phospho-D-glycerate 2,3-phosphomutase',
    equation='Apg3 <-> Apg2 []',
    # C3H4O7P (-3) <-> C3H4O7P (-3)
    compartment='cyto',
    sboTerm=SBO_BIOCHEMICAL_REACTION,
    pars=[
       Parameter('PGM_keq', 0.181375378837397, 'dimensionless'),
       Parameter('PGM_k_pg3', 5, 'mM'),
       Parameter('PGM_k_pg2', 1, 'mM'),
       Parameter('PGM_Vmax', 420, 'mmole_per_min'),
    ],
    formula=('f_gly * PGM_Vmax * (pg3 - pg2/PGM_keq) / (pg3 + PGM_k_pg3 *(1 dimensionless + pg2/PGM_k_pg2))',
             'mmole_per_min')
)

EN = Reaction(
    sid='EN',
    name='2-Phospho-D-glucerate hydro-lyase (enolase)',
    equation='Apg2 <-> Ah2o + Apep []',
    # C3H4O7P (-3) <-> H2O (0) + C3H2O6P (-3)
    compartment='cyto',
    sboTerm=SBO_BIOCHEMICAL_REACTION,
    pars=[
       Parameter('EN_keq', 0.054476985386756, 'dimensionless'),
       Parameter('EN_k_pep', 1, 'mM'),
       Parameter('EN_k_pg2', 1, 'mM'),
       Parameter('EN_Vmax', 35.994, 'mmole_per_min'),
    ],
    formula=('f_gly * EN_Vmax * (pg2 - pep/EN_keq) / (pg2 + EN_k_pg2 *(1 dimensionless + pep/EN_k_pep))', 'mmole_per_min')
)

PK = Reaction(
    sid='PK',
    name='Pyruvatkinase',
    equation='Apep + Aadp + Ah => Apyr + Aatp [Afru16bp]',
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
       AssignmentRule('PKn_f', 'fru16bp^PKn_n_fbp / (PKn_k_fbp^PKn_n_fbp + fru16bp^PKn_n_fbp)', 'dimensionless'),
       AssignmentRule('PKp_f', 'fru16bp^PKp_n_fbp / (PKp_k_fbp^PKp_n_fbp + fru16bp^PKp_n_fbp)', 'dimensionless'),
       AssignmentRule('PKn_alpha_inp', '(1 dimensionless - PKn_f) * (PKn_alpha - PK_ae) + PK_ae', 'dimensionless'),
       AssignmentRule('PKp_alpha_inp', '(1 dimensionless - PKp_f) * (PKp_alpha - PK_ae) + PK_ae', 'dimensionless'),
       AssignmentRule('PKn_pep_inp', '(1 dimensionless - PKn_f) *(PKn_k_pep - PKn_k_pep_end) + PKn_k_pep_end', 'mM'),
       AssignmentRule('PKp_pep_inp', '(1 dimensionless - PKp_f) *(PKp_k_pep - PKn_k_pep_end) + PKn_k_pep_end', 'mM'),
       AssignmentRule('PKn', 'f_gly * PK_Vmax * PKn_alpha_inp * pep^PKn_n/(PKn_pep_inp^PKn_n + pep^PKn_n) * '
                                'adp/(adp + PK_k_adp) * ( PKn_ba + (1 dimensionless - PKn_ba) * PKn_f )', 'mmole_per_min'),
       AssignmentRule('PKp', 'f_gly * PK_Vmax * PKp_alpha_inp * pep^PKp_n/(PKp_pep_inp^PKp_n + pep^PKp_n) * '
                                'adp/(adp + PK_k_adp) * ( PKp_ba + (1 dimensionless - PKp_ba) * PKp_f )', 'mmole_per_min'),
    ],
    formula=('(1 dimensionless - gamma)* PKn + gamma * PKp', 'mmole_per_min')
)

PEPCK = Reaction(
    sid='PEPCK',
    name='PEPCK cyto',
    equation='Agtp + Aoaa <-> Aco2 + Agdp + Apep []',
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
    formula=('f_gly * PEPCK_Vmax / (PEPCK_k_oaa * PEPCK_k_gtp) * (oaa*gtp - pep*gdp*co2/PEPCK_keq) / '
             '( (1 dimensionless + oaa/PEPCK_k_oaa)*(1 dimensionless +gtp/PEPCK_k_gtp) + '
             '(1 dimensionless + pep/PEPCK_k_pep)*(1 dimensionless + gdp/PEPCK_k_gdp)*'
             '(1 dimensionless +co2/PEPCK_k_co2) - 1 dimensionless)', 'mmole_per_min')
)

PEPCKM = Reaction(
    sid='PEPCKM',
    name='PEPCK mito',
    equation='Agtp_mito + Aoaa_mito <-> Aco2_mito + Agdp_mito + Apep_mito []',
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
             '(1 dimensionless +co2_mito/PEPCK_k_co2) - 1 dimensionless)', 'mmole_per_min')
)

PC = Reaction(
    sid='PC',
    name='Pyruvate Carboxylase',
    equation='Aatp_mito + Apyr_mito + Aco2_mito + Ah2o_mito => Aadp_mito + Aoaa_mito + Aphos_mito + 2 Ah [Aacoa_mito]',
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
    formula=('f_gly * PC_Vmax * atp_mito/(PC_k_atp + atp_mito) * pyr_mito/(PC_k_pyr + pyr_mito) * '
             'co2_mito/(PC_k_co2 + co2_mito) * acoa_mito^PC_n / (acoa_mito^PC_n + PC_k_acoa^PC_n)', 'mmole_per_min')
)

LDH = Reaction(
    sid='LDH',
    name='Lactate Dehydrogenase',
    equation='Apyr + Anadh + Ah <-> Alac + Anad []',
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
    formula=('f_gly * LDH_Vmax / (LDH_k_pyr * LDH_k_nadh) * (pyr*nadh - lac*nad/LDH_keq) / '
             '( (1 dimensionless +nadh/LDH_k_nadh)*(1 dimensionless +pyr/LDH_k_pyr) + '
             '(1 dimensionless +lac/LDH_k_lac) * (1 dimensionless +nad/LDH_k_nad) - 1 dimensionless)', 'mmole_per_min')
)

LACT = Reaction(
    sid='LACT',
    name='Lactate transport (import)',
    equation='Alac_ext <-> Alac []',
    # C3H5O3 (-1) <-> C3H5O3 (-1)
    compartment='pm',
    sboTerm=SBO_TRANSPORT_REACTION,
    pars=[
       Parameter('LACT_keq', 1, 'dimensionless'),
       Parameter('LACT_k_lac', 0.8, 'mM'),
       Parameter('LACT_Vmax', 5.418, 'mmole_per_min'),
    ],
    formula=('f_gly * LACT_Vmax/LACT_k_lac * (lac_ext - lac/LACT_keq) / '
             '(1 dimensionless + lac_ext/LACT_k_lac + lac/LACT_k_lac)', 'mmole_per_min')
)

PYRTM = Reaction(
    sid='PYRTM',
    name='Pyruvate transport (mito)',
    equation='Apyr <-> Apyr_mito []',
    # C3H3O3 (-1) <-> C3H3O3 (-1)
    compartment='mm',
    sboTerm=SBO_TRANSPORT_REACTION,
    pars=[
       Parameter('PYRTM_keq', 1, 'dimensionless'),
       Parameter('PYRTM_k_pyr', 0.1, 'mM'),
       Parameter('PYRTM_Vmax', 42, 'mmole_per_min'),
    ],
    formula=('f_gly * PYRTM_Vmax/PYRTM_k_pyr * (pyr - pyr_mito/PYRTM_keq) / '
             '(1 dimensionless + pyr/PYRTM_k_pyr + pyr_mito/PYRTM_k_pyr)', 'mmole_per_min')
)

PEPTM = Reaction(
    sid='PEPTM',
    name='PEP Transport (export mito)',
    equation='Apep_mito <-> Apep []',
    # C3H2O6P (-3) <-> C3H2O6P (-3)
    compartment='mm',
    sboTerm=SBO_TRANSPORT_REACTION,
    pars=[
       Parameter('PEPTM_keq', 1, 'dimensionless'),
       Parameter('PEPTM_k_pep', 0.1, 'mM'),
       Parameter('PEPTM_Vmax', 33.6, 'mmole_per_min'),
    ],
    formula=('f_gly * PEPTM_Vmax/PEPTM_k_pep * (pep_mito - pep/PEPTM_keq) / '
             '(1 dimensionless + pep/PEPTM_k_pep + pep_mito/PEPTM_k_pep)', 'mmole_per_min')
)

PDH = Reaction(
    sid='PDH',
    name='Pyruvate Dehydrogenase',
    equation='Apyr_mito + Acoa_mito + Anad_mito => Aacoa_mito + Aco2_mito + Anadh_mito []',
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
       AssignmentRule('PDH_base', 'f_gly * PDH_Vmax * pyr_mito/(pyr_mito + PDH_k_pyr) * '
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
    equation='Aacoa_mito + Aoaa_mito + Ah2o_mito <-> Acit_mito + Acoa_mito + Ah_mito []',
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
    formula=('f_gly * CS_Vmax/(CS_k_oaa * CS_k_acoa) * (acoa_mito*oaa_mito - cit_mito*coa_mito/CS_keq) / '
             '( (1 dimensionless +acoa_mito/CS_k_acoa)*(1 dimensionless +oaa_mito/CS_k_oaa) + '
             '(1 dimensionless +cit_mito/CS_k_cit)*(1 dimensionless +coa_mito/CS_k_coa) -1 dimensionless)',
             'mmole_per_min')
)

NDKGTPM = Reaction(
    sid='NDKGTPM',
    name='Nucleoside-diphosphate kinase (ATP, GTP) mito',
    equation='Aatp_mito + Agdp_mito <-> Aadp_mito + Agtp_mito []',
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
    equation='=> Aoaa_mito []',
    # ->
    compartment='mito',
    pars=[
       Parameter('OAAFLX_Vmax', 0, 'mmole_per_min'),
    ],
    formula=('f_gly * OAAFLX_Vmax', 'mmole_per_min')
)

ACOAFLX = Reaction(
    sid='ACOAFLX',
    name='acetyl-coa efflux',
    equation='Aacoa_mito => []',
    compartment='mito',
    pars=[
       Parameter('ACOAFLX_Vmax', 0, 'mmole_per_min'),
    ],
    formula=('f_gly * ACOAFLX_Vmax', 'mmole_per_min')
)

CITFLX = Reaction(
    sid='CITFLX',
    name='citrate efflux',
    equation='Acit_mito => []',
    compartment='mito',
    pars=[
       Parameter('CITFLX_Vmax', 0, 'mmole_per_min'),
    ],
    formula=('f_gly * CITFLX_Vmax', 'mmole_per_min')
)
