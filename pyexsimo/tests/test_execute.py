"""
Test executing the complete workflow.
"""
import pytest
from pyexsimo.execute import execute


def test_execute(tmp_path):
    """ Execute complete workflow.

    Writes results in tmp_path.
    """
    execute(output_path=tmp_path, model_output_path=tmp_path)
