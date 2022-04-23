# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
import re
from Scrapy_Movie.items import *

class Dytt8Spider(scrapy.Spider):
    name = 'dytt8'
    allowed_domains = ['www.dytt8.net']
    start_urls = ['http://www.dytt8.net/html/gndy/dyzz/index.html']

    def parse(self, response):

        root_sel = Selector(response)

        for table in root_sel.xpath("//table"):
            for title in table.xpath("//a[@class='ulink']/text()").extract():
                #print title.encode('utf-8')
                pass

            for link in table.xpath("//a[@class='ulink']/@href").extract():
                yield scrapy.Request("http://www.dytt8.net"+ link, callback=self.parse_detail)

        for page_link in root_sel.xpath('//select[@name="sldd"]/option/@value').extract():
            yield scrapy.Request("http://www.dytt8.net/html/gndy/dyzz/" + page_link, callback=self.parse)
            pass

    def parse_detail(self,response):
        root_sel = Selector(response)
        title =  root_sel.xpath('//div[@class="title_all"]/h1/font/text()').extract()[0].encode('utf-8')

        detail_text = ''.join([item.extract().encode('utf-8') for item in root_sel.xpath('//div[@id="Zoom"]//span/text()')])
        movie_item = ScrapyDytt8MovieItem()


        movie_item['name'] =  self.match_detail_item(detail_text,r'◎片　　名　(.+)')
        movie_item['ans_name'] = self.match_detail_item(detail_text,r'◎译　　名　(.+)')
        movie_item['yes'] = self.match_detail_item(detail_text,r'◎年　　代　(.+)')
        movie_item['couny'] =  self.match_detail_item(detail_text,r'◎国　　家　(.+)')
        movie_item['catery'] = self.match_detail_item(detail_text,r'◎类　　别　(.+)')
        movie_item['nguage'] =  self.match_detail_item(detail_text,r'◎语　　言　(.+)')
        movie_item['word'] =  self.match_detail_item(detail_text,r'◎字　　幕　(.+)')
        movie_item['IMDBsre'] = self.match_detail_item(detail_text,r'◎IMDB评分 (.+)')
        movie_item['filermat'] =  self.match_detail_item(detail_text,r'◎文件格式　(.+)')
        movie_item['vidsize'] =  self.match_detail_item(detail_text,r'◎视频尺寸　(.+)')
        movie_item['direor'] =  self.match_detail_item(detail_text,r'◎导　　演　(.+)')
        movie_item['starring'] = self.match_detail_item(detail_text,r'◎主　　演　(.+)')

        print movie_item

    def match_detail_item(self,text,reg):
          matchObj  = re.match(reg, text, re.M|re.I)
          if matchObj:
              return  matchObj.group(1)