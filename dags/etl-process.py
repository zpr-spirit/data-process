from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
from sqlalchemy import create_engine

# 定义默认参数
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'user_trans_process',
    default_args=default_args,
    description='Read user_info and trans_detail, join them, and write to PostgreSQL',
    schedule_interval='0 0 * * *',
    catchup=False,
)

# 读取用户信息表
def read_user_info():
    df_userinfo = pd.read_csv('/root/przhang/data-process/data/process-data-userinfo.csv')
    return df_userinfo

# 读取交易流水表
def read_transac_detail():
    trans_detail = pd.read_json('/root/przhang/data-process/data/process-data-trans-detail.json')
    trans_detail['timestamp'] = pd.to_datetime(trans_detail['timestamp'])
    user_mean_amount = trans_detail.groupby('user_id')['amount'].transform('mean')
    trans_detail['amount'] = trans_detail['amount'].fillna(user_mean_amount)
    return trans_detail

# 合并数据并写入 PostgreSQL
def join_and_write_to_postgres(**kwargs):
    # 从上游任务获取数据
    ti = kwargs['ti']
    df_userinfo = ti.xcom_pull(task_ids='read_user_info_task')
    df_transaction = ti.xcom_pull(task_ids='read_transac_detail_task')

    # 按照 id 进行 join
    merged_df = pd.merge(df_userinfo, df_transaction, left_on='id', right_on='user_id')
    need_cols = ["transaction_id", "user_id", "name", "email", "signup_date", "amount", "timestamp"]
    merged_df = merged_df[need_cols]

    # 写入 PostgreSQL
    engine = create_engine('postgresql+psycopg2://airflow:airflow@localhost:5432/dataprocess')  # 替换为实际连接信息
    merged_df.to_sql('merged_table', engine, if_exists='replace', index=False)

# 定义任务
read_csv_task = PythonOperator(
    task_id='read_csv_task',
    python_callable=read_user_info,
    dag=dag,
)

read_json_task = PythonOperator(
    task_id='read_json_task',
    python_callable=read_transac_detail,
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