import os
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Default args for DAG
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

# Base directory of the DAG file
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Define DAG
with DAG(
    dag_id='telco_churn_ml_pipeline',
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule_interval=None,  # Can be '0 12 * * *' for daily runs
    catchup=False,
    tags=['ml', 'telco', 'churn'],
) as dag:

    fetch_data = BashOperator(
        task_id='fetch_data',
        bash_command=f'python3 {BASE_DIR}/scripts/fetch_data.py',
        dag=dag
    )

    preprocess_data = BashOperator(
        task_id='preprocess_data',
        bash_command=f'python3 {BASE_DIR}/scripts/preprocess_validate.py',
        dag=dag
    )

    train_model = BashOperator(
        task_id='train_model',
        bash_command=f'python3 {BASE_DIR}/scripts/train_evaluate.py',
        dag=dag
    )

    # Set task dependencies
    fetch_data >> preprocess_data >> train_model
