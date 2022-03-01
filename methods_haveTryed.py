'''
这里面是一些感觉有用的demo 可不理
'''
'''
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
'''

'''
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
'''