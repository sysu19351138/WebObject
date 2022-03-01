from flask import Flask, jsonify,abort, make_response
from flask import request,Response
from CorV_token import create_token,verify_token
import json
import redis
import mysql_sql
import os
import time
import mysql_sql

app = Flask(__name__)
MY_URL = '/api/'

"""通用接口"""
# 404 处理
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

"""登陆注册接口"""
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
    TorF = mysql_sql.USER_INFO_match(username, password)
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

"""请求发布接口"""
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
    TorF = mysql_sql.USER_INFO_find(data['username'])['flag']
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

@app.route(MY_URL + 'service_visualize/', methods=['GET', 'POST'])
def service_visualize():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    token = data.get('token')

    try:
        data = verify_token(token)
    except Exception:
        abort(404)
    # 检查匹配

    TorF = mysql_sql.USER_INFO_find(data['username'])['flag']

    if TorF == str(True):
        service_info = mysql_sql.SERVICE_INFO_get()
        length = len(service_info)

        def get_data(servicename: str, servicebrief: str, servicedetail: str, next: str, nextdata):
            return {
                "servicename": servicename,
                "servicebrief": servicebrief,
                "servicedetail": servicedetail,
                "next": next,
                "nextdata": nextdata
            }

        data = get_data(service_info[length - 1][0], service_info[length - 1][1], service_info[length - 1][2], "0",
                        "null")
        for i in range(length - 1):
            data = get_data(service_info[length - i - 2][0], service_info[length - i - 2][1],
                            service_info[length - i - 2][2], "1", data)

        # json生成
        data = {
            "code": 200,
            "message": "Success",
            "data": data
        }
    elif TorF == str(False):
        data = {
            "code": 200,
            "message": "False"
        }

    ret_json = json.dumps(data)
    return ret_json

# 用以校验token 并发布流信息
@app.route(MY_URL + 'service_request/', methods=['GET','POST'])
def service_request():

    data = request.get_data()
    data = json.loads(data.decode("utf-8"))

    # 获取 token servicename 并校验 token
    try:
        token = data.get('token')
        servicename = data.get('servicename')
        data = verify_token(token)
    except Exception:
        abort(404)
    # 检查匹配
    TorF = mysql_sql.USER_INFO_find(data['username'])['flag']
    TorF1 = mysql_sql.SERVICE_INFO_find(servicename)['flag']
    TorF = TorF & TorF1
    if TorF == str(True):
        # json生成
        data = {
            "code": 200,
            "message": "Publish Success",
        }
    elif TorF == str(False):
        data = {
            "code": 200,
            "message": "Publish False"
        }

    # 流信息发布 通道为'event'
    red = redis.StrictRedis(host='localhost', port=6379, db=6)
    red.publish(str(servicename), u'[Code:200 Message:Publish Begin]')
    time.sleep(10)
    red.publish(str(servicename), u'[Code:200 Message:Success] [Userid]:%s [Event]:%s [Data]:%s [Retry]:%s' % ("id",'event',"None",'None'))

    ret_json = json.dumps(data)
    #Response(ret_json, content_type='application/json')
    return ret_json
# 实时监听事件(yield)
def event_stream():
    red = redis.StrictRedis(host='localhost', port=6379, db=6)
    pubsub = red.pubsub()
    pubsub.subscribe('event')
    for message in pubsub.listen():
        yield 'data: %s\n\n' % message['data']
# sse数据接收接口
@app.route(MY_URL + 'sse_message/', methods=['GET', 'POST'])
def sse_message():
    # 流信息
    data = event_stream()
    print(data)
    return Response(data, mimetype="text/event-stream")

# 返回流式文件
@app.route(MY_URL + '/model_download/<filename>', methods=['POST', 'GET'])
def model_download(filename):
    # json 处理
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    token = data.get('token')
    servicename = data.get('servicename')

    # 判断数据库中同时有存在的username和servicename再返回图片
    data = verify_token(token)
    print(data)
    flag1 = mysql_sql.USER_INFO_find(data['username'])['flag']
    flag2 = mysql_sql.SERVICE_INFO_find(servicename=servicename)['flag']

    if flag1 and flag2:
        TorF = True

    if TorF:
        # 存放模型的文件夹名字 “download”
        DOWNLOAD_PATH = os.path.join(os.path.dirname(__file__), 'download')
        DOWNLOAD_PATH = os.path.join(DOWNLOAD_PATH,filename)
        print(DOWNLOAD_PATH)
        # json生成
        data = {
            "code": 200,
            "message": "Success",
        }

        # 流式读取
        def send_chunk():
            with open(DOWNLOAD_PATH, 'rb') as target_file:
                while True:
                    chunk = target_file.read(2 * 1024 * 1024)  # 每次读取2mb大小
                    if not chunk:
                        break
                    yield chunk
    else:
        data = {
            "code": 200,
            "message": "False"
        }

    ret_json = json.dumps(data)
    # 现在只返回图片
    return Response(send_chunk(), content_type='application/octet-stream')

