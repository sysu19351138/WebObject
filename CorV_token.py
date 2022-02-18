# 导入依赖包
from flask import request,jsonify,current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

def create_token(username):
    # 输入：username
    # 输出：token

    # 第一个参数是内部的私钥，这里写在共用的配置信息里了，如果只是测试可以写死
    # 第二个参数是有效期(秒)
    # 密钥也可以自己乱编
    key = Serializer('abcdefghijklmm', expires_in=3600)

    # 接收用户id转换与编码
    token = key.dumps({"username": username}).decode("ascii")
    return token

def verify_token(token):
    # 输入：token
    # 输出：username

    # 密钥是自己乱编
    key = Serializer('abcdefghijklmm')
    try:
        # 转换为字典 {'username': '18811891816'}
        data = key.loads(token)
        print(data)
    except Exception:
        return False
    return data