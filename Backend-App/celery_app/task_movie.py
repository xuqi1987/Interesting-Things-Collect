# -*- coding: utf-8 -*-

import time
from celery_app import app
from common.tools import *
from oss.oss import OssSDK
from database.datamodule import *

@app.task
def scrapy_movie(spider):
    print "start scrapy movie"
    Run("scrapy crawl %s"%(spider))
    pass

@app.task
def download_upload_image(url,title):
    oss = OssSDK('x2020-movie')
    new_url = oss.put_url_auto_name(url)
    #print "download_upload_image : [%s] :%s" % (title,new_url)
    if new_url == url:
        print u"[Error]:重新下载图片失败 url=%s\n"% url
    else:
        print u"图片重新下载成功 : %s %s\n" %(title,url)
        tb_movies.update(img=new_url).where(tb_movies.title==title).execute()
    pass

@app.task
def upload_image(content,title):
    oss = OssSDK('x2020-movie')
    new_url = oss.put_content_auto_name(content)
    #print "upload_image : [%s] :%s" % (title,new_url)
    print u"图片上传成功 : %s\n" %(new_url)
    tb_movies.update(img=new_url).where(tb_movies.title==title).execute()
    pass

@app.task
def test(x,y):
    print "hello"
    pass