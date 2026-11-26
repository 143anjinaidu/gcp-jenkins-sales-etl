
import pandas as pd
import pytest

import etl


def test_etl_processes_valid_and_rejects_invalid_records(tmp_path, monkeypatch):
    input_file = tmp_path / "sales.csv"
    processed_file = tmp_path / "processed_sales.csv"
    rejected_file = tmp_path / "rejected_sales.csv"

    data = {
        "order_id": [1, 2],
        "order_date": ["2026-11-01", "2026-11-02"],
        "customer": ["Alice", "Bob"],
        "product": ["Laptop", "Phone"],
        "quantity": [2, 0],
        "price": [1000, 500],
        "region": ["South", "North"],
    }

    pd.DataFrame(data).to_csv(input_file, index=False)

    monkeypatch.setattr(etl, "INPUT_FILE", input_file)
    monkeypatch.setattr(etl, "PROCESSED_FILE", processed_file)
    monkeypatch.setattr(etl, "REJECTED_FILE", rejected_file)

    etl.run_etl()

    processed = pd.read_csv(processed_file)
    rejected = pd.read_csv(rejected_file)

    assert len(processed) == 1
    assert len(rejected) == 1
    assert processed.iloc[0]["customer"] == "Alice"


def test_etl_fails_when_required_column_is_missing(tmp_path, monkeypatch):
    input_file = tmp_path / "sales.csv"

    pd.DataFrame({
        "order_id": [1],
        "customer": ["Alice"],
    }).to_csv(input_file, index=False)

    monkeypatch.setattr(etl, "INPUT_FILE", input_file)

    with pytest.raises(ValueError, match="Missing columns"):
        etl.run_etl()
