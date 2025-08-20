import os
import json
import logging
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from datetime import datetime

log = logging.getLogger(__name__)

SHARED_DIR = "/opt/airflow/shared"

def transform_data(**context):
    conf = (context.get("dag_run") and context["dag_run"].conf) or {}
    input_path = conf.get("input_path", f"{SHARED_DIR}/extracted_data.json")
    output_path = conf.get("output_path", f"{SHARED_DIR}/transformed_data.json")

    with open(input_path, "r") as f:
        data = json.load(f)

    data["city"] = data["city"].upper()
    data["full_label"] = f"{data['name']} ({data['age']}) - {data['city']}"

    with open(output_path, "w") as f:
        json.dump(data, f)

    log.info(f"Transformed Data saved: {data}")

default_args = {"owner": "azad", "start_date": datetime(2025, 1, 1)}

with DAG(
    dag_id="transform_dag",
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    description="Transform Stage of ETL Pipeline"
) as dag:

    transform_task = PythonOperator(
        task_id="transform_task",
        python_callable=transform_data
    )

    preview_file = BashOperator(
        task_id="preview_transformed_file",
        bash_command=f'echo "Transformed Data:" && cat {SHARED_DIR}/transformed_data.json'
    )

    trigger_load = TriggerDagRunOperator(
        task_id="trigger_load_dag",
        trigger_dag_id="load_dag",
        conf={"input_path": f"{SHARED_DIR}/transformed_data.json"},
        wait_for_completion=False
    )
    transform_task >> preview_file >> trigger_load

