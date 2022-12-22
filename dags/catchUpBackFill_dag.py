from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "vlinh",
    "retries": 5,
    "retry_delay": timedelta(seconds=20)
}

with DAG(
    dag_id="catchUpBackFill",
    default_args=default_args,
    start_date=datetime(year=2022, month=12, day=10),
    schedule_interval="@daily",
    catchup=False
) as dag:
    task1 = BashOperator(
        task_id="HelloWorld",
        bash_command="echo Hello World!"
    )