# -*- coding: utf-8 -*-
import scrapy
import re

from pydispatch import dispatcher
from scrapy import signals
from scrapy.http import Request
from urllib import parse

from items import XiaojianrenItemLoader, xunyingItem
from utils.common import get_md5


class XunyingSpider(scrapy.Spider):
    name = 'xunying'
    allowed_domains = ['www.xunyingwang.com']
    start_urls = ['http://www.xunyingwang.com/movie/']

    def parse(self, response):
        post_nodes = response.css("body > div:nth-child(3) > div.row > div.col-xs-12 > div > div")
        for post_node in post_nodes:
            image_url = post_node.css("a img::attr(data-original)").extract_first("")
            post_url = post_node.css("a::attr(href)").extract_first("")
            tags = post_node.css(".otherinfo a::text").extract()
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url": image_url,"tags":tags},
                          callback=self.parse_detail)  # response获取meta
        # 提取下一页并交给scrapy进行下载
        next_url = response.xpath("//a[contains(@rel, 'next')]").css("::attr(href)").extract_first("")
        if next_url:
            print(next_url)
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self, response):
        if response.url == 'http://www.xunyingwang.com/movie/':
            print("------------------url为www.xunyingwang.com/movie------------------")
            return None
        movie_item = XiaojianrenItemLoader()  # 实例化
        # 通过item loader加载item
        front_image_url = response.meta.get("front_image_url", "")  # 文章封面图
        tags = response.meta.get("tags", "")
        item_loader = XiaojianrenItemLoader(item=xunyingItem(), response=response)  # 默认ItemLoader是一个list，自定义TakeFirst()
        item_loader.add_css("title", ".movie-info h1::text")
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_xpath("create_date", '/html/body/div[2]/div/div/div[1]/div[1]/div[2]/table/tbody/tr[7]/td[2]')
        item_loader.add_value("front_image_url", front_image_url)
        item_loader.add_value("tags", ','.join(str(n) for n in tags))
        item_loader.add_xpath("duration", '/html/body/div[2]/div/div/div[1]/div[1]/div[2]/table/tbody/tr[8]/td[2]/text()')
        item_loader.add_css("score", '.score::text')
        item_loader.add_xpath("description", '/html/body/div[2]/div/div/div[1]/div[2]/div[2]/p/text()')

        movie_item = item_loader.load_item()

        yield movie_item  # 将传到piplines中
