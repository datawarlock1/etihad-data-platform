import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pyspark.sql import SparkSession
from src.transformations.flight_transforms import filter_active, recent_days, add_ingested_at


def test_transforms_pipeline():
    spark = SparkSession.builder.master("local[1]").appName("test").getOrCreate()
    data = [("FL001","ACTIVE","AUH","DXB",1), ("FL002","CANCELLED","AUH","DXB",5)]
    cols = ["flight_id","flight_status","origin","destination","days_since"]
    df = spark.createDataFrame(data, cols)

    df1 = filter_active(df)
    assert df1.count() == 1

    df2 = recent_days(df1, days=3)
    assert df2.count() == 1

    df3 = add_ingested_at(df2)
    assert "ingested_at" in [f.name for f in df3.schema.fields]
