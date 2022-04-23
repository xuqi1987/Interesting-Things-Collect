# -*- coding:utf8 -*-
import time
from flask import Flask,request, make_response
from wechatAPI import *

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'] )
def wechat():
    resp = make_response('')
    api = WechatAPI()
    try:
        if request.method == 'GET':
            # 用于接入微信
            resp = make_response(api.wechat_auth(request))
        else:
            # 取的access token
            # api.get_token();

            # 被动回复用户消息
            replydata = api.recv_reply(request.data)

            resp = make_response(replydata)
            resp.content_type = 'application/xml'
    except Exception as e:
        resp =  make_response(e.message)
    finally:
        return resp

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=80)