# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from moviespider.items import *
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class Dy2018Spider(CrawlSpider):
    name = "dy2018"
    allowed_domains = ["dy2018.com"]
    start_urls = (
        'http://www.dy2018.com/html/gndy/dyzz/',
    )

    rules = (
        # 提取匹配 'category.php' (但不匹配 'subsection.php') 的链接并跟进链接(没有callback意味着follow默认为True)
        Rule(LinkExtractor(allow=('/index.*\.html', )),follow= True),

        # 提取匹配 'item.php' 的链接并使用spider的parse_item方法进行分析
        Rule(LinkExtractor(allow=('/i/\d+.html', )), callback='parse_item'),
    )

    def parse_item(self, response):
        sel = Selector(response)
        item = MovieInfo()


        item['title'] =  u''.join(sel.xpath('//div[contains(@class,"title_all")]/h1/text()').extract())

        if item['title'].find(u"《") > 0 and item['title'].find(u"》") > 0:
            startindex = item['title'].index(u"《")+1
            endindex = item['title'].index(u"》")
            item['name'] = item['title'][startindex:endindex]
        else:
            item['name'] = ''

        item['cate']  = code(sel.xpath('//div[contains(@class,"bd3l")]/a/text()').extract()[-1])

        item['img'] =  u''.join(sel.xpath('//div[contains(@id,"Zoom")]/p/img/@src').extract())
        item['link'] = u'\n'.join(sel.xpath('//td[@bgcolor]/a/text()').extract())

        #print '-'*50
        #print  startindex
        #print endindex
        #print item['name']
        # print u''.join(sel.xpath('//div[contains(@class,"title_all")]/h1/text()').extract())
        # print code(sel.xpath('//div[contains(@class,"bd3l")]/a/text()').extract()[-1])
        # print u''.join(sel.xpath('//div[contains(@id,"Zoom")]/p/img/@src').extract())
        # print u'\n'.join(sel.xpath('//td[@bgcolor]/a/text()').extract())
        #print '='*50
        return item

    def closed(self, reason):
        print("DoubanBookSpider Closed:" + reason)

def code(tmp):

    return eval("u'%s'"%tmp)