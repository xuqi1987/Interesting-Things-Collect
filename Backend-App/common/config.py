# -* - coding: UTF-8 -* -
import ConfigParser
import os
#生成config对象
conf = ConfigParser.ConfigParser()
print '-'*40
print os.getcwd()
if os.path.exists("common/conf.cfg"):
    #用config对象读取配置文件
    conf.read("common/conf.cfg")
else:
    print os.getcwd()
    print "file not find"

def getweixindb():
    print "getweixindb: " + getrootpath('weixinflask') + conf.get('weixinflask','database')
    return getrootpath('weixinflask') + conf.get('weixinflask','database')

def getphoto():
    return getrootpath('weixinflask') + conf.get('weixinflask','photo')

def getthumbnail():
    return getrootpath('weixinflask')+ conf.get('weixinflask','thumbnail')

def getmoviedb():
    print "getmoviedb : "  +  getrootpath('movieflask') + conf.get('movieflask','database')
    return getrootpath('movieflask') + conf.get('movieflask','database')


def getrootpath(section):
    if os.path.exists(conf.get(section,'root')):
        return conf.get(section,'root')
    else:
        return './'

def getmovie_port():
    return conf.get('movieflask','port')

def getweixin_port():
    return conf.get('weixinflask','port')

def getceleryip():
    return conf.get('common','celeryip')
def getceleryport():
    return conf.get('common','celeryport')
#以列表形式返回所有的section
#sections = conf.sections()
# #得到指定section的所有option
# options = conf.options("sec_a")
# print 'options:', options           #options: ['a_key1', 'a_key2']
# #得到指定section的所有键值对
# kvs = conf.items("sec_a")
# print 'sec_a:', kvs                 #sec_a: [('a_key1', '20'), ('a_key2', '10')]
# #指定section，option读取值
# str_val = conf.get("sec_a", "a_key1")
# int_val = conf.getint("sec_a", "a_key2")
#
# print "value for sec_a's a_key1:", str_val   #value for sec_a's a_key1: 20
# print "value for sec_a's a_key2:", int_val   #value for sec_a's a_key2: 10
#
# #写配置文件
# #更新指定section，option的值
# conf.set("sec_b", "b_key3", "new-$r")
# #写入指定section增加新option和值
# conf.set("sec_b", "b_newkey", "new-value")
# #增加新的section
# conf.add_section('a_new_section')
# conf.set('a_new_section', 'new_key', 'new_value')
# #写回配置文件
# conf.write(open("test.cfg", "w"))