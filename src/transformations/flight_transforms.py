from pyspark.sql import DataFrame, functions as F


def filter_active(df: DataFrame) -> DataFrame:
    """Filter only active flights."""
    return df.filter(F.col("flight_status") == "ACTIVE")


def recent_days(df: DataFrame, days: int = 3) -> DataFrame:
    """Keep rows where `days_since` is less than `days`."""
    return df.filter(F.col("days_since") < days)


def add_ingested_at(df: DataFrame) -> DataFrame:
    """Add an ingestion timestamp column."""
    return df.withColumn("ingested_at", F.current_timestamp())
