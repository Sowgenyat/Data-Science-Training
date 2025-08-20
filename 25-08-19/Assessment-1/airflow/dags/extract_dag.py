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
os.makedirs(SHARED_DIR, exist_ok=True)

def extract_data(**kwargs):
    data = {"name": "Azad", "age": 23, "city": "Chennai"}
    file_path = os.path.join(SHARED_DIR, "extracted_data.json")
    with open(file_path, "w") as f:
        json.dump(data, f)
    log.info(f" Data extracted and saved: {data}")

default_args = {"owner": "azad", "start_date": datetime(2025, 1, 1)}

with DAG(
    dag_id="extract_dag",
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    description="Extract Stage of ETL Pipeline"
) as dag:

    extract_task = PythonOperator(
        task_id="extract_task",
        python_callable=extract_data
    )

    validate_file = BashOperator(
        task_id="validate_extracted_file",
        bash_command=f'ls -lh {SHARED_DIR}/extracted_data.json && cat {SHARED_DIR}/extracted_data.json'
    )

    trigger_transform = TriggerDagRunOperator(
        task_id="trigger_transform_dag",
        trigger_dag_id="transform_dag",
        conf={
            "input_path": f"{SHARED_DIR}/extracted_data.json",
            "output_path": f"{SHARED_DIR}/transformed_data.json"
        },
        wait_for_completion=False
    )

    extract_task >> validate_file >> trigger_transform

