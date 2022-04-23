# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from database.movieDB import MovieModule
from scrapy.exceptions import DropItem
from database.datamodule import tb_movies,tb_links,tb_doubans
from douban import DoubanMovie
from celery_app.task_movie import download_upload_image,upload_image
from oss.oss import OssSDK
import requests
import random
import datetime

class MoviePipeline(object):

    def __init__(self):

        self.oss = OssSDK('x2020-movieflask')
        self.douban = DoubanMovie()
        self.count = 0
        pass

    def process_item(self, item, spider):

        for key in item:
            item[key] = item[key].replace("'","")

        if (item['cate'].find(u'综艺') < 0 ) and len(item['link']) > 0  and len(item['title']) > 0:

            self.count = self.count + 1
            print '[%s]:%s  %s  %s'%(self.count,item['name'],item['title'],item['cate'])
            print item['img']
            print item['link']


            # 如果没有重复
            if tb_movies.select().where(tb_movies.title==item['title']).count() == 0:

                if len(item['img']) > 0:

                    # r = requests.get(item['img'])
                    # if r.status_code == 200:
                    #     upload_image.delay(r.content,item['title'])
                    #     print "\n"
                    # else:
                    #print "图片下载,10秒后尝试重新下载 : %s\n"%item['img']

                    download_upload_image.apply_async(args=(item['img'],item['title']),countdown=random.randint(1, 10))

                    # 下载图片
                    pass

                # 插入数据库
                tb_movies.insert(title=item['title'],cate=item['cate'],img=item['img'],name=item['name'],org_url=item['url'],updatetime=datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")).execute()

                # 更新链接
                id = tb_movies.get(tb_movies.title==item['title']).id
                for link in item['link'].split('\n'):
                    tb_links.insert(movie=id,sourceurl=link).execute()

                # search douban by name
                i = self.douban.searchMovie(item['name'])
                if i.has_key('url'):
                    data = self.douban.detailInfo(i['url'])
                    # get detial info
                    if data.has_key('title'):
                        # 将电影保存到豆瓣数据库中
                        tb_doubans.insert(movie=id,title=data['title'],year=data['year'],douban_url=data['alt'],rating=data['rating'],directors=data['directors'],genres=data['genres'],pubdates=data['pubdates'],rating_betterthan=data['rating_betterthan'],summary=data['summary'],info=data['info']).execute()
                return item
            else:
                DropItem(u"重复项: %s" % item['title'])
        else:
            DropItem(u"无效项: %s" % item['title'])


    def download_img(self,url):
        pass