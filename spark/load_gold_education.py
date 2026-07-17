from pyspark.sql import SparkSession
from pyspark.sql.functions import count

from config import *
from db_connection import connection_properties
from logger import logger

# Create Spark Session
spark = (
    SparkSession.builder
    .master("local[*]")
    .appName("Gold Education Summary")
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

# --------------------------------
# Education Summary
# --------------------------------

education_summary = (
    silver_df
    .groupBy("education")
    .agg(
        count("*").alias("total_customers")
    )
)

logger.info("Writing Gold Education Summary...")

(
    education_summary.write
    .mode("overwrite")
    .jdbc(
        url=JDBC_URL,
        table="gold.education_summary",
        properties=connection_properties
    )
)

logger.info("Gold Education Summary Loaded Successfully!")

spark.stop()