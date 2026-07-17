month_df = (
    silver_df
    .groupBy("month")
    .agg(count("*").alias("customers"))
)

(
    month_df.write
    .mode("overwrite")
    .jdbc(
        url=JDBC_URL,
        table="gold.month_summary",
        properties=connection_properties
    )
)