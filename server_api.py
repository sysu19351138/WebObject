from flask import Flask, jsonify,abort, make_response
from flask import request,Response
from CorV_token import create_token,verify_token
import json
import redis
import mysql_sql


app = Flask(__name__)
MY_URL = '/api/'

# get
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

###############################################
# 404处理
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

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
    TorF = mysql_sql.USER_INFO_find(data['username'])
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

# 用以校验token 并发布流信息
@app.route(MY_URL + 'service_request/', methods=['GET','POST'])
def service_request():

    data = request.get_data()
    data = json.loads(data.decode("utf-8"))

    # 获取 token servicename 并校验 token
    try:
        token = data.get('token')
        data = verify_token(token)
        servicename = data.get('servicename')
    except Exception:
        abort(404)

    # 检查匹配
    TorF = mysql_sql.USER_INFO_find(data['username'])
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
    red.publish('event', u'[Code:200 Message:Success] [Userid]:%s [Event]:%s [Data]:%s [Retry]:%s' % ("id",'event',"None",'None'))

    ret_json = json.dumps(data)
    return ret_json

# 实时监听事件(yield)
def event_stream():
    red = redis.StrictRedis(host='localhost', port=6379, db=6)
    pubsub = red.pubsub()
    pubsub.subscribe('event')
    for message in pubsub.listen():
        yield 'data: %s\n\n' % message['data']

# 以下用以测试
@app.route(MY_URL + 'service_test/', methods=['GET','POST'])
def service_test():
    # 流信息
    data = event_stream()
    print(data)
    return Response(data,mimetype="text/event-stream")

# 信息发布
@app.route(MY_URL + 'service_public/', methods=['GET','POST'])
def service_public():
    # 信息发布
    red = redis.StrictRedis(host='localhost', port=6379, db=6)
    red.publish('event', u'[Code:200 Message:Success] [Userid]:%s [Event]:%s [Data]:%s [Retry]:%s' % ("id",'event',"None",'None'))
    #red.publish('event', u'[%s]:%s %s' % ("Userid",'event','data','retry'))
    return Response(status=204)

# 测试用的URL 可不理
@app.route(MY_URL + 'Test/')
def home():
    return u"""
        <!doctype html>
        <title>chat</title>
        <script src="http://cdn.staticfile.org/jquery/2.1.1/jquery.min.js"></script>
        <style>body { max-width: 500px; margin: auto; padding: 1em; background: black; color: #fff; font: 16px/1.6 menlo, monospace; }</style>
        </p><button id="time">Click for time!</button>
        <pre id="out"></pre>
        <script>
            function sse() {
                var source = new EventSource('/api/service_test?channel=event');
                var out = document.getElementById('out');
                source.onmessage = function(e) {
                    out.innerHTML = 'now-tiem:'+ e.data + '\\n' + out.innerHTML;
                };
            }
            $('#time').click(function(){
                    $.post('/api/service_public');
                }
            );
            sse();
        </script>
    """








