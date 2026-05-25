import pytest
from unittest.mock import MagicMock, patch
from pyspark.sql import SparkSession
from src.ingestion.schema_validator import validate_schema, get_row_count

@pytest.fixture(scope="session")
def spark():
    return SparkSession.builder \
        .master("local[1]") \
        .appName("test") \
        .getOrCreate()


def test_validate_schema_passes(spark):
    """Schema validation passes when all expected columns present."""
    data = [("FL001", "ACTIVE", "AUH", "DXB", 1)]
    cols = ["flight_id","flight_status","origin","destination","days_since"]
    df   = spark.createDataFrame(data, cols)
    assert validate_schema(df) is True


def test_validate_schema_missing_col(spark):
    """Schema validation raises when a column is missing."""
    data = [("FL001", "ACTIVE")]
    cols = ["flight_id", "flight_status"]
    df   = spark.createDataFrame(data, cols)
    with pytest.raises(ValueError, match="Missing columns"):
        validate_schema(df)


def test_get_row_count(spark):
    """Row count returns correct integer."""
    data = [("a",), ("b",), ("c",)]
    df   = spark.createDataFrame(data, ["val"])
    assert get_row_count(df) == 3

# NOTE: flight_ingestor.py is NOT tested → coverage will be low → Sonar flags it
