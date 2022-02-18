from flask import Flask, jsonify,abort, make_response
from flask import request
from CorV_token import create_token,verify_token
import json
import mysql_sql

# 参考网址
# https://blog.csdn.net/u012212157/article/details/78216267
# https://www.cnblogs.com/nimingdaoyou/p/9037812.html

app = Flask(__name__)
MY_URL = '/api/'

# get
# http://192.168.2.105:5100/everything/api/v1/tasks/get/?what=hello
@app.route(MY_URL + 'tasks/get/', methods=['GET'])
def get_task():
    # 必须存在某个参数
    if not 'name' in request.args.to_dict():
        abort(404)
    print(request.args.to_dict())  #
    return str(request.args.to_dict())


# post
@app.route(MY_URL + 'tasks/post/', methods=['POST'])
def post_task():
    print(request.json)
    if not request.json:
        abort(404)
    print('222222222')
    global hello
    hello = hello + str(request.json)
    print(hello)
    return jsonify(request.json)


# 404处理
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


##########################
# 访问示例
# http://192.168.2.105:5100/everything/api/v1/tasks/login/?name=18811891816&password=18811891816
@app.route(MY_URL + 'login/', methods=['POST'])
def login():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    try:
        username = data.get('username')
        password = data.get('password')
    except Exception:
        abort(404)

    # 检查匹配
    TorF = mysql_sql.match(username, password)
    if TorF == str(True):
        # token生成
        token = create_token(username)
        # json生成
        data = {
            "code": 200,
            "message": "Success",
            "token": token
        }
        ret_json = json.dumps(data)
    elif TorF == str(False):
        data = {
            "code": 400,
            "message": "False"
        }
        ret_json = json.dumps(data)

    return ret_json

@app.route(MY_URL + 'home_source/', methods=['GET','POST'])
def home_source():
    data = request.get_data()
    #据说要改
    # token = request.values.get('token')
    data = json.loads(data.decode("utf-8"))
    token = data.get('token')

    try:
        data = verify_token(token)
    except Exception:
        abort(404)
    # 检查匹配
    TorF = mysql_sql.find(data['username'])
    if TorF == str(True):
        username = data["username"]
        # json生成
        data = {
            "code": 200,
            "message": "Success",
            "username": username
        }
    elif TorF == str(False):
        data = {
            "code": 200,
            "message": "False"
        }

    ret_json = json.dumps(data)
    return ret_json


if __name__ == '__main__':
    app.run()