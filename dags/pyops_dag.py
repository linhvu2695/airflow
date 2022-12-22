from airflow import DAG, models
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator

default_args = {
    "owner": "vlinh",
    "retries": 5,
    "retry_delay": timedelta(seconds=20)
}

def greet(ti: models.TaskInstance):
    first_name = ti.xcom_pull(task_ids="get_name", key="first_name")
    last_name = ti.xcom_pull(task_ids="get_name", key="last_name")
    age = ti.xcom_pull(task_ids="get_age", key="age")
    name = first_name + " de " + last_name
    print(f"Hello World! I am {name} and I'm {age} years old")

def get_name(ti: models.TaskInstance):
    ti.xcom_push(key="first_name", value="Miguel")
    ti.xcom_push(key="last_name", value="Cervantes")

def get_age(ti: models.TaskInstance):
    ti.xcom_push(key="age", value=20)

with DAG(
    dag_id="pyops",
    default_args=default_args,
    description="This is my first DAG",
    start_date=datetime(year=2022, month=12, day=20),
    schedule_interval="@daily"
) as dag:
    task1 = PythonOperator(
        task_id="greet",
        python_callable=greet
    )
    task2 = PythonOperator(
        task_id="get_name",
        python_callable=get_name
    )
    task3 = PythonOperator(
        task_id="get_age",
        python_callable=get_age
    )
    task3 >> task1
    task2 >> task1