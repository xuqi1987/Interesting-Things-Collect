# -*- coding:utf8 -*-
import time
from flask import Flask,g,request,render_template,request,flash,url_for
from wechatAPI import Wechat

from helper import *
from common import  getweixin_port
weixin_app = Flask(__name__)
weixin_app.secret_key = 'some_secret'
api = Wechat()


@weixin_app.before_request
def before_request():
    pass


@weixin_app.teardown_request
def teardown_request(exception):
    pass

@weixin_app.route('/photolist/')
def getphotolist():
    return get_photolist()

@weixin_app.route('/', methods = ['GET', 'POST'])
def wechat():
    if request.method == 'GET':
        # 用于接入微信
        return api.check_signature(request)
    if request.method == 'POST':
        return api.response_msg(request)
@weixin_app.route('/test/')
def test():
    return make_response('hello')

def startweixin(port=getweixin_port()):
    print "启动微信服务 %s, 进程:%s" %(port,os.getpid())
    weixin_app.run(host='0.0.0.0', port=port)


