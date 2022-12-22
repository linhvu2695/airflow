from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "vlinh",
    "retries": 5,
    "retry_delay": timedelta(seconds=20)
}

with DAG(
    dag_id="test",
    default_args=default_args,
    description="This is my first DAG",
    start_date=datetime(year=2022, month=12, day=20),
    schedule_interval="@daily"
) as dag:
    task1 = BashOperator(
        task_id="first_task",
        bash_command="echo Hello World"
    )
    task2 = BashOperator(
        task_id="SecondTask",
        bash_command="echo Ran after task1 is completed"
    )
    task3 = BashOperator(
        task_id="ThirdTask",
        bash_command=("echo Also ran after task1 is completed")
    )
    #task1.set_downstream(task2)
    #task1.set_downstream(task3)

    # task1 >> task2
    # task1 >> task3

    task1 >> [task2, task3]

