# -*- coding: utf-8 -*-
from movieproject.items import MovieItem,MovieDetailItem
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

class Mp4baSpider(CrawlSpider):
    name = "mp4ba"
    allowed_domains = ["mp4ba.com"]
    start_urls = (
        u'http://www.mp4ba.com/',
    )

    rules = (
        Rule(LinkExtractor(allow=r'\index.php\?(.)*page=(\d)*'), callback='parse_page', follow=True),
        
        Rule(LinkExtractor(allow=r'show.php\?hash=(.)*'), callback='parse_detail', follow=False),
    )

    def parse_page(self, response):
        items = []
        for  data in response.xpath("//tbody[@id='data_list']/tr[@class='alt1']"):
            item = MovieItem()
            item['publish_time'] =  u''.join(data.xpath("td[1]/text()").extract())
            item['category'] = u''.join(data.xpath("td[2]/a[@href]/text()").extract())
            item['name'] = u''.join(data.xpath("td[3]/a[@href]/text()").extract()).strip()
            item['size'] = u''.join(data.xpath("td[4]/text()").extract())
            item['download_count'] = u''.join(data.xpath("td[@nowrap]/span[@class='btl_1']/text()").extract())
            item['detail_link'] = u''.join(data.xpath("td[3]/a[@href]/@href").extract())
            item['torrert_count'] = u''.join(data.xpath("td[@nowrap]/span[@class='bts_1']/text()").extract())
            items.append(item)
        return items
        pass

    def parse_detail(self, response):
        item = MovieDetailItem()
        item['detail_link'] = response.url
        item['download_link'] = response.xpath("//p[@class='original download']/a[@id='download']/@href").extract()
        item['magnet_link'] = response.xpath("//p[@class='original magnet']/a[@id='magnet']/@href").extract()
        return item
        pass