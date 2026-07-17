from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .master("local[*]")
    .appName("SparkTest")
    .getOrCreate()
)

print("Spark Started Successfully!")

spark.stop()