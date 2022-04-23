# -*- coding:utf8 -*-
from common.config import *
from common.dbhelper import Table

DATABASE = getweixindb()

class User(Table):

    def __init__(self, data_file=DATABASE):
        super(User, self).__init__(data_file, 'users',
                                   ['id TEXT', 'name TEXT','createtime TEXT'])

    def select(self, *args, **kwargs):
        cursor = super(User, self).select(*args, **kwargs)
        results = cursor.fetchall()
        cursor.close()
        return results

    def insert(self, *args):
        self.free(super(User, self).insert(*args))

    def update(self, set_args, **kwargs):
        self.free(super(User, self).update(set_args, **kwargs))

    def delete(self, **kwargs):
        self.free(super(User, self).delete(**kwargs))

    def delete_all(self):
        self.free(super(User, self).delete_all())

    def drop(self):
        self.free(super(User, self).drop())

    def exists(self, id):
        results = self.select('*', id=id)
        return len(results) > 0

    def insert_user(self,*args):
        id = args[0]
        name = args[1]
        createtime = args[2]

        if self.exists(id):
            self.update({'name':name,'createtime':createtime},id=id)
        else:
            self.insert(*args)

class Photo(Table):

    def __init__(self, data_file=DATABASE):
        super(Photo, self).__init__(data_file, 'photo',
                                   ['mediaid TEXT', 'picurl TEXT','localpath TEXT','createtime TEXT','user TEXT'])

    def select(self, *args, **kwargs):
        cursor = super(Photo, self).select(*args, **kwargs)
        results = cursor.fetchall()
        cursor.close()
        return results

    def insert(self, *args):
        self.free(super(Photo, self).insert(*args))

    def update(self, set_args, **kwargs):
        self.free(super(Photo, self).update(set_args, **kwargs))

    def delete(self, **kwargs):
        self.free(super(Photo, self).delete(**kwargs))

    def delete_all(self):
        self.free(super(Photo, self).delete_all())

    def drop(self):
        self.free(super(Photo, self).drop())

    def exists(self, mediaid):
        results = self.select('*', mediaid=mediaid)
        return len(results) > 0

    def insert_photo(self,*args):
        mediaid = args[0]
        picurl = args[1]
        localpath = args[2]
        createtime = args[3]
        user = args[4]

        if self.exists(mediaid):
            self.update({'mediaid':mediaid,'picurl':picurl,'localpath':localpath,'createtime':createtime,'user':user},mediaid=mediaid)
        else:
            self.insert(*args)

