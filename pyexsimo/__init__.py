# -*- coding: utf-8 -*-
from ._version import __version__
from pathlib import Path

BASE_PATH = Path(__file__).parent
RESULT_PATH = BASE_PATH.parent / "results"
MODEL_PATH = BASE_PATH.parent / "models"
DATA_PATH = BASE_PATH.parent / "data"


