from __future__ import annotations
from datetime import datetime, timedelta

import pandas as pd
import psycopg2
from airflow import DAG
from airflow.operators.python import PythonOperator

DB_CONFIG = {
    "host": "postgres",      # docker-compose service name, not localhost
    "port": 5432,
    "dbname": "banking_db",
    "user": "admin",
    "password": "password123",
}

DATA_PATH = "/opt/airflow/data/bank.csv"  # adjust filename if different

default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

COLUMNS = ["age","job","marital","education","default","balance","housing","loan",
           "contact","day","month","duration","campaign","pdays","previous","poutcome","y"]

def load_bronze(**context):
    df = pd.read_csv(DATA_PATH)
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("TRUNCATE TABLE bronze.customer_raw")
    rows = [tuple(row[c] for c in COLUMNS) for _, row in df.iterrows()]
    cur.executemany(
        f"""INSERT INTO bronze.customer_raw
            ({','.join(c if c != 'default' else 'default_status' for c in COLUMNS)})
            VALUES ({','.join(['%s']*len(COLUMNS))})""",
        rows,
    )
    conn.commit()
    cur.close()
    conn.close()

def load_silver(**context):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("TRUNCATE TABLE silver.customer_clean")
    cur.execute("""
        INSERT INTO silver.customer_clean
        SELECT * FROM bronze.customer_raw
        WHERE age IS NOT NULL AND balance IS NOT NULL
    """)
    conn.commit()
    cur.close()
    conn.close()

def load_gold(**context):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("TRUNCATE TABLE gold.customer_summary")
    cur.execute("""
        INSERT INTO gold.customer_summary
        SELECT
            COUNT(*) AS total_customers,
            SUM(CASE WHEN y = 'yes' THEN 1 ELSE 0 END) AS subscribed_customers,
            AVG(age) AS average_age,
            AVG(balance) AS average_balance,
            SUM(balance) AS total_balance
        FROM silver.customer_clean
    """)
    conn.commit()
    cur.close()
    conn.close()

with DAG(
    dag_id="banking_bronze_silver_gold",
    default_args=default_args,
    description="Load bank marketing CSV through bronze -> silver -> gold layers",
    schedule_interval="@daily",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["banking", "etl"],
) as dag:

    bronze_task = PythonOperator(task_id="load_bronze", python_callable=load_bronze)
    silver_task = PythonOperator(task_id="load_silver", python_callable=load_silver)
    gold_task = PythonOperator(task_id="load_gold", python_callable=load_gold)

    bronze_task >> silver_task >> gold_task