# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class MovieItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    publish_time = scrapy.Field()
    category = scrapy.Field()
    name = scrapy.Field()
    size = scrapy.Field()
    torrert_count = scrapy.Field()
    download_count = scrapy.Field()
    detail_link = scrapy.Field()
    pass

class MovieDetailItem(scrapy.Item):
    detail_link = scrapy.Field()
    download_link = scrapy.Field()
    magnet_link = scrapy.Field()
    pass
