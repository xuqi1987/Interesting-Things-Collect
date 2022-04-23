# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from movieproject.mysql import MySqlHelp

class MovieSavePipeline(object):
    def __init__(self):
        self.linecount = 0
        self.db = MySqlHelp()

    def process_item(self, item, spider):
        self.linecount  = self.linecount +1

        if item.has_key('name'):
            #print item.values
            self.db.insert(item)
        else:
            print item['download_link']
        return item
