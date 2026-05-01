from pathlib import Path

def test_raw_data_exists():
    base = Path(__file__).resolve().parent.parent
    raw_dir = base / "data" / "raw"

    files = ["customers.csv", "orders.csv", "products.csv"]

    for f in files:
        assert (raw_dir / f).exists(), f"{f} not generated"