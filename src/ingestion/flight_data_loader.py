"""
Flight Data Loader.

This module provides a secure and maintainable way to fetch flight data and
process records. It avoids hardcoded secrets, side effects, and anti-patterns.
"""

import json
import logging
import os
from typing import Any, Dict, List, Optional

import requests

logger = logging.getLogger(__name__)


def get_api_url() -> str:
    api_url = os.environ.get("API_URL", "http://localhost:8000")
    return api_url.rstrip("/")


def build_flight_endpoint() -> str:
    return f"{get_api_url()}/flights"


def load_flight_data(env: str, status: str) -> List[Dict[str, Any]]:
    endpoint = build_flight_endpoint()
    response = requests.get(endpoint, params={"env": env, "status": status}, timeout=10)
    response.raise_for_status()
    return response.json()


def process_record(record: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    try:
        flight_id = record["flight_id"]
        price = float(record["price"])
        return {
            "flight_id": flight_id,
            "price_with_tax": price * 1.1,
        }
    except (KeyError, TypeError, ValueError) as exc:
        logger.warning("Skipping invalid record: %s", exc)
        return None


def ingest_flight_data(env: str, status: str) -> List[Dict[str, Any]]:
    records = load_flight_data(env, status)
    processed_records = [result for record in records if (result := process_record(record)) is not None]
    return processed_records


def save_results(results: List[Dict[str, Any]], path: str) -> None:
    if not path:
        raise ValueError("Output path is required")
    with open(path, "w", encoding="utf-8") as writer:
        json.dump(results, writer, indent=2)


if __name__ == "__main__":
    example_results = ingest_flight_data("prod", "ACTIVE")
    output_path = os.path.join(os.getcwd(), "flight_results.json")
    save_results(example_results, output_path)
