
# -*- coding:utf8 -*-
import requests
import hashlib
import xml.etree.cElementTree as ET
from xml2json import Xml2json as x2j
import json
from ct import *
import time
import requests


class WechatAPI():
    def __init__(self):
        self.appid = 'wxe589b00c17795e10'
        self.secret = '577a346208002399faf26896e6462f12'
        # 获取access token
        self.token = ''
        self.expires = 0

        pass

    def wechat_auth(self,request):
        token = 'xq123456' # your token
        query = request.args  # GET 方法附上的参数
        signature = query.get('signature', '')  # 微信加密签名
        timestamp = query.get('timestamp', '')  # 时间戳
        nonce = query.get('nonce', '')  # 随机数
        echostr = query.get('echostr', '') # 随机字符串
        s = [timestamp, nonce, token]
        # 1. 将token、timestamp、nonce三个参数进行字典序排序
        s.sort()
        # 2. 将三个参数字符串拼接成一个字符串进行sha1加密
        s = ''.join(s)
        # 3. 开发者获得加密后的字符串可与signature对比，标识该请求来源于微信
        key = hashlib.sha1(s).hexdigest()
        if (key == signature):
            print "验证成功"
            return echostr
        raise Exception("验证失败")


    def get_token(self):
        # 因为有调用限制,所以不要每次都取
        params = {'grant_type':'client_credential',
                  'appid':'wxe589b00c17795e10',
                  'secret':'577a346208002399faf26896e6462f12'}
        url = "https://api.weixin.qq.com/cgi-bin/token"

        if self.token == '':
            resp = self.get(url,params)
            self.token = resp['access_token']
            self.expires = resp['expires_in']
            print resp
        pass

    def check_error(ret,self):
        if ret.has_key('errcode'):
            raise Exception(ret)


    def get(self,url,params):
        r = requests.get(url,params=params)
        ret = json.loads(r.text)
        self.check_error(ret)
        return ret

    def recv_reply(self,data):
        action = recv_reply_action()
        action.pre(data)
        return action.reply()
        pass


# 用户处理用户的信息
class recv_reply_action():
    def __init__(self):
        self.xml_recv = ""
        pass

    def g(self,param):
        return self.xml_recv.find(param).text

    def pre(self,data):
        self.xml_recv = ET.fromstring(data)


    def reply(self):
        xdata = ''
        if self.g(MsgType) == text:
            # 回复文本,并且回复原文
            xdata = self._do_text_reply(self.g(Content))

        print "Reply %s "% xdata
        return xdata

# 根据type创建回复消息格式
    def _create_reply_xml(self,type):
        jdata =  ''
        if type == text:
            jdata = { 'xml':{
                ToUserName:self.g(FromUserName),
                FromUserName:self.g(ToUserName),
                CreateTime:str(int(time.time())),
                MsgType:text,
                Content:"<![CDATA[%s]]>",
                },
            }
            
        rdata = x2j().json2xml(jdata)
        rdata =rdata.replace('&lt;','<')
        rdata = rdata.replace('&gt;','>')

        return rdata

# 图灵机器人回复
    def _get_tuling_ans(self,context):
        url='http://www.tuling123.com/openapi/api'
        data={'key':'fa78fe2fbb85c914c7126d42bc7c3ebb','info':context,'userid':str(self.g(FromUserName))}
        r = requests.post(url,data=data)
        ans = json.loads(r.text)
        return ans['text']

# 回复Text
    def _do_text_reply(self,context):
        # 通过图灵得到回复
        context = self._get_tuling_ans(context)
        # 生成text类型的回复模版
        t = self._create_reply_xml(text)
        # 格式化消息
        t = t % context
        return  t


