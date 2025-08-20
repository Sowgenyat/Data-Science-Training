import os
import json
import random
import logging
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
log = logging.getLogger(__name__)
AUDIT_FILE = "/tmp/audit_result.json
def data_pull(**kwargs):
    log.info("Pulling data from external API")
    data = {
        "transaction_id": random.randint(1000, 9999),
        "amount": random.randint(50, 5000),
        "timestamp": datetime.isoformat()
    }
    kwargs['ti'].xcom_push(key="pulled_data", value=data)
    log.info(f"Pulled Data: {data}")
def audit_rule_validation(**kwargs):
    ti = kwargs['ti']
    data = ti.xcom_pull(key="pulled_data", task_ids="data_pull_task")
    threshold = 1000
    result = {
        "transaction_id": data["transaction_id"],
        "amount": data["amount"],
        "passed": data["amount"] <= threshold,
        "timestamp": data["timestamp"]
    }
    with open(AUDIT_FILE, "w") as f:
        json.dump(result, f)
    log.info(f"Audit Result: {result}")
    if not result["passed"]:
        raise ValueError(f"Audit Failed: Amount {data['amount']} exceeds threshold {threshold}")
def log_audit_results(**kwargs):
    with open(AUDIT_FILE, "r") as f:
        result = json.load(f)
    if result["passed"]:
        log.info(f" Audit Success: Transaction {result['transaction_id']} passed ")
    else:
        log.error(f"Audit Failure: Transaction {result['transaction_id']} failed")
default_args = {
    "owner": "azad",
    "email": ["azad@example.com"],
    "email_on_failure": True,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    "start_date": datetime(2025, 1, 1),
}
with DAG(
    dag_id="data_audit_dag",
    default_args=default_args,
    description="Event-Driven Data Audit DAG",
    schedule_interval="@hourly",
    catchup=False,
) as dag:
    data_pull_task = PythonOperator(
        task_id="data_pull_task",
        python_callable=data_pull,
        provide_context=True,
    )
    audit_validation_task = PythonOperator(
        task_id="audit_validation_task",
        python_callable=audit_rule_validation,
        provide_context=True,
    )
    log_result_task = PythonOperator(
        task_id="log_result_task",
        python_callable=log_audit_results,
    )
    final_status_update = BashOperator(
        task_id="final_status_update",
        bash_command='echo "Data Audit DAG Completed Successfully at $(date)"'
    )
    data_pull_task >> audit_validation_task >> log_result_task >> final_status_update
