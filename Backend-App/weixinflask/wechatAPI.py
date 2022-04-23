
# -*- coding:utf8 -*-
import hashlib
import xml.etree.cElementTree as ET

from helper import *

LOG_FILENAME="webcharAPI.log"
logging.basicConfig(filename=LOG_FILENAME,level=logging.NOTSET)

class Wechat():
    def __init__(self):
        self.appid = 'wxe589b00c17795e10'
        self.secret = '577a346208002399faf26896e6462f12'
        # 获取access token
        self.token = ''
        self.expires = 0
        pass

    def check_signature(self,request):
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
            logging.debug("验证成功")
            return make_response(echostr)
        else:
            logging.error("验证失败")
            return make_response('')


    def response_msg(self,request):
        msg = self.parse_msg(request)
        sync(add_user,msg)
        if msg['MsgType'] == 'text':
            return judge_text(msg)
        elif msg['MsgType'] == 'event':
            return judge_event(msg)
        elif msg['MsgType'] == 'image':
            return judge_image(msg)
        else:
            return donot_know(msg)

        # elif msg['MsgType'] == 'music':
        #     response_content = dict(content = judge_text(msg),
        #     touser = msg['FromUserName'],
        #     fromuser = msg['ToUserName'],
        #     createtime = str(int(time.time())),)
        #     return music_reply.format(**response_content)
        #
        # elif msg['MsgType'] == 'event':
        #     return judge_event(msg)
        #
        # elif msg['MsgType'] == 'location':
        #     return judge_location(msg)
        # elif msg['MsgType'] == 'voice':
        #     return judge_voice(msg)

    def parse_msg(self,request):
        """此函数用于解析XML文档，确定XML的类型"""
        msg ={}
        xlm_tree = request.data
        root= ET.fromstring(xlm_tree)
        for child in root:
            msg[child.tag] = to_unicode(child.text)
        return msg


    def get_token(self):
        # 因为有调用限制,所以不要每次都取
        params = {'grant_type':'client_credential',
                  'appid':'wxe589b00c17795e10',
                  'secret':'577a346208002399faf26896e6462f12'}
        url = "https://api.weixinflask.qq.com/cgi-bin/token"

        if self.token == '':
            resp = self.get(url,params)
            self.token = resp['access_token']
            self.expires = int(resp['expires_in']) +time.time()
            print resp
        pass

        return self.token

    # def get_material_list(self):
    #     url = "https://api.weixin.qq.com/cgi-bin/material/batchget_material"
    #     data = {'type':"image",
    #               'offset':0,
    #               'count':20}
    #     param = {'access_token':self.get_token()}
    #     resp = self.post(url,params=param, data=json.dumps(data))
    #
    #     print resp
    #
    #     pass
    #
    # def check_error(self,ret):
    #     if ret.has_key('errcode'):
    #         raise Exception(ret)
    #
    # def get(self,url,params):
    #     r = requests.get(url,params=params)
    #     ret = json.loads(r.text)
    #     self.check_error(ret)
    #     return ret
    #
    # def post(self,url,params,data):
    #     r = requests.post(url,params=params,data=data)
    #     ret = json.loads(r.text)
    #     self.check_error(ret)
    #     return ret
    #
    # def recv_reply(self,data):
    #     action = Recv_reply_action(data)
    #
    #     return action.reply()
    #     pass
    #



