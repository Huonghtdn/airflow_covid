#step-1
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
import datetime as dt
default_args = {
    'owner': 'airflow',
    'start_date': dt.datetime(2020, 4, 1, 1, 00, 00),
    'retries': 1
}

dag = DAG('covid',
          default_args=default_args,
          schedule_interval='0 1 * * *',
          catchup=False
          )
#step-2
gitPath="https://github.com/Huonghtdn/airflow_covid/blob/main"
command_t1 = 'python '+gitPath+'/covid_func.py '
t1 = BashOperator(
          task_id = 'covidPlots',
          bash_command = command_t1,
          dag = dag
)

command_t2 = 'python '+gitPath+'/git_push.py '
t2 = BashOperator(
                  task_id = 'gitPush',
                  bash_command = command_t2,
                  dag = dag
)

t3 = BashOperator(
                 task_id = 'gitPush_repit',
                 bash_command = command_t2,
                 dag = dag)

t1 >> t2 >> t3
