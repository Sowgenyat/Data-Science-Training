from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import Bashüperator
from datetime import datetime
import os
MESSAGE PATH="/tmp/airflow_message.txt"
def generate message():
    message ="Hello, this message flows through tasks!"
    with open(MESSAGE_PATH, 'w') as f:
        f.write(message)
def read message():
    if os.path.exists(MESSAGE_PATH):
        with open(MESSAGE PATH, 'r') as f:
            print("Message from file:", f.read())
    else:
        raise FileNotFoundError("Message file does not exist.")
with DAG(
    dag_id="chained_tasks_dag",
    start_date= datetime(year: 2023, monthi day 1)
    schedule_interval=None,
    catchup=False,
    tags=["example"]
) as dag:
    generate= PythonOperator(
        task_id="generate_message",
        python_callable=generate_message)
    simulate_save Bashüperator(
        task_id=simulate_file_confirmation",
        bash_command=f"echo 'Message saved at [MESSAGE_PATH}"
    read PythonOperator(
        task id="read_message",
        python_callable=read_message)
    generate >> simulate_save >> read
