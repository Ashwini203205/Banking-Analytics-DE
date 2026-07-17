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
    'banking_data_ingestion',
    default_args=default_args,
    description='Automated pipeline for banking analytics',
    schedule_interval='@daily',  # Runs once a day automatically
    catchup=False,
) as dag:

    # Task to execute our python script inside the container
    run_python_script = BashOperator(
        task_id='run_test_connection',
        bash_command='python /opt/airflow/dags/test_connection.py', 
        # Note: In a production environment, you would place scripts inside the DAG folder 
        # or build a custom Docker image with your dependencies installed.
    )

    run_python_script