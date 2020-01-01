# -*- coding: utf-8 -*-
from ._version import __version__
from pathlib import Path

BASE_PATH = Path(__file__).parent
RESULT_PATH = BASE_PATH.parent / "docs"  # for github pages
MODEL_PATH = BASE_PATH.parent / "docs" / "models"
DATA_PATH = BASE_PATH.parent / "data"
TEMPLATE_PATH = BASE_PATH / "templates"



