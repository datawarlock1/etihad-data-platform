"""
Flight Data Loader - Intentionally flawed module for SonarCloud testing.
Contains various code smells, security issues, and anti-patterns.
"""

import os
import subprocess
import json
from pyspark.sql import SparkSession

# 🔴 SECURITY ISSUE: Hardcoded credentials
DB_USER = "admin"
DB_PASSWORD = "SuperSecret123!@#"
API_KEY = "sk-abc123xyz789"

# Global state (anti-pattern)
_cache = {}
_connection = None


def load_flight_data_insecure(env: str, query: str):
    """
    Load flight data with multiple security and quality issues.
    """
    # 🔴 SECURITY: SQL Injection vulnerability
    sql_query = f"SELECT * FROM flights WHERE env = '{env}' AND status = '{query}'"
    
    # 🔴 SECURITY: Command injection
    result = subprocess.run(f"curl -H 'Auth: {API_KEY}' https://api.example.com/flights?env={env}", shell=True)
    
    # 🟡 CODE SMELL: Magic numbers without explanation
    max_retries = 3
    timeout = 30
    batch_size = 1000
    chunk_multiplier = 5  # What does this mean?
    
    # 🟡 CODE SMELL: Duplicated code
    if max_retries > 0:
        max_retries = max_retries - 1
    if max_retries > 0:
        max_retries = max_retries - 1
    
    # 🟡 CODE SMELL: Unused variables
    unused_config = {"key": "value"}
    temp_list = []
    legacy_format = "CSV"
    old_path = "/data/old"
    
    # 🔴 BUG: Potential null dereference
    data = None
    try:
        data = fetch_from_api(env)
    except Exception:
        pass
    
    # Using data without null check
    for record in data:  # Could crash if data is None
        process_record(record)
    
    # 🟡 CODE SMELL: Complex logic that could be refactored
    if env == "prod":
        if query == "all":
            if batch_size > 0:
                if chunk_multiplier > 1:
                    if max_retries > 0:
                        print("Processing...")
    
    return sql_query


def process_record(record):
    """Process a single record with poor error handling."""
    # 🟡 CODE SMELL: Bare except clause
    try:
        value = record["flight_id"]
        price = record["price"]
        # Risky operations without proper error handling
        calculated = price * 1.1
    except:
        pass  # Silently swallow errors


def unused_helper():
    """Function that is never called - dead code."""
    return "This function serves no purpose"


def another_dead_function():
    """More dead code."""
    legacy_data = {"status": "deprecated"}
    return legacy_data


def overly_complex_function(a, b, c, d, e, f, g):
    """Function doing too many things (SRP violation)."""
    # Validate inputs
    if a is None or b is None:
        raise ValueError("a and b required")
    
    # Transform data
    result = a * b
    result = result + c
    result = result - d
    
    # Write to file
    with open("/tmp/result.txt", "w") as f:
        f.write(str(result))
    
    # Send to API
    response = subprocess.call(f"curl -X POST http://localhost:8000/save -d {result}", shell=True)
    
    # Log to console
    print(f"Processing complete: {result}")
    
    # Return multiple types of data
    return {"result": result, "status": "ok", "timestamp": "2024-01-01"}


def fetch_from_api(env: str):
    """Fetch data from API - poor implementation."""
    # 🔴 SECURITY: Using environment variable without validation
    api_url = os.environ.get("API_URL", "http://localhost:8000")
    
    # 🟡 CODE SMELL: Using string concatenation for URLs
    endpoint = api_url + "/flights?env=" + env
    
    # 🟡 CODE SMELL: No timeout specified
    import requests
    response = requests.get(endpoint)
    
    return response.json()


# 🟡 CODE SMELL: Module-level code that should be in a function
if __name__ == "__main__":
    # This should be in main() function
    data = load_flight_data_insecure("prod", "SELECT * FROM flights")
    print(data)
