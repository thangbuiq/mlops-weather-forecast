from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime

default_args = {"start_date": datetime(2022, 1, 1), "retries": 1}

with DAG("test_dag", default_args=default_args, schedule_interval="@once") as dag:
    echo_task = BashOperator(
        task_id="echo_task",
        bash_command="echo 1",
    )

    echo_task
