from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'banking_analytics',
    'depends_on_past': False,
    'start_date': datetime(2026, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='banking_data_ingestion',
    default_args=default_args,
    description='Banking Analytics ETL Pipeline',
    schedule_interval='@daily',
    catchup=False,
) as dag:

    test_connection = BashOperator(
        task_id='run_test_connection',
        bash_command='python /opt/airflow/dags/test_connection.py'
    )

    bronze = BashOperator(
        task_id='load_bronze',
        bash_command='python /opt/airflow/spark/load_bronze.py'
    )

    silver = BashOperator(
        task_id='load_silver',
        bash_command='python /opt/airflow/spark/load_silver.py'
    )

    customer = BashOperator(
        task_id='gold_customer',
        bash_command='python /opt/airflow/spark/load_gold_customer.py'
    )

    job = BashOperator(
        task_id='gold_job',
        bash_command='python /opt/airflow/spark/load_gold_job.py'
    )

    education = BashOperator(
        task_id='gold_education',
        bash_command='python /opt/airflow/spark/load_gold_education.py'
    )

    marital = BashOperator(
        task_id='gold_marital',
        bash_command='python /opt/airflow/spark/load_gold_marital.py'
    )

    month = BashOperator(
        task_id='gold_month',
        bash_command='python /opt/airflow/spark/load_gold_month.py'
    )

    test_connection >> bronze >> silver >> customer >> job >> education >> marital >> month