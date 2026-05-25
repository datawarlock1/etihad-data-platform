import json
import os
from unittest.mock import patch

import pytest

import src.ingestion.flight_data_loader as loader


def test_get_api_url_defaults_to_localhost(monkeypatch):
    monkeypatch.delenv("API_URL", raising=False)
    assert loader.get_api_url() == "http://localhost:8000"


def test_build_flight_endpoint_returns_url(monkeypatch):
    monkeypatch.setenv("API_URL", "http://example.com")
    assert loader.build_flight_endpoint() == "http://example.com/flights"


@patch("src.ingestion.flight_data_loader.requests.get")
def test_load_flight_data_calls_requests(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [{"flight_id": "FL001", "price": 100}]

    result = loader.load_flight_data("prod", "ACTIVE")

    mock_get.assert_called_once()
    assert result == [{"flight_id": "FL001", "price": 100}]


def test_process_record_valid_data():
    record = {"flight_id": "FL001", "price": 100}
    result = loader.process_record(record)
    assert result["flight_id"] == "FL001"
    assert result["price_with_tax"] == 110.0


def test_process_record_invalid_data():
    record = {"flight_id": "FL002", "price": "invalid"}
    result = loader.process_record(record)
    assert result is None


@patch("src.ingestion.flight_data_loader.requests.get")
def test_ingest_flight_data_filters_invalid_records(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [
        {"flight_id": "FL001", "price": 100},
        {"flight_id": "FL002", "price": "invalid"},
    ]

    result = loader.ingest_flight_data("prod", "ACTIVE")

    assert len(result) == 1
    assert result[0]["flight_id"] == "FL001"


def test_save_results_writes_json(tmp_path):
    output_file = tmp_path / "results.json"
    results = [{"flight_id": "FL001", "price_with_tax": 110.0}]

    loader.save_results(results, str(output_file))

    with open(output_file, "r", encoding="utf-8") as source:
        saved = json.load(source)

    assert saved == results
