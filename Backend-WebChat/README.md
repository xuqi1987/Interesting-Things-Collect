#weixin

**参考：**

[http://blog.csdn.net/linhan8/article/details/8746110]()

要通过微信配置，必须先服务器端配置好


## 第一步 服务器端配置

服务器接入指南：

[http://mp.weixin.qq.com/wiki/8/f9a0b8382e0b77d87b3bcc1ce6fbc104.html]()

开发者提交信息后，微信服务器将发送GET请求到填写的服务器地址URL上，GET请求携带四个参数：

参数	|	描述
------------- | -------------
signature	| 微信加密签名，signature结合了开发者填写的token参数和请求中的timestamp参数、nonce参数。
timestamp	 | 时间戳
nonce	| 随机数
echostr	| 随机字符串


开发者通过检验signature对请求进行校验（下面有校验方式）。若确认此次GET请求来自微信服务器，请原样返回echostr参数内容，则接入生效，成为开发者成功，否则接入失败。

```
加密/校验流程如下：
1. 将token、timestamp、nonce三个参数进行字典序排序
2. 将三个参数字符串拼接成一个字符串进行sha1加密
3. 开发者获得加密后的字符串可与signature对比，标识该请求来源于微信

```

```
# -*- coding:utf8 -*-
import time
from flask import Flask,request, make_response
import hashlib

app = Flask(__name__)

@app.route('/wechat', methods = ['GET', 'POST'] )
def wechat_auth():

    if request.method == 'GET':
        token = 'xq123456' # your token
        query = request.args  # GET 方法附上的参数
        signature = query.get('signature', '')
        timestamp = query.get('timestamp', '')
        nonce = query.get('nonce', '')
        echostr = query.get('echostr', '')
        s = [timestamp, nonce, token]
        # 1. 将token、timestamp、nonce三个参数进行字典序排序
        s.sort()
        # 2. 将三个参数字符串拼接成一个字符串进行sha1加密
        s = ''.join(s)
        # 3. 开发者获得加密后的字符串可与signature对比，标识该请求来源于微信
        key = hashlib.sha1(s).hexdigest()
        if (key == signature):
            return make_response(echostr)
```

**遇到小问题**

因为域名没有备案，所以无法通过域名设置，只能设置ip。

## 第二步 网页端配置

网页端提交后：

![](http://cl.ly/3H34353N1c1f/Image%202016-03-17%20at%2012.17.38%20%E4%B8%8A%E5%8D%88.png)


## 第三步 接收普通消息
当普通微信用户向公众账号发消息时，微信服务器将POST消息的XML数据包到开发者填写的URL上。

假如服务器无法保证在五秒内处理并回复，可以直接回复空串，微信服务器不会对此作任何处理，并且不会发起重试。

消息类型：

- 文本消息
- 图片消息
- 语音消息
- 视频消息
- 小视频消息
- 地理位置消息
- 链接消息


### 文本消息
```
<xml>
 <ToUserName><![CDATA[toUser]]></ToUserName>
 <FromUserName><![CDATA[fromUser]]></FromUserName> 
 <CreateTime>1348831860</CreateTime>
 <MsgType><![CDATA[text]]></MsgType>
 <Content><![CDATA[this is a test]]></Content>
 <MsgId>1234567890123456</MsgId>
 </xml>
```

参数 | 描述
---|---
ToUserName	|开发者微信号
FromUserName	|发送方帐号（一个OpenID）
CreateTime|	消息创建时间 （整型）
MsgType	|text
Content	|文本消息内容
MsgId|	消息id，64位整型


## 第四步 被动回复消息

被动回复消息，消息的类型有很多种，先从简单的文本开始。

用户收到“该公众号暂时无法提供服务，请稍后再试”：原因：

+ 开发者在5秒内未回复任何内容
+ 开发者回复了异常数据，比如JSON数据等

### 回复文本消息

```
<xml>
<ToUserName><![CDATA[toUser]]></ToUserName>
<FromUserName><![CDATA[fromUser]]></FromUserName>
<CreateTime>12345678</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[你好]]></Content>
</xml>
```

参数	| 是否必须	 | 描述
----|----|----
ToUserName|是|	接收方帐号（收到的OpenID）
FromUserName|	是|	开发者微信号
CreateTime|	是	|消息创建时间 （整型）
MsgType|	是|	text
Content|	是	|回复的消息内容（换行：在content中能够换行，微信客户端就支持换行显示）


虽然消息内容不一致，但是都是xml格式，所以需要有辅助处理xml格式的函数

修改
[https://github.com/hay/xml2json/blob/master/xml2json.py
]()

主要修改是将这些方法封装成类，然后删除一些函数的参数，例如以下的options.

```
	def elem2json(elem, options, strip_ns=1, strip=1):

```

测试代码：

``` 
from xml2json import *

x = Xml2json()
xml = '''<xml>
 <ToUserName><![CDATA[toUser]]></ToUserName>
 <FromUserName><![CDATA[fromUser]]></FromUserName>
 <CreateTime>1348831860</CreateTime>
 <MsgType><![CDATA[text]]></MsgType>
 <Content><![CDATA[this is a test]]></Content>
 <MsgId>1234567890123456</MsgId>
 </xml>'''
j = x.xml2json(xml)

print j

a = x.json2xml(j)

print a
```

输出：

```
test.py
{
    "xml": {
        "Content": "this is a test",
        "CreateTime": "1348831860",
        "FromUserName": "fromUser",
        "MsgId": "1234567890123456",
        "MsgType": "text",
        "ToUserName": "toUser"
    }
}
<xml><FromUserName>fromUser</FromUserName><MsgId>1234567890123456</MsgId><ToUserName>toUser</ToUserName><Content>this is a test</Content><MsgType>text</MsgType><CreateTime>1348831860</CreateTime></xml>

```

与微信的格式对比后，发现json2xml这个函数没办法满足需求。可以看到转换前有CDATA，转换后就没有了。

**Tips:**
>操作XML文件时，如果允许用户输入内容，例如∶"< "、">"、"/"、""等，当生成XML时，会破坏了XML结构，使数据中断。
>这就要用XML CDATA
>在XML文档中的所有文本都会被解析器解析。
>只有在CDATA部件之内的文本会被解析器忽略。


找了半天，发现有帮助的文档只有：
[http://stackoverflow.com/questions/174890/how-to-output-cdata-using-elementtree
]()

这里介绍的解决方法就是重写_write方法，然后在_write方法中，判断是否是自定义的标签，如果是的，返回自定义的格式。
但是我重写了这个方法后，发现父类没有这个方法。所以这个解决办法不可用。




