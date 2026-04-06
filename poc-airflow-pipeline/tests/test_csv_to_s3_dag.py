import pytest
import pandas as pd
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../dags"))

def test_csv_to_s3_dag_imports():
    from csv_to_s3_dag import dag
    assert dag.dag_id == "csv_to_s3"

def test_dag_has_tasks():
    from csv_to_s3_dag import dag
    task_ids = [task.task_id for task in dag.tasks]
    assert "extract_and_validate" in task_ids
    assert "transform_and_calculate" in task_ids
    assert "upload_to_s3" in task_ids

def test_dag_task_order():
    from csv_to_s3_dag import dag
    task_ids = [task.task_id for task in dag.tasks]
    assert task_ids.index("extract_and_validate") < task_ids.index("transform_and_calculate")
    assert task_ids.index("transform_and_calculate") < task_ids.index("upload_to_s3")

def test_dag_schedule():
    from csv_to_s3_dag import dag
    assert dag.schedule_interval == "@daily"
    assert dag.catchup == False

def test_transform_logic():
    df = pd.DataFrame({
        "price": [10.0, 20.0, 30.0],
        "quantity": [2, 3, 1],
        "product_id": ["A", "B", "C"]
    })
    df["total"] = df["price"] * df["quantity"]
    df["discounted_total"] = df["total"] * 0.9
    assert list(df["total"]) == [20.0, 60.0, 30.0]
    assert list(df["discounted_total"]) == [18.0, 54.0, 27.0]
