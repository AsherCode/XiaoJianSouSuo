# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request, Spider
from urllib import parse

from items import XiaojianrenItemLoader, CaiItem
from utils.common import get_md5
from urllib.parse import quote

class CaipuSpider(scrapy.Spider):
    name = 'caipu'
    allowed_domains = ['meishij.net']
    base_url='http://www.meishij.net/chufang/diy/'

    def start_requests(self):
        for page in range(1, self.settings.get('MAX_PAGE') + 1):
            yield Request(url=self.base_url, callback=self.parse, meta={'page': page}, dont_filter=True)

    def parse(self, response):
        cais = response.css("#listtyle1_list .listtyle1")
        for cai in cais:
            cai_item = CaiItem()  # 实例化
            cai_item["consume"] = cai.css(".c2 .li1::text").extract_first("")
            cai_item["post_url"] = cai.css("a::attr(href)").extract_first("")
            cai_item["description"] = cai.css(".c2 .li2::text").extract_first("")
            cai_item["popularity"] = cai.css(".c1 span::text").extract_first("")
            cai_item["title"] = cai.css(".c1 strong::text").extract_first("")
            cai_item["author"] = cai.css(".c1 em::text").extract_first("")
            cai_item["advantage"] = cai.css(".gx span::text").extract_first("")
            cai_item["url_object_id"] = get_md5(cai_item["post_url"])
            cai_item["image_url"] = cai.css("img::attr(src)").extract_first("")
            yield  cai_item
