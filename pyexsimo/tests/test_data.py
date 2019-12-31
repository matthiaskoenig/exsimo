"""
Test data files.
"""
import pytest
import pandas as pd
from pyexsimo import DATA_PATH

data_paths = [
    DATA_PATH / "DoseResponse" / ".DoseResponse_TabEpinephrine.tsv",
    DATA_PATH / "DoseResponse" / ".DoseResponse_TabGlucagon.tsv",
    DATA_PATH / "DoseResponse" / ".DoseResponse_TabInsulin.tsv",
    DATA_PATH / "Glycogen" / ".Glycogen_TabMagnusson1992.tsv",
    DATA_PATH / "Glycogen" / ".Glycogen_TabRadziuk2001.tsv",
    DATA_PATH / "Glycogen" / ".Glycogen_TabRothman1991.tsv",
    DATA_PATH / "Glycogen" / ".Glycogen_TabTaylor1996.tsv",
    DATA_PATH / "Nuttal2008" / ".Nuttal2008_TabA.tsv",
]


@pytest.mark.parametrize("data_path", data_paths)
def test_datafile_exists(data_path):
    assert data_path.exists()


@pytest.mark.parametrize("data_path", data_paths)
def test_datafile_parsable(data_path):
    df = pd.read_csv(data_path, skiprows=1, sep="\t")
    assert not df.empty
