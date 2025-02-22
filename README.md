# data-process
IM data etl process

## 系统部署
### 1. 构建自定义airflow镜像，安装以来
```bash
docker build -t airflow-own:v0.1 .
```
### 2. 启动psql和airflow服务
```bash
# 启动postgresql服务
docker-compose up -d postgres
# 初始化 Airflow 数据库
docker-compose run airflow-webserver airflow db init
# 创建一个管理员用户以便登录 Airflow Web UI
docker-compose run airflow-webserver airflow users create \
    --username admin \
    --password admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com
# 使用 Docker Compose 启动所有服务
docker-compose up -d
```

### 3. 启动数据查询后台服务


## 系统运行截图
airflow dag_run execute status

psql database
![alt text](image-2.png)
Retrieve a list of users with their total transaction amounts.
![alt text](image.png)
Retrieve transaction details for a specific user.
![alt text](image-1.png)