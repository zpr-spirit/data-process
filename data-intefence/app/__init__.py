from flask import Flask, jsonify, request, g, Response
from controller.trans_search import router_trans
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://airflow:airflow@localhost:5432/dataprocess'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 禁用跟踪修改以节省资源

# 初始化 SQLAlchemy
db = SQLAlchemy(app)
app.register_blueprint(router_trans)