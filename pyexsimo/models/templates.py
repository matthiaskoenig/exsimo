"""
Template information for all tissue models.
"""
from datetime import datetime
from sbmlutils.units import *
from sbmlutils.factory import *

MODEL_UNITS = ModelUnits(time='min',
                         extent='mmole',
                         substance='mmole',
                         length='m',
                         area='m2',
                         volume='l')

UNITS = [
    Unit('l', [(UNIT_KIND_LITRE, 1.0)], metaId='meta_l', port=True),
    Unit('min', [(UNIT_KIND_SECOND, 1.0, 0, 60)], metaId='meta_min', port=True),
    Unit('s', [(UNIT_KIND_SECOND, 1.0, 0, 1)], metaId='meta_s', port=True),
    Unit('kg', [(UNIT_KIND_GRAM, 1.0, 3, 1.0)], metaId='meta_kg', port=True),
    Unit('m', [(UNIT_KIND_METRE, 1.0)], metaId='meta_m', port=True),
    Unit('m2', [(UNIT_KIND_METRE, 2.0)], metaId='meta_m2', port=True),
    Unit('mg', [(UNIT_KIND_GRAM, 1.0, -3, 1.0)], metaId='meta_mg', port=True),
    Unit('ml', [(UNIT_KIND_LITRE, 1.0, -3, 1.0)], metaId='meta_ml', port=True),
    Unit('mmole', [(UNIT_KIND_MOLE, 1.0, -3, 1)], metaId='meta_mmole', port=True),
    Unit('per_min', [(UNIT_KIND_SECOND, -1.0, 0, 60)], metaId='meta_per_min', port=True),
    Unit('mM', [(UNIT_KIND_MOLE, 1.0, -3, 1),
                   (UNIT_KIND_LITRE, -1.0, 0, 1)], metaId='meta_mM', port=True),
    Unit('mmole_per_min', [(UNIT_KIND_MOLE, 1.0, -3, 1),
                              (UNIT_KIND_SECOND, -1.0, 0, 60)], metaId='meta_mmole_per_min', port=True),
    Unit('mmole_per_min_l', [(UNIT_KIND_MOLE, 1.0, -3, 1),
                               (UNIT_KIND_SECOND, -1.0, 0, 60), (UNIT_KIND_LITRE, -1.0, 0, 1.0)], metaId='meta_mmole_per_minl', port=True),
]

CREATORS = [
    Creator(familyName='Koenig',
            givenName='Matthias',
            email='koenigmx@hu-berlin.de',
            organization='Humboldt-University Berlin, Institute for Theoretical Biology',
            site="https://livermetabolism.com"),
]

def notes(tissue):
    return Notes([
    """
    <h1>{} glucose model</h1>
    <h2>Description</h2>
    <p>
        {} tissue glucose metabolism  
        encoded in <a href="http://sbml.org">SBML</a> format.<br /> 
    </p>
    """.format(tissue, tissue) + TERMS_OF_USE + """
    """
])

TERMS_OF_USE = """
    <div class="dc:provenance">The content of this model has been carefully created in a manual research effort.</div>
    <div class="dc:publisher">This file has been created by
    <a href="{site}" title="{given_name} {family_name}" target="_blank">{given_name} {family_name}</a>.</div>

    <h2>Terms of use</h2>
    <div class="dc:rightsHolder">Copyright © {year} {given_name} {family_name}.</div>
    <div class="dc:license">
        <p>Redistribution and use of any part of this model, with or without modification, are permitted provided
        that the following conditions are met:
        <ol>
          <li>Redistributions of this SBML file must retain the above copyright notice, this list of conditions and
          the following disclaimer.</li>
          <li>Redistributions in a different form must reproduce the above copyright notice, this list of conditions
          and the following disclaimer in the documentation and/or other materials provided
          with the distribution.</li>
        </ol>
        This model is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
        implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
        </p>
    </div>
""".format(year=datetime.now().year, given_name=CREATORS[0].givenName,
           family_name=CREATORS[0].familyName, site=CREATORS[0].site)