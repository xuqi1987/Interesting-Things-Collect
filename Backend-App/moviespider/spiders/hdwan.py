# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from moviespider.items import *
import sys
import re
from douban import DoubanMovie
from scrapy import log

reload(sys)
sys.setdefaultencoding("utf-8")

class HdwanSpider(CrawlSpider):
    name = "hdwan"
    allowed_domains = ["hdwan.net"]
    start_urls = ['http://www.hdwan.net/']

    rules = (
        # 提取匹配 'category.php' (但不匹配 'subsection.php') 的链接并跟进链接(没有callback意味着follow默认为True)
        Rule(LinkExtractor(allow=('[a-zA-Z]*/page/\d+', ),deny=('/tag/.*','/wp-login\.php.*' )),follow= True),

        # 提取匹配 'item.php' 的链接并使用spider的parse_item方法进行分析
        Rule(LinkExtractor(allow=('\d+\.html', )), callback='parse_item'),
    )

    def parse_item(self, response):
        sel = Selector(response)
        item = MovieInfo()


        item['title'] =  u''.join(sel.xpath('//span[@class="current"]/text()').extract())
        item['name'] = self._get_name(sel)

        if len(sel.xpath('//a[@itemprop="breadcrumb"]/text()').extract()) > 1:
            item['cate']  = u''.join(sel.xpath('//a[@itemprop="breadcrumb"]/text()').extract()[1])
        else:
            item['cate'] = u''

        if len(sel.xpath('//div[@id="post_content"]/p/a/@href').extract()) > 0:
            item['img'] =  u''.join(sel.xpath('//div[@id="post_content"]/p/a/@href').extract()[0])
        else:
            item['img'] = u''


        item['link'] = u'\n'.join(sel.xpath('//div[contains(@class,"dw-box")]/a/@href').extract())

        item['url'] = response.url
        return item

    def closed(self, reason):
        log.WARNING("HdwanSpider Closed:" + reason)


    def _get_name(self,sel):
                # 过滤名字
        movie_name = u''.join(sel.xpath('//meta[@name="description"]/@content').extract()).replace(u"影片名：", u"")

        if movie_name.find(u"。") > 0:
            movie_name = u''.join(sel.xpath('//span[@class="current"]/text()').extract())

        if movie_name.find(u']') > 0:

            name = sel.xpath('//a[@id="post_content"]/h3/text()').extract()
            if len(name) > 0 and name[0].find(u'影片名：') > 0:
                movie_name = name[0].replace(u"影片名：", u"")

        if movie_name.find(u' ') >0:
            movie_name = movie_name.split(' ')[0]

        pattern = re.compile(r'\[')
        if pattern.search(movie_name) and movie_name.startswith(u'['):

            pattern1 = re.compile('\[([^\]]+)\]')
            movie_name = pattern1.findall(movie_name)[0]
        return movie_name




