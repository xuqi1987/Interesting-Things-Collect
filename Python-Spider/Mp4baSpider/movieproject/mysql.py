#!/usr/bin/python
#coding=utf-8
#

import pymysql

class MySqlHelp(object):
    def __init__(self):
        self.dbName='movie'
        self.createTbSql = u'''CREATE TABLE IF NOT EXISTS tb_movieitem (
                                        id int(10) unsigned NOT NULL AUTO_INCREMENT,
                                        publish_time varchar(10) NOT NULL DEFAULT '',
                                        category varchar(40) NOT NULL DEFAULT '',
                                        name varchar(80) NOT NULL DEFAULT '',
                                        size varchar(10)  DEFAULT '',
                                        torrert_count varchar(10)  DEFAULT '',
                                        download_count varchar(10)  DEFAULT '',
                                        detail_link varchar(20) NOT NULL DEFAULT '',    
                                        PRIMARY KEY (id)
                                        );
                                        '''
        try:
            self.open()
            self.cur.execute(self.createTbSql)

        except pymysql.Error,e:
            print u"Mysql Error %d: %s" % (e.args[0], e.args[1])

        finally:
            self.close()
        pass

    def open(self):
        self.conn=pymysql.connect(host='localhost',user='root',passwd='Xq123456',port=3306,charset="utf8")
        self.cur=self.conn.cursor()
        self.cur.execute("create database if not exists %s character set utf8;" % self.dbName)  
        self.conn.select_db(self.dbName)
        pass

    def close(self):
        self.cur.close()
        self.conn.close()
        self.conn = None
        self.cur = None
        pass


    def insert(self,value):
        sql = u"INSERT INTO tb_movieitem (publish_time, category,name,size,torrert_count,download_count,detail_link) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        try:
            self.open()

            item = []
            item.append(value['publish_time'].encode('UTF-8'))
            item.append(value['category'].encode('UTF-8'))
            item.append(value['name'].encode('UTF-8'))
            item.append(value['size'].encode('UTF-8'))
            item.append(value['torrert_count'].encode('UTF-8'))
            item.append(value['download_count'].encode('UTF-8'))
            item.append(value['detail_link'].encode('UTF-8'))
            self.cur.execute(sql,item)
            self.conn.commit()

        except pymysql.Error,e:
            print u"Mysql Error %d: %s" % (e.args[0], e.args[1])
        finally:
            self.close()
        pass
