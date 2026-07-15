from pyspark.sql import SparkSession
from pyspark.sql.functions import count

from config import *
from db_connection import connection_properties
from logger import logger

# Create Spark Session
spark = (
    SparkSession.builder
    .master("local[*]")
    .appName("Gold Marital Summary")
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

logger.info(f"Silver Records: {silver_df.count()}")

# Marital Summary
marital_summary = (
    silver_df
    .groupBy("marital")
    .agg(
        count("*").alias("total_customers")
    )
)

logger.info("Writing Gold Marital Summary...")

(
    marital_summary.write
    .mode("overwrite")
    .jdbc(
        url=JDBC_URL,
        table="gold.marital_summary",
        properties=connection_properties
    )
)

logger.info("Gold Marital Summary Loaded Successfully!")

spark.stop()