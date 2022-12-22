from airflow import DAG, models
from datetime import datetime, timedelta
from airflow.decorators import dag, task

default_args = {
    "owner": "vlinh",
    "retries": 5,
    "retry_delay": timedelta(seconds=20)
}

@dag(dag_id="taskflowApi", 
    default_args=default_args, 
    start_date=datetime(year=2022, month=12, day=20),
    schedule_interval="@daily")
def hello_world_etl():
    @task(multiple_outputs=True)
    def get_name():
        return {
            "first_name":"Miguel",
            "last_name":"Cervantes"
        }
    
    @task()
    def get_age():
        return 20
    
    @task()
    def greet(first_name, last_name, age):
        print(f"Hello World! I am {first_name} de {last_name} and I am {age} years olf")

    name = get_name()
    age = get_age()
    greet(first_name=name["first_name"], 
        last_name=name["last_name"], 
        age=age)

greet_dag = hello_world_etl()