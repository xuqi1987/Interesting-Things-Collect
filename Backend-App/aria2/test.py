# -*- coding: utf-8 -*-
import codecs
from pyaria2 import PyAria2
import time
import urllib
a = PyAria2()
#print a.getGlobalOption()
url = 'ftp://a:a@dygod18.com:21/[电影天堂www.dy2018.com]海底总动员2：多莉去哪儿HD国英双语中字.mkv'
url_unquote = urllib.unquote(u'ftp://a:a@dygod18.com:21/[电影天堂www.dy2018.com]海底总动员2：多莉去哪儿HD国英双语中字.mkv')
# url_gbk = decode(url, "gbk")
url_utf8 = url.decode("utf-8")
url_gbk = url_utf8
print url_gbk

#url_quote = urllib.quote(url_utf8)

import urllib2, json
jsonreq = json.dumps({'jsonrpc':'2.0', 'id':'qwer','method':'aria2.addUri','params':[[url_utf8]]})
c = urllib2.urlopen('http://localhost:6800/jsonrpc', jsonreq)
print c.read()
#	print gid[0]

#gid = a.addUri([url_quote],{"dir":"/data/downloads"})

#print gid

while True:
	result =  a.tellStatus(gid)
	print result
	print "speed:%(downloadSpeed)s \tstate:%(status)s\t %(completedLength)s | %(totalLength)s" % result
	time.sleep(1)