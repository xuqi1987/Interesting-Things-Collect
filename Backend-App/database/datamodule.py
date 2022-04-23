# -* - coding: UTF-8 -* -
from common.config import *

import datetime
from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase
import redis

DATABASE = getmoviedb()

database_object = SqliteDatabase(DATABASE)



def create_init_table():
    database_object.create_table(tb_links,safe=True)
    database_object.create_table(tb_movies,safe=True)
    database_object.create_table(tb_doubans,safe=True)
    database_object.create_table(tb_downloads,safe=True)
    database_object.create_table(tb_test,safe=True)

def before_request_handler():
    database_object.connect()

def after_request_handler():
    database_object.close()

class BaseModel(Model):
    class Meta:
        database = database_object


class tb_movies(BaseModel):
    id = IntegerField(primary_key=True)
    org_url = TextField(default=u'')
    title =TextField(default=u'')
    name = TextField(default=u'')
    cate = TextField(default=u'')
    updatetime = TextField(default=datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S"))
    img = TextField(default=u'')
    #douban = ForeignKeyField(tb_doubans,related_name='douban')

class tb_subscript(BaseModel):
    id = IntegerField(primary_key=True)

class tb_doubans(BaseModel):
    id = IntegerField(primary_key=True)
    title = TextField(default=u'')
    #original_title = TextField(default=u'')
    douban_url = TextField(default=u'')
    rating = TextField(default=u'')
    directors = TextField(default=u'')
    genres = TextField(default=u'')
    pubdates = TextField(default=u'')
    year = TextField(default=u'')
    rating_betterthan = TextField(default=u'')
    summary = TextField(default=u'')
    info = TextField(default=u'')
    movie = ForeignKeyField(tb_movies)



class tb_links(BaseModel):
    id = IntegerField(primary_key=True)
    movie = ForeignKeyField(tb_movies)

    gid = TextField(default=u'')
    status = TextField(default=u'')
    sourceurl=TextField(default=u'')
    downloadpath = TextField(default=u'')
    playpath = TextField(default=u'')
    dir = TextField(default=u'')
    completedLength = TextField(default=u'')
    downloadSpeed =TextField(default=u'')
    errorMessage = TextField(default=u'')
    totalLength = TextField(default=u'')

class tb_downloads(BaseModel):
    id = IntegerField(primary_key=True)
    link = ForeignKeyField(tb_links)

class tb_test(BaseModel):
    id = IntegerField(primary_key=True)
    name = TextField(default=u'')

# Redis DataBase 设计
# key 表名:主键值:列名

class db_Movie():
    def __init__(self):
        self.r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
        self.tb_movies = 'tb_movies'
    # 字符串
    # table:count value
    # table:id:列名 value
    # table:value id
    def _id(self,tb_name):
        if self.r.exists('%s:count' % tb_name):
            self.r.incr('%s:count' % tb_name)
        else:
            self.r.set('%s:count' % tb_name,0)

        return self.r.get('%s:count' % tb_name)

    def insert_tb_movies(self,**kwargs):

        id = self._id(self.tb_movies)

        for key in kwargs:
            self.r.set('%s:%s:%s'%(self.tb_movies,id,key),kwargs[key])
            if key == "title":
                self.r.zadd('%s:%s' %(self.tb_movies,kwargs[key]),id)
                pass
            pass
        else:
            pass
        pass


    def exist_tb_movies(self,title):
        return  self.r.sismember('%s:%s'%(self.tb_movies,'title'),title)




