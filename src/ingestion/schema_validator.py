from pyspark.sql import DataFrame
from pyspark.sql.types import StructType, StructField, StringType, LongType

EXPECTED_SCHEMA = StructType([
    StructField("flight_id",     StringType(), False),
    StructField("flight_status", StringType(), True),
    StructField("origin",        StringType(), True),
    StructField("destination",   StringType(), True),
    StructField("days_since",    LongType(),   True),
])

def validate_schema(df: DataFrame) -> bool:
    """
    Validates that the incoming DataFrame matches expected schema.
    Returns True if valid, raises ValueError otherwise.
    """
    actual_fields   = {f.name for f in df.schema.fields}
    expected_fields = {f.name for f in EXPECTED_SCHEMA.fields}

    missing = expected_fields - actual_fields
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    return True


def get_row_count(df: DataFrame) -> int:
    """Returns the row count of a DataFrame."""
    return df.count()
