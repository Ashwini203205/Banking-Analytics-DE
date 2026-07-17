from pyspark.sql import SparkSession
from pyspark.sql.functions import col

from config import *
from db_connection import connection_properties
from logger import logger

# Create Spark Session
spark = (
    SparkSession.builder
    .master("local[*]")
    .appName("Data Quality Check")
    .config("spark.jars", JAR_PATH)
    .getOrCreate()
)

logger.info("Reading Silver Table...")

silver_df = (
    spark.read.jdbc(
        url=JDBC_URL,
        table="silver.customer_clean",
        properties=connection_properties
    )
)

# -----------------------------
# Duplicate Check
# -----------------------------
duplicates = silver_df.count() - silver_df.dropDuplicates().count()

# -----------------------------
# Null Check
# -----------------------------
null_age = silver_df.filter(col("age").isNull()).count()
null_job = silver_df.filter(col("job").isNull()).count()

# -----------------------------
# Negative Balance Check
# -----------------------------
negative_balance = silver_df.filter(col("balance") < 0).count()

# -----------------------------
# Invalid Age Check
# -----------------------------
invalid_age = silver_df.filter(col("age") < 18).count()

print("=" * 50)
print("DATA QUALITY REPORT")
print("=" * 50)

print(f"Duplicate Records : {duplicates}")
print(f"Null Age          : {null_age}")
print(f"Null Job          : {null_job}")
print(f"Negative Balance  : {negative_balance}")
print(f"Invalid Age (<18) : {invalid_age}")

print("=" * 50)

spark.stop()