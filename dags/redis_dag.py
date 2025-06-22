from airflow import DAG
from datetime import datetime
import os
import sys


sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pipelines.aws_s3_pipeline import upload_s3_pipeline




from airflow.operators.python_operator import PythonOperator
from pipelines.reddit_pipeline import reddit_pipeline

default_args={
    'owner': 'Vivek Basavanth Hanagoji',
    'start_date': datetime(2024, 1, 18)
}

file_postfix = datetime.now().strftime("%Y%m%d")


dag = DAG(
    
    dag_id = "etl_reddit_pipeline",
    default_args = default_args,
    schedule_interval = '@daily',
    catchup = False,
    tags=['reddit','etl', 'pipeline']
)

#extration of data from Reddit.

extract = PythonOperator(
    task_id = 'reddit_extraction',
    python_callable = reddit_pipeline,
    op_kwargs = {
        'file_name': f'reddit_{file_postfix}',
        'subreddit': 'DataEngineering',
        'time_filter': 'month',
        'limit': 10000
    },
    dag=dag
)

upload_s3 = PythonOperator(
    task_id = 's3_upload',
    python_callable = upload_s3_pipeline,
    dag= dag
)

extract >> upload_s3