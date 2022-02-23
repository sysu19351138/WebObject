from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)

class Config(object):
    """配置参数"""
    # 设置连接数据库的URL 需要更改 密码 与 数据库名
    user = 'root'
    password = 'wch011005'
    database = 'USER_INFO'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@127.0.0.1:3306/%s' % (user,password,database)

    # 设置sqlalchemy自动更跟踪数据库
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # 查询时会显示原始SQL语句
    app.config['SQLALCHEMY_ECHO'] = True

    # 禁止自动提交数据处理
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False

# 读取配置
app.config.from_object(Config)

# 创建数据库sqlalchemy工具对象
db = SQLAlchemy(app)

# 用户信息表
class USER_INFO(db.Model):
    # 定义表名
    __tablename__ = 'USER_INFO'
    # 定义字段
    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(20), nullable=False)

# 创建服务信息表
class SERVICE_INFO(db.Model):
    # 定义表名
    __tablename__ = 'SERVICE_INFO'
    # 服务名
    servicename = db.Column(db.String(20), primary_key=True)
    # 服务简介
    servicebrief = db.Column(db.String(50), nullable=False)
    # 服务详情
    servicedetail = db.Column(db.String(50), nullable=False)
    # 所请求的服务是否有已训练模型
    iftrained = db.Column(db.Boolean, nullable=False)
    # 所请求的服务是否训练
    iftrainable = db.Column(db.Boolean, nullable=False)
    # 负责该人的管理员ID
    adminid = db.Column(db.String(20), nullable=False)
    # 服务使用者ID
    userid = db.Column(db.String(20), nullable=False)

# 创建全局模型信息表
class GLOBAL_MODEL_INFO(db.Model):
    # 定义表名
    __tablename__ = 'GLOBAL_MODEL_INFO'
    # 服务名
    servicename = db.Column(db.String(20), primary_key=True, nullable=False)
    # 模型版本
    modelversion = db.Column(db.String(20), primary_key=True, nullable=False)
    # 最大训练轮数
    maxround = db.Column(db.Integer, nullable=True)
    # 聚合协调时序
    aggregationtiming = db.Column(db.String(20), nullable=True)
    # 收敛精度
    epsilon = db.Column(db.String(20), nullable=True)
    # 批量大小
    batchsize = db.Column(db.Integer, nullable=True)
    # 学习率
    lr = db.Column(db.Float, nullable=True)
    # 初始化策略保存时间
    initializetime = db.Column(db.DateTime, nullable=True)
    # 该训练已聚合更新轮次
    updatenum = db.Column(db.Integer, nullable=True)
    # 上一次聚合更新时间
    updatetime = db.Column(db.DateTime, nullable=True)
    # 训练结果保存的本地路径
    modelpath = db.Column(db.String(20), nullable=True)
