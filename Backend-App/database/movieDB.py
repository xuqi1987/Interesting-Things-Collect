# -*- coding:utf8 -*-

from common.config import *
from common.dbhelper import Table

from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase


DATABASE = getmoviedb()

class MovieInfo_tb(Table):

    def __init__(self, data_file=DATABASE):
        super(MovieInfo_tb, self).__init__(data_file, 'movieinfo',
                                   ['ID INTEGER PRIMARY KEY AUTOINCREMENT', 'title TEXT','name TEXT','cate TEXT','rank TEXT','actor TEXT','updatetime TEXT','img TEXT','detaillink TEXT'])

    def select(self, *args, **kwargs):
        cursor = super(MovieInfo_tb, self).select(*args, **kwargs)
        results = cursor.fetchall()
        cursor.close()
        return results

    def insert(self, *args):
        self.free(super(MovieInfo_tb, self).insert(*args))

    def update(self, set_args, **kwargs):
        self.free(super(MovieInfo_tb, self).update(set_args, **kwargs))

    def delete(self, **kwargs):
        self.free(super(MovieInfo_tb, self).delete(**kwargs))

    def delete_all(self):
        self.free(super(MovieInfo_tb, self).delete_all())

    def drop(self):
        self.free(super(MovieInfo_tb, self).drop())

    def exists(self, id):
        results = self.select('*', id=id)
        return len(results) > 0


class DownloadLink_tb(Table):

    def __init__(self, data_file=DATABASE):
        super(DownloadLink_tb, self).__init__(data_file, 'links',
                                   ['ID INTEGER PRIMARY KEY AUTOINCREMENT', 'movieinfoid INTEGER NOT NULL','gid TEXT','status TEXT','sourceurl TEXT','downloadpath TEXT','playpath TEXT',' FOREIGN KEY (ID) REFERENCES movieinfo(ID)'])

    def select(self, *args, **kwargs):
        cursor = super(DownloadLink_tb, self).select(*args, **kwargs)
        results = cursor.fetchall()
        cursor.close()
        return results

    def insert(self, *args):
        self.free(super(DownloadLink_tb, self).insert(*args))

    def update(self, set_args, **kwargs):
        self.free(super(DownloadLink_tb, self).update(set_args, **kwargs))

    def delete(self, **kwargs):
        self.free(super(DownloadLink_tb, self).delete(**kwargs))

    def delete_all(self):
        self.free(super(DownloadLink_tb, self).delete_all())

    def drop(self):
        self.free(super(DownloadLink_tb, self).drop())

    def exists(self, id):
        results = self.select('*', id=id)
        return len(results) > 0

class MovieModule():

    def __init__(self):
        self.movieinfo = MovieInfo_tb()
        self.link = DownloadLink_tb()
        self.id = 0

    def insert_movieinfo(self,**kwargs):
        self.movieinfo.insert_key(**kwargs)
        self.id = self.movieinfo.select_top('ID')


    def insert_linkinfo(self,**kwargs):
        self.link.insert_key(movieinfoid=self.id,**kwargs)

    def select_all(self, *args):
        cursor =  self.movieinfo.select_all(args)
        result = cursor.fetchall()
        cursor.close()
        return result

    def search_name(self,key):
        sql = "select id,title,name,cate,img from movieinfo where name like '%" + key + "%';"
        cursor = self.movieinfo.exe(sql)
        result = cursor.fetchall()
        cursor.close()
        return result

    def search_title_exist(self,title):
        sql = "select * from movieinfo where title='" +title + "';"
        cursor = self.movieinfo.exe(sql)
        result = cursor.fetchall()
        cursor.close()
        return len(result) > 0

    def test(self):
        self.insert_movieinfo(title='a')
        self.insert_linkinfo(sourceurl='wwww.baidu.com')
        cursor =  self.movieinfo.select_all('*')
        print cursor.fetchall()
        cursor.close()


movie_database = SqliteDatabase(DATABASE)

def before_request_handler():
    movie_database.connect()

def after_request_handler():
    movie_database.close()


class BaseModel(Model):
    class Meta:
        database = movie_database

class links(BaseModel):
    id = IntegerField()
    movieinfoid = IntegerField()

    gid = TextField()
    status = TextField()
    sourceurl=TextField()
    downloadpath = TextField()
    playpath = TextField()


class movieinfo(BaseModel):
    id = IntegerField()
    title =TextField()

    name = TextField()
    cate = TextField()
    rank = TextField()
    actor = TextField()
    updatetime = TextField()
    img = TextField()