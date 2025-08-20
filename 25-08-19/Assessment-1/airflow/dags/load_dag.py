import os
import json
import logging
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime

log = logging.getLogger(__name__)

SHARED_DIR = "/opt/airflow/shared"

def load_data(**context):
    conf = (context.get("dag_run") and context["dag_run"].conf) or {}
    input_path = conf.get("input_path", f"{SHARED_DIR}/transformed_data.json")

    with open(input_path, "r") as f:
        data = json.load(f)

    log.info(f"Final Data Loaded: {data}")

default_args = {"owner": "azad", "start_date": datetime(2025, 1, 1)}

with DAG(
    dag_id="load_dag",
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    description="Load Stage of ETL Pipeline"
) as dag:

    load_task = PythonOperator(
        task_id="load_task",
        python_callable=load_data
    )

    success_msg = BashOperator(
        task_id="success_message",
        bash_command='echo "Data successfully loaded into target system!"'
    )

    load_task >> success_msg


