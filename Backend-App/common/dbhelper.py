# -*- coding:utf8 -*-
import sqlite3


queries = {
    'SELECT': 'SELECT %s FROM %s WHERE %s',
    'SELECT_TOP':'SELECT * from %s ORDER BY %s DESC LIMIT 1',
    'SELECT_ALL': 'SELECT %s FROM %s',
    'INSERT_KEY': 'INSERT INTO %s (%s) VALUES (%s)',
    'INSERT': 'INSERT INTO %s VALUES (%s)',
    'UPDATE': 'UPDATE %s SET %s WHERE %s',
    'DELETE': 'DELETE FROM %s where %s',
    'DELETE_ALL': 'DELETE FROM %s',
    'CREATE_TABLE': 'CREATE TABLE IF NOT EXISTS %s(%s)',
    'DROP_TABLE': 'DROP TABLE %s'}


class DatabaseObject(object):

    def __init__(self, data_file):
        self.db = sqlite3.connect(data_file, check_same_thread=False)
        self.data_file = data_file

    def free(self, cursor):
        cursor.close()

    def write(self, query, values=None):
        cursor = self.db.cursor()
        if values is not None:
            cursor.execute(query, list(values))
        else:
            cursor.execute(query)
        self.db.commit()
        return cursor

    def read(self, query, values=None):
        cursor = self.db.cursor()
        if values is not None:
            cursor.execute(query, list(values))
        else:
            cursor.execute(query)
        return cursor

    def select(self, tables, *args, **kwargs):
        vals = ','.join([l for l in args])
        locs = ','.join(tables)
        conds = ' and '.join(['%s=?' % k for k in kwargs])
        subs = [kwargs[k] for k in kwargs]
        query = queries['SELECT'] % (vals, locs, conds)
        print query
        return self.read(query, subs)

    def select_query(self,tables,conds, *args):
        vals = ','.join([l for l in args])
        locs = ','.join(tables)
        query = queries['SELECT'] % (vals, locs, conds)
        print query
        return self.read(query)

    def select_top(self, tables, order_arg):
        locs = ','.join(tables)
        query = queries['SELECT_TOP'] % (locs,order_arg)
        return self.read(query).fetchall()[0][0]

    def select_all(self, tables, *args):
        vals = ','.join([l for l in args])
        locs = ','.join(tables)
        query = queries['SELECT_ALL'] % (vals, locs)
        return self.read(query)

    def insert(self, table_name, *args):
        values = ','.join(['?' for l in args])
        query = queries['INSERT'] % (table_name, values)
        print query
        return self.write(query, args)

    def insert_key(self, table_name, **kwargs):
        subs = ','.join([k for k in kwargs])
        vals = ','.join(["'%s'" % kwargs[k] for k in kwargs])
        query = queries['INSERT_KEY'] % (table_name, subs,vals)
        print query
        return self.write(query)

    def update(self, table_name, set_args, **kwargs):
        updates = ','.join(['%s=?' % k for k in set_args])
        conds = ' and '.join(['%s=?' % k for k in kwargs])
        vals = [set_args[k] for k in set_args]
        subs = [kwargs[k] for k in kwargs]
        query = queries['UPDATE'] % (table_name, updates, conds)
        print query
        return self.write(query, vals + subs)

    def delete(self, table_name, **kwargs):
        conds = ' and '.join(['%s=?' % k for k in kwargs])
        subs = [kwargs[k] for k in kwargs]
        query = queries['DELETE'] % (table_name, conds)
        return self.write(query, subs)

    def delete_all(self, table_name):
        query = queries['DELETE_ALL'] % table_name
        return self.write(query)

    def create_table(self, table_name, values):
        query = queries['CREATE_TABLE'] % (table_name, ','.join(values))
        self.free(self.write(query))

    def drop_table(self, table_name):
        query = queries['DROP_TABLE'] % table_name
        self.free(self.write(query))

    def disconnect(self):
        self.db.close()


class Table(DatabaseObject):


    def __init__(self, data_file, table_name, values):
        super(Table, self).__init__(data_file)
        self.create_table(table_name, values)
        self.table_name = table_name

    def exe(self,sql):
        return super(Table,self).read(sql)

    def select(self, *args, **kwargs):
        return super(Table, self).select([self.table_name], *args, **kwargs)

    def select_query(self,conds, *args):
        return super(Table, self).select_query([self.table_name],conds,*args)

    def select_top(self, order_arg):
        return super(Table,self).select_top([self.table_name],order_arg)


    def select_all(self, *args):
        return super(Table, self).select_all([self.table_name], *args)

    def insert(self, *args):
        return super(Table, self).insert(self.table_name, *args)

    def insert_key(self, **kwargs):
        return super(Table, self).insert_key(self.table_name, **kwargs)

    def update(self, set_args, **kwargs):
        return super(Table, self).update(self.table_name, set_args, **kwargs)

    def delete(self, **kwargs):
        return super(Table, self).delete(self.table_name, **kwargs)

    def delete_all(self):
        return super(Table, self).delete_all(self.table_name)

    def drop(self):
        return super(Table, self).drop_table(self.table_name)

# Sample
    # user = User('test.dat')
    # user.delete_all()
    # user.insert('ben', 'attal')
    # user.insert('hello', 'world')

    # user.update({password:xxx},username=aa)
    # user.select('*',username=aa)
    # cursor =  user.select_all('*')
    # print cursor.fetchall()
    # cursor.close()