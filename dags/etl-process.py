from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine

# 定义默认参数
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
}

# 定义 DAG
dag = DAG(
    'csv_json_to_postgres',
    default_args=default_args,
    description='Read CSV and JSON, join them, and write to PostgreSQL',
    schedule_interval=None,  # 手动触发
    catchup=False,
)

# 读取用户信息表
def read_csv():
    df_userinfo = pd.read_csv('/path/to/test1.csv')
    return df_userinfo

# 读取交易流水表
def read_json():
    df_transaction = pd.read_json('/path/to/test2.json')
    return df_transaction

# 合并数据并写入 PostgreSQL
def join_and_write_to_postgres(**kwargs):
    # 从上游任务获取数据
    ti = kwargs['ti']
    df_userinfo = ti.xcom_pull(task_ids='read_csv_task')
    df_transaction = ti.xcom_pull(task_ids='read_json_task')

    # 按照 id 进行 join
    merged_df = pd.merge(df_userinfo, df_transaction, left_on='id', how='inner')

    # 写入 PostgreSQL
    engine = create_engine('postgresql+psycopg2://user:password@host:port/dbname')  # 替换为实际连接信息
    merged_df.to_sql('merged_table', engine, if_exists='replace', index=False)

# 定义任务
read_csv_task = PythonOperator(
    task_id='read_csv_task',
    python_callable=read_csv,
    dag=dag,
)

read_json_task = PythonOperator(
    task_id='read_json_task',
    python_callable=read_json,
    dag=dag,
)

join_and_write_task = PythonOperator(
    task_id='join_and_write_task',
    python_callable=join_and_write_to_postgres,
    provide_context=True,  # 允许传递上下文
    dag=dag,
)

# 设置任务依赖
read_csv_task >> join_and_write_task
read_json_task >> join_and_write_task