# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class ScrapyDytt8MovieItem(scrapy.Item):
# define the fields for your item here like:
# name = scrapy.Field()
    name = Field()
    trans_name = Field()
    years = Field()
    country = Field()
    category  = Field()
    language  =  Field()
    words =  Field()
    IMDBscore = Field()
    fileformat =  Field()
    videosize =  Field()
    director =  Field()
    starring  = Field()
    pass

