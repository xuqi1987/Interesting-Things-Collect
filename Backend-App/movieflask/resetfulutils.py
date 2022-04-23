# -*- coding:utf8 -*-
from aria2.pyaria2 import *
from database.datamodule import before_request_handler,after_request_handler,tb_movies,tb_links,tb_downloads
import urllib
import os
from common.tools import sync
import requests

def init_aria2():
    aria2 = PyAria2()
    return aria2

# 这个任务应该单独起个线程
def download_task(id,path='./data/download'):
    path = path+'/'+id + '/'

    # 1. 如果已经下载中(查找tb_downloads),有没有linkid == id的数据，如果已经在下载中，不进行任何操作
    if tb_downloads.select().where(tb_downloads.link == id).count() == 0:
        # 2. 没有在下载中，判断是否有文件夹，如果有，先删除，如果没有，创建文件夹 /data/download/id，
        if not os.path.exists(path):
            os.mkdir(path)
        # 3. 从tb_links表取得下载地址，然后判断下载地址的类型，常见的下载类型有torrent,http,ftp,
        for item in tb_links.select().where(tb_links.id == id):
            print u"开始下载:%s"%item.sourceurl
            sync(create_download_task,(id, path,item.sourceurl))
        pass

    else:
        pass


def create_download_task(id,path,url):

     # 4. 根据类型选择下载工具，如果是torrent,，使用aria2
    if url.endswith(".torrent"):
        aria2 = init_aria2()
        gid = aria2.addUri([url],position={"dir":path})
        # 5. 通过url下载电影，while循环定时查询下载结果，更新tb_downloads
        result = aria2.tellStatus(gid)
        # 6. 下载torrent成功
        while not result.has_key("followedBy"):
            time.sleep(1)
            result = aria2.tellStatus(gid)

        followedBy_gid =  result['followedBy'][0]

        result = aria2.tellStatus(followedBy_gid)
        print result
        # 7.开始下载视频
        while not (result['status'] == 'error' or result['status'] == 'complete'):
            time.sleep(1)
            result = aria2.tellStatus(followedBy_gid)
            print result
            if result.has_key('errorMessage'):
                query = tb_links.update(gid = followedBy_gid,status=result['status'],downloadpath=result['files'][0]['path'],errorMessage=result['errorMessage'],completedLength=result['completedLength'],totalLength= result['totalLength'],downloadSpeed=result['downloadSpeed']).where(tb_links.id == id)
                query.execute()

            else:
                query = tb_links.update(gid = followedBy_gid,status=result['status'],downloadpath=result['files'][0]['path'],completedLength=result['completedLength'],totalLength= result['totalLength'],downloadSpeed=result['downloadSpeed']).where(tb_links.id == id)
                query.execute()


    else:
        pass
    # 1. 如果已经下载中(查找tb_downloads),有没有linkid == id的数据，如果已经在下载中，不进行任何操作

    # 4. 根据类型选择下载工具，如果是torrent,或者http，使用aria2
    # 5. 通过url下载电影，while循环定时查询下载结果，更新tb_downloads
    # 6. 如果下载失败，删除重试，如果失败3次，则不再下载，更新tb_link表
    # 7. 如果下载成功，更新tb_link的下载地址，然后开始上传阿里，更新上传进度tb_download，如果上传结束，更新tb_link
    pass


def download_thread(id,path='/data/download'):
    aria2 = init_aria2()
    path = path+'/'+id
    if not os.path.exists(path):
        os.mkdir(path)

    data = [dic for dic in  tb_links.select().where(tb_links.id == id).dicts()]
    print data
    result = []
    if len(data) > 0:
        gid = data[0]['gid']

        if len(gid) == 0:
            print urllib.unquote(data[0]['sourceurl'].encode('UTF-8'))
            gid = aria2.addUri([urllib.unquote(data[0]['sourceurl'].encode('UTF-8'))],{"dir":path})
            result = aria2.tellStatus(gid)
        else:
            result = aria2.tellStatus(gid)
        print "-"*100
        print result
        print "-"*100
        query = tb_links.update(gid = gid,status=result['status'],downloadpath=result['files'][0]['path']).where(tb_links.id == id)
        query.execute()

        print result['status']
    return result
    pass


# print gid
#
# while True:
# 	result =  a.tellStatus(gid)
# 	print result
# 	print "speed:%(downloadSpeed)s \tstate:%(status)s\t %(completedLength)s | %(totalLength)s" % result
# 	time.sleep(1)


