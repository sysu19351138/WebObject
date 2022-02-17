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
class USER_INFO(db.Model):
    # 定义表名
    __tablename__ = 'USER_INFO'
    # 定义字段
    #id = db.Column(db.Integer, primary_key=True)  # 编号
    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(20), nullable=False)
    #addtime = db.Column(db.DateTime, nullable=False)


if __name__ == '__main__':

    # 删除所有表
    db.drop_all()

    # 创建所有表
    db.create_all()