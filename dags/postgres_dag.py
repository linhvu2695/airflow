from airflow import DAG, models
from datetime import datetime, timedelta
from airflow.providers.postgres.operators.postgres import PostgresOperator

default_args = {
    "owner": "vlinh",
    "retries": 5,
    "retry_delay": timedelta(seconds=20)
}

with DAG(
    dag_id="postgres",
    default_args=default_args,
    start_date=datetime(2022, 12, 20),
    schedule_interval="0 0 * * *"
) as dag:
    task1 = PostgresOperator(
        task_id="create_table",
        postgres_conn_id="postgres_localhost",
        sql="""
            CREATE TABLE IF NOT EXISTS dag_runs (
                dt DATE,
                dag_id CHARACTER VARYING,
                PRIMARY KEY (dt, dag_id)
            )
        """
    )
    task2 = PostgresOperator(
        task_id="insert_table",
        postgres_conn_id="postgres_localhost",
        sql="""
            INSERT INTO dag_runs (dt, dag_id) VALUES ('{{ds}}', '{{dag.dag_id}}') ON CONFLICT DO NOTHING
        """
    )
    task3 = PostgresOperator(
        task_id="delete_table",
        postgres_conn_id="postgres_localhost",
        sql="""
            DELETE FROM dag_runs WHERE dt = '{{ds}}' AND dag_id = '{{dag.dag_id}}'
        """
    )

    task1 >> task3 >> task2