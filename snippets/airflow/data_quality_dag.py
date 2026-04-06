from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="data_quality_check",
    start_date=datetime(2025, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    default_args=default_args,
    tags=["ai-devops", "data-quality"],
) as dag:

    def check_data_quality(**context):
        import pandas as pd
        df = pd.read_csv("/opt/airflow/data/input.csv")
        null_counts = df.isnull().sum()
        duplicates = df.duplicated().sum()
        print(f"Null values:\n{null_counts}")
        print(f"Duplicates: {duplicates}")
        if duplicates > 0:
            raise ValueError(f"Found {duplicates} duplicate rows")

    quality_check = PythonOperator(
        task_id="check_data_quality",
        python_callable=check_data_quality,
        provide_context=True,
    )

    quality_check
