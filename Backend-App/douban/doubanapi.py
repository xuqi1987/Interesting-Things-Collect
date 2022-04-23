# -*- coding: utf-8 -*-
import requests

from lxml import etree
from urllib import quote
import json
from bs4 import BeautifulSoup

class DoubanMovie():

    SEARCH_RUL = u"https://movie.douban.com/subject_search?search_text=%s"

    def __init__(self):
        pass

    def _get(self,url):
        r = requests.get(url)
        if r.status_code == 200:
            return r
        else:
            print "[Error]status_code is not 200 url=%s \n"%url
            return None

    def searchMovie(self,*args):
        key = "+".join(list(args))
        r = self._get(self.SEARCH_RUL%key)
        ret_dic = {}
        if r != None:
            tree = etree.HTML(r.text)
            search_nodes = tree.xpath('//div[@class="article"]/div/table')
            if len(search_nodes) > 0:
                for item in search_nodes:
                    nodes =  item.xpath('tr/td[1]/a')
                    for node in nodes:
                        name =  u''.join(node.xpath('img/@alt'))
                        if name.find(key) >= 0:
                            ret_dic['name'] = name
                            ret_dic['url'] = u''.join(node.xpath('@href'))
                pass
            else:
                pass


        return ret_dic


    def detailInfo(self,url):
        r = self._get(url)
        ret_dic = {}
        ret_dic['alt'] = url

        if r != None:
            tree = etree.HTML(r.text)
            ret_dic['title'] = u''.join(tree.xpath('//span[@property="v:itemreviewed"]/text()'))
            ret_dic['year'] = u''.join(tree.xpath('//span[@class="year"]/text()'))[1:-1]
            ret_dic['rating'] = u''.join(tree.xpath('//strong[@property="v:average"]/text()'))
            ret_dic['directors'] = u''.join(tree.xpath('//a[@rel="v:directedBy"]/text()'))
            ret_dic['genres'] = u'|'.join(tree.xpath('//span[@property="v:genre"]/text()'))
            ret_dic['pubdates'] = u'|'.join(tree.xpath('//span[@property="v:initialReleaseDate"]/text()'))
            ret_dic['rating_betterthan'] = u'|'.join(tree.xpath('//div[@class="rating_betterthan"]/a/text()'))

            info = BeautifulSoup(r.text,"lxml").find(id="info")
            del info['id']
            ret_dic['info']  = info.prettify()

            ret_dic['summary'] = u''.join(tree.xpath('//span[@property="v:summary"]/text()')).strip()


            print "Douban :  %s\n"%(ret_dic['title'])
        return ret_dic

        pass


    def pick_movie(self,type):
        # type
        # 热门
        # 最新
        # 经典
        # 豆瓣高分
        # 华语
        # 欧美
        # 喜剧
        # 科幻
        url = "https://movie.douban.com/j/search_subjects?type=movieflask&tag=%s&sort=recommend&page_limit=20&page_start=0"%(quote(type))
        r = self._get(url)
        ret_dic = {}
        if r != None:
            ret_dic =  json.loads(r.text)

        return ret_dic


