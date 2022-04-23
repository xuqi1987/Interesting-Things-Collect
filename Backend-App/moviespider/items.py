# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item,Field

class MovieInfo(Item):
    title = Field()
    name = Field()
    cate = Field()
    rank = Field()
    actor = Field()
    updatetime = Field()
    img = Field()
    link = Field()
    url = Field()
    summary = Field()
    info = Field()

