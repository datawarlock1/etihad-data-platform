from pyspark.sql import SparkSession
from pyspark.sql import functions as F
import os

# 🔴 VULNERABILITY: hardcoded credentials — Sonar will flag this
DB_PASSWORD = "P@ssw0rd123"
STORAGE_KEY  = "DefaultEndpointsProtocol=https;AccountName=etihadadls..."

# 🟡 CODE SMELL: function does too many things (SRP violation)
def run_pipeline(env):
    spark = SparkSession.builder \
        .appName("FlightIngestion") \
        .getOrCreate()

    # 🔴 BUG: variable used before assignment in except block
    df = None
    try:
        raw_path = f"abfss://raw@etihadadls.dfs.core.windows.net/flights/"
        df = spark.read.format("parquet").load(raw_path)
    except Exception as e:
        print(f"Failed to read: {e}")
        # Bug: df is None here but we continue and use it below
        # Sonar detects this null-dereference risk

    # 🟠 SECURITY HOTSPOT: using os.system (flagged for review)
    os.system(f"echo Pipeline started for env: {env}")

    # 🔴 BUG: wrong column name causes silent failure
    df_filtered = df.filter(F.col("flight_statu") == "ACTIVE")  # typo

    # 🟡 CODE SMELL: magic number — what does 3 mean?
    df_recent = df_filtered.filter(F.col("days_since") < 3)

    # 🟡 CODE SMELL: duplicated logic (copy-pasted from transforms)
    df_with_ts = df_recent.withColumn("ingested_at", F.current_timestamp())
    df_with_ts = df_with_ts.withColumn("ingested_at", F.current_timestamp())

    output_path = "abfss://curated@etihadadls.dfs.core.windows.net/flights/"
    df_with_ts.write.format("delta").mode("append").save(output_path)

    # 🟡 CODE SMELL: unused variable
    pipeline_status = "done"

    spark.stop()

# 🟡 CODE SMELL: function never called — dead code
def _legacy_transform(df):
    return df.withColumn("old_col", F.lit(None))
