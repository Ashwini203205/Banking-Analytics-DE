from pyspark.sql import SparkSession
from pyspark.sql.functions import col

from config import *
from constants import *
from db_connection import connection_properties
from logger import logger

# Create Spark Session
spark = (
    SparkSession.builder
    .master("local[*]")
    .appName(APP_NAME)
    .config("spark.jars", JAR_PATH)
    .getOrCreate()
)

logger.info("Spark Session Started")

# Read CSV file
logger.info("Reading CSV File...")

df = (
    spark.read
    .option("header", "true")
    .option("delimiter", ";")
    .option("inferSchema", "true")
    .csv(SOURCE_FILE)
)

# Rename 'default' column because PostgreSQL uses 'default_status'
df = df.withColumnRenamed("default", "default_status")

logger.info(f"Total Records: {df.count()}")

# Display schema (optional)
df.printSchema()

# Display first 5 rows (optional)
df.show(5)

# Write data to Bronze table
logger.info("Loading data into Bronze Layer...")

(
    df.write
    .mode("overwrite")          # Change to "append" if needed
    .jdbc(
        url=JDBC_URL,
        table=BRONZE_TABLE,
        properties=connection_properties
    )
)

logger.info("Bronze Layer Loaded Successfully!")

spark.stop()

logger.info("Spark Session Stopped")