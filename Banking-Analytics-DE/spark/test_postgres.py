from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .master("local[*]")
    .appName("Postgres Test")
    .config(
        "spark.driver.extraClassPath",
        "jars/postgresql-42.7.7.jar"
    )
    .getOrCreate()
)

df = (
    spark.read
    .option("header", True)
    .option("delimiter", ";")
    .option("inferSchema", True)
    .csv("data/source/bank-full.csv")
)

df = df.withColumnRenamed("default", "default_status")

connection_properties = {
    "user": "postgres",
    "password": "root",
    "driver": "org.postgresql.Driver"
}

jdbc_url = "jdbc:postgresql://localhost:5432/banking_analytics"

df.limit(5).write \
    .mode("append") \
    .jdbc(
        url=jdbc_url,
        table="bronze.customer_raw",
        properties=connection_properties
    )

print("Successfully inserted 5 rows into PostgreSQL!")

spark.stop()