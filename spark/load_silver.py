from pyspark.sql import SparkSession
from pyspark.sql.functions import trim, lower, col

from config import *
from db_connection import connection_properties
from logger import logger

# Create Spark Session
spark = (
    SparkSession.builder
    .master("local[*]")
    .appName("Silver Layer")
    .config("spark.jars", JAR_PATH)
    .getOrCreate()
)

logger.info("Reading Bronze Table...")

bronze_df = (
    spark.read.jdbc(
        url=JDBC_URL,
        table="bronze.customer_raw",
        properties=connection_properties
    )
)

logger.info(f"Bronze Records: {bronze_df.count()}")

# Remove duplicates
silver_df = bronze_df.dropDuplicates()

# Fill NULL values
silver_df = silver_df.fillna({
    "job": "unknown",
    "education": "unknown",
    "contact": "unknown",
    "poutcome": "unknown"
})

# Trim string columns
for c in silver_df.columns:
    if silver_df.schema[c].dataType.simpleString() == "string":
        silver_df = silver_df.withColumn(c, trim(col(c)))

# Convert text to lowercase
text_cols = [
    "job",
    "marital",
    "education",
    "default_status",
    "housing",
    "loan",
    "contact",
    "month",
    "poutcome",
    "y"
]

for c in text_cols:
    silver_df = silver_df.withColumn(c, lower(col(c)))

logger.info(f"Silver Records: {silver_df.count()}")

logger.info("Writing Silver Table...")

(
    silver_df.write
    .mode("overwrite")
    .jdbc(
        url=JDBC_URL,
        table="silver.customer_clean",
        properties=connection_properties
    )
)

logger.info("Silver Layer Loaded Successfully!")

spark.stop()