# 使用官方 Python 镜像作为基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制项目文件到容器中
COPY . .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 暴露端口（Flask 默认端口是 5000）
EXPOSE 8088

# 设置环境变量
ENV FLASK_APP=run.py
ENV FLASK_ENV=production

# 启动应用
CMD ["flask", "run", "--host=0.0.0.0", "--port", "8088"]
