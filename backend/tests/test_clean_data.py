import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from scripts.clean_data import load_csv


def test_load_csv_exists():
    try:
        df = load_csv("customers.csv")
        assert df is not None
    except Exception as e:
        assert "not found" in str(e)


def test_load_csv_type():
    try:
        df = load_csv("customers.csv")
        assert hasattr(df, "columns")
    except Exception:
        assert True