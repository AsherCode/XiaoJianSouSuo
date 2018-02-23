# -*- coding: utf-8 -*-
import scrapy
import re

from pydispatch import dispatcher
from scrapy import signals
from scrapy.http import Request
from urllib import parse

from items import XiaojianrenItemLoader, movie80sItem
from utils.common import get_md5


class Movie80sSpider(scrapy.Spider):
    name = 'movie80s'
    allowed_domains = ['80s.tw']
    start_urls = ['https://www.80s.tw/movie/list']
    def parse(self, response):
        last_url = response.css("#block3 > div.clearfix.noborder.block1 > div > a:nth-child(7)").css("a::attr(href)").extract_first("")
        last_code_re = re.search(".*?(\d+)", last_url)
        last_code = last_code_re.group(1)
        yield Request(url=response.url,meta={"last_code":last_code},callback=self.parse_list)
    def parse_list(self,response):
        last_code = response.meta.get("last_code", "421")
        post_nodes = response.css("#block3 > div.clearfix.noborder.block1 > ul.me1.clearfix > li")
        for post_node in post_nodes:
            image_url = post_node.css("img::attr(_src)").extract_first("")
            post_url = post_node.css("li>a::attr(href)").extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url": image_url},
                          callback=self.parse_detail)  # response获取meta

        for i in range(1, int(last_code)):
            i+=1
            next_url = "/movie/list/-----p"+str(i)
            yield Request(url=parse.urljoin(response.url, next_url),meta={"last_code":last_code},callback=self.parse_list)
    def parse_detail(self, response):
        movie_item = XiaojianrenItemLoader() # 实例化
        #通过item loader加载item
        front_image_url = response.meta.get("front_image_url", "")  # 文章封面图
        item_loader = XiaojianrenItemLoader(item=movie80sItem(), response=response)#默认ItemLoader是一个list，自定义TakeFirst()
        item_loader.add_css("title", "#minfo > div.info > h1::text")
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_xpath("create_date", '//*[@id="minfo"]/div[2]/div[1]/span[5]/text()')
        item_loader.add_value("front_image_url", [front_image_url])
        item_loader.add_xpath("tags", '//*[@id="minfo"]/div[2]/div[1]/span[1]/a/text()')
        item_loader.add_xpath("duration",'//*[@id="minfo"]/div[2]/div[1]/span[6]')
        item_loader.add_xpath("score",'//*[@id="minfo"]/div[2]/div[2]/span[1]')
        item_loader.add_css("description",'#movie_content')

        movie_item = item_loader.load_item()



        yield movie_item #将传到piplines中