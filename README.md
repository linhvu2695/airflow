# Airflow Tutorial

## Running Airflow locally

### 1. Installation
- Install Airflow with the following command (adjust the python version accordingly)
```
pip install 'apache-airflow==2.5.0' \
 --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.5.0/constraints-3.7.txt"
```

### 2. Initialization
- `export AIRFLOW_HOME=<current_dir>` change airflow home directory to the project directory - use absolute path (by default is at `~/airflow`)
- `airflow db init` create sqlite `airflow.db`, log folder `logs/` & some config files
- Create username & password
```
airflow users create \
    --username admin \
    --firstname firstname \
    --lastname lastname \
    --role Admin
    --email admin@admin.com

// Will prompt to set up password
```
- `airflow webserver -p 8080` initiate webserver. The webserver is available at `http://localhost:8080`
- `airflow scheduler` initiate scheduler in another terminal. Be reminded to change airflow home directory first

## Running Airflow on Docker
- `curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.5.0/docker-compose.yaml'` fetch docker-compose file
- The file can be edited to a non-Celery version
- `mkdir -p ./dags ./logs ./plugins` create mounted directories for the containers
- `docker-compose up airflow-init` set up database migrations and create the first user account
- `docker-compose up -d` run Airflow on Docker
- Login to airflow at `http://localhost:8080` using credentials `airflow:airflow`

## DAG design

### Dependency
```
task1 >> task2
task1.set_downstream(task2)
```

### Bash operator
```
task = BashOperator(
        task_id="hello",
        bash_command="echo Hello World"
    )
```

### Python operator
```
def greet(ti: models.TaskInstance):
    name = ti.xcom_pull(task_ids="greet", key="name")
    print(f"Hello World! I am {name}")

task = PythonOperator(
        task_id="greet",
        python_callable=greet,
        op_kwargs={"name": "Cervantes", "age": "20"}
    )
```

### Taskflow API
```
@task()
def greet():
    ...
```

### Backfill
Catchup: use parameter `catchup` when declare DAG<br>
Backfill: 
- `docker exec -it airflow-airflow-scheduler-1 bash` to enter scheduler container<br>
- `airflow dags backfill -s <start_date> -e <end_date> <DAG_name>` to backfill tasks

### Cronjob
Use parameter `schedule_interval` when declare DAG
```
with DAG(
    ...
    schedule_interval="0 0 * * *",
    ...
) as dag:
```

## Postgres

### Connection
- Ensure to have package `airflow.providers.postgres`. If package is not found, install `pip install apache-airflow-providers-postgres` (make sure the system have Postgres installed - `brew install postgresql`)
- Set up database and tables in local PostgreSQL
- Use Airflow web interface to add connection (put the host as `host.docker.internal` if Airflow is running on Docker)

### Postgres operator
```
task = PostgresOperator(
        task_id="insert_table",
        postgres_conn_id="postgres_localhost",
        sql="""
            INSERT INTO dag_runs (dt, dag_id) VALUES ('{{ds}}', '{{dag.dag_id}}') ON CONFLICT DO NOTHING
        """
    )
```


