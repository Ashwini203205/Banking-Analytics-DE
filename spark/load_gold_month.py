from pyspark.sql import SparkSession
from pyspark.sql.functions import count, sum, when

from config import *
from db_connection import connection_properties
from logger import logger

# Create Spark Session
spark = (
    SparkSession.builder
    .master("local[*]")
    .appName("Gold Month Summary")
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

# Month Summary
month_summary = (
    silver_df
    .groupBy("month")
    .agg(
        count("*").alias("total_customers"),
        sum(
            when(silver_df.y == "yes", 1).otherwise(0)
        ).alias("subscribed_customers")
    )
)

logger.info("Writing Gold Month Summary...")

(
    month_summary.write
    .mode("overwrite")
    .jdbc(
        url=JDBC_URL,
        table="gold.month_summary",
        properties=connection_properties
    )
)

logger.info("Gold Month Summary Loaded Successfully!")

spark.stop()
