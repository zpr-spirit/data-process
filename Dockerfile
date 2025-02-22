FROM apache/airflow:2.5.1
RUN pip install pandas numpy SQLAlchemy psycopg2-binary -i https://pypi.tuna.tsinghua.edu.cn/simple