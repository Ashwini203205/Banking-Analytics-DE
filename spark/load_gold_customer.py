from pyspark.sql import SparkSession
from pyspark.sql.functions import count, avg, sum, when, col

from config import *
from db_connection import connection_properties
from logger import logger

# Create Spark Session
spark = (
    SparkSession.builder
    .master("local[*]")
    .appName("Gold Customer Summary")
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

# Customer KPI Summary
customer_summary = (
    silver_df
    .agg(
        count("*").alias("total_customers"),

        sum(
            when(col("y") == "yes", 1).otherwise(0)
        ).alias("subscribed_customers"),

        avg("age").alias("average_age"),

        avg("balance").alias("average_balance"),

        sum("balance").alias("total_balance")
    )
)

logger.info("Writing Gold Customer Summary...")

(
    customer_summary.write
    .mode("overwrite")
    .jdbc(
        url=JDBC_URL,
        table="gold.customer_summary",
        properties=connection_properties
    )
)

logger.info("Gold Customer Summary Loaded Successfully!")

spark.stop()