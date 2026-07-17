from pyspark.sql import SparkSession
from pyspark.sql.functions import count

from config import *
from db_connection import connection_properties
from logger import logger

# Create Spark Session
spark = (
    SparkSession.builder
    .master("local[*]")
    .appName("Gold Job Summary")
    .config("spark.jars", JAR_PATH)
    .getOrCreate()
)

logger.info("Reading Silver Table...")

silver_df = (
    spark.read
    .jdbc(
        url=JDBC_URL,
        table="silver.customer_clean",
        properties=connection_properties
    )
)

logger.info(f"Silver Records: {silver_df.count()}")

# Job Summary
job_df = (
    silver_df
    .groupBy("job")
    .agg(
        count("*").alias("total_customers")
    )
)

logger.info("Writing Gold Job Summary...")

(
    job_df.write
    .mode("overwrite")
    .jdbc(
        url=JDBC_URL,
        table="gold.job_summary",
        properties=connection_properties
    )
)

logger.info("Gold Job Summary Loaded Successfully!")

spark.stop()