"""策略设置与训练调用接口"""
@app.route(MY_URL + 'strategy_set/',methods=['GET','POST'])
def strategy_set():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))

    token = data.get('token')
    servicename = data.get('servicename')
    strategies = data.get('strategies') # 字典

    # 获取 token servicename 并校验 token
    try:
        data = verify_token(token)
    except Exception:
        abort(404)

    # 检查匹配
    TorF = mysql_sql.USER_INFO_find(data['username'])['flag']
    if TorF == str(True):
        # json生成
        data = {
            "code": 200,
            "message": "Token Verify = Success",
        }
    elif TorF == str(False):
        data = {
            "code": 400,
            "message": "Token Verify = False"
        }
    print(strategies)

    # GLOBAL_MODEL_INFO表更新 版本自己设置未更新
    mysql_sql.GLOBAL_MODEL_INFO_update1(servicename,"0.1",strategies['maxround'],strategies['aggregationtiming'],
                                  strategies['epsilon'],strategies['batchsize'],strategies['lr'])

    # 流信息发布 通道为'event'
    red = redis.StrictRedis(host='localhost', port=6379, db=6)
    red.publish('event', u'[Code:200 Message:Publish Begin]')
    time.sleep(10)
    red.publish('event', u'[Code:200 Message:Success] [Userid]:%s [Event]:%s [Data]:%s [Retry]:%s' % ("id",'event',"None",'None'))

    ret_json = json.dumps(data)
    #Response(ret_json, content_type='application/json')
    return ret_json

@app.route(MY_URL + 'task_visualize/', methods=['GET', 'POST'])
def task_visualize():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    token = data.get('token')

    try:
        data = verify_token(token)
    except Exception:
        abort(404)
    # 检查匹配

    TorF = mysql_sql.USER_INFO_find(data['username'])['flag']

    if TorF == str(True):
        service_info = mysql_sql.SERVICE_INFO_get()
        print(service_info)
        global_model_info = mysql_sql.GLOBAL_MODEL_INFO_get()
        print(global_model_info)
        length = len(service_info)

        def get_data(servicename: str, servicebrief: str, servicedetail: str, next: str, nextdata):
            # 下面几个参数分别是第3、4、6、7项
            maxround = mysql_sql.GLOBAL_MODEL_INFO_find(servicename)['data'][0][2]
            aggregationtiming = mysql_sql.GLOBAL_MODEL_INFO_find(servicename)['data'][0][3]
            batchsize= mysql_sql.GLOBAL_MODEL_INFO_find(servicename)['data'][0][5]
            lr= mysql_sql.GLOBAL_MODEL_INFO_find(servicename)['data'][0][6]
            return {
                "servicename": servicename,
                "servicebrief": servicebrief,
                "servicedetail": servicedetail,
                "strategies":{
                                "maxround":maxround,
                                "aggregationtiming":aggregationtiming,
                                "batchsize":batchsize,
                                "lr":lr
                },
                "next": next,
                "nextdata": nextdata
            }

        data = get_data(service_info[length - 1][0], service_info[length - 1][1], service_info[length - 1][2], "0",
                        "null")
        for i in range(length - 1):
            data = get_data(service_info[length - i - 2][0], service_info[length - i - 2][1],
                            service_info[length - i - 2][2], "1", data)

        # json生成
        data = {
            "code": 200,
            "message": "Success",
            "data": data
        }
    elif TorF == str(False):
        data = {
            "code": 200,
            "message": "False"
        }

    ret_json = json.dumps(data)
    return ret_json

"""信息列表相关功能"""
@app.route(MY_URL + 'info_visualize/', methods=['GET','POST'])
def info_visualize():

    data = request.get_data()
    data = json.loads(data.decode("utf-8"))

    # 获取 token 并校验 token
    try:
        token = data.get('token')
        data = verify_token(token)
    except Exception:
        abort(404)

    # 检查匹配
    TorF = mysql_sql.USER_INFO_find(data['username'])['flag']
    if TorF == str(True):
        # json生成
        data = {
            "code": 200,
            "message": "Publish Success",
        }
    elif TorF == str(False):
        data = {
            "code": 200,
            "message": "Publish False"
        }

    ret_json = json.dumps(data)
    return ret_json

@app.route(MY_URL + 'userpage_source/', methods=['GET','POST'])
def userpage_source():

    data = request.get_data()
    data = json.loads(data.decode("utf-8"))

    # 获取 token servicename 并校验 token
    try:
        token = data.get('token')
        data = verify_token(token)
    except Exception:
        abort(404)

    # 检查匹配
    TorF = mysql_sql.USER_INFO_find(data['username'])['flag']
    if TorF == str(True):
        # json生成
        data = {
            "code": 200,
            "message": "Publish Success",
            "username":str(data['username'])
        }
    elif TorF == str(False):
        data = {
            "code": 200,
            "message": "Publish False"
        }

    ret_json = json.dumps(data)
    return ret_json