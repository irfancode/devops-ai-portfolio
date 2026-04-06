from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
import boto3
import os

S3_BUCKET = os.environ.get("S3_BUCKET", "my-analytics-bucket")
INPUT_PATH = "/opt/airflow/data/input.csv"
OUTPUT_PATH = "/opt/airflow/data/output.csv"

def extract_and_validate(**context):
    df = pd.read_csv(INPUT_PATH)
    required_cols = ["price", "quantity", "product_id"]
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    df = df.dropna()
    context["ti"].xcom_push(key="row_count", value=len(df))
    return f"Extracted {len(df)} rows"

def transform_and_calculate(**context):
    df = pd.read_csv(INPUT_PATH)
    df["total"] = df["price"] * df["quantity"]
    df["discounted_total"] = df["total"] * 0.9
    df["processed_at"] = datetime.now().isoformat()
    df.to_csv(OUTPUT_PATH, index=False)
    return f"Transformed {len(df)} rows"

def upload_to_s3(**context):
    s3 = boto3.client("s3")
    s3.upload_file(OUTPUT_PATH, S3_BUCKET, f"output/{datetime.now().strftime('%Y/%m/%d')}/output.csv")
    return f"Uploaded to s3://{S3_BUCKET}/output/"

with DAG(
    dag_id="csv_to_s3",
    start_date=datetime(2025, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    default_args={
        "retries": 2,
        "retry_delay": timedelta(minutes=5),
        "sla": timedelta(hours=1),
    },
    tags=["ai-devops", "analytics"],
) as dag:
    extract = PythonOperator(
        task_id="extract_and_validate",
        python_callable=extract_and_validate,
        provide_context=True,
    )

    transform = PythonOperator(
        task_id="transform_and_calculate",
        python_callable=transform_and_calculate,
        provide_context=True,
    )

    upload = PythonOperator(
        task_id="upload_to_s3",
        python_callable=upload_to_s3,
        provide_context=True,
    )

    extract >> transform >> upload
