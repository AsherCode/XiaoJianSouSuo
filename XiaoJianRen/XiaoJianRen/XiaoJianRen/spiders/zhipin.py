# -*- coding: utf-8 -*-
import datetime
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from items import XiaojianrenItemLoader, ZhipinItem
from utils.common import get_md5


class ZhipinSpider(CrawlSpider):
    name = 'zhipin'
    allowed_domains = ['www.zhipin.com']
    start_urls = ['http://www.zhipin.com/']
    custom_settings = {  # 优先并覆盖项目，避免被重定向
        "COOKIES_ENABLED": False,  # 关闭cookies
        "DOWNLOAD_DELAY": 5,
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Host': 'www.zhipin.com',
        }
    }
    rules = (
        Rule(LinkExtractor(allow=r'job_detail/\d+.html'), callback='parse_job', follow=True),  # follow深入爬取
    )

    def parse_job(self, response):
        item_loader = XiaojianrenItemLoader(item=ZhipinItem(), response=response)
        item_loader.add_css("title", "div.name>h1::text")
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_css("salary", "#main > div.job-banner > div > div > div.info-primary > div.name > span::text")
        item_loader.add_css("job_city", '#main > div.job-banner > div > div > div.info-primary > p')
        item_loader.add_css("degree_need", '#main > div.job-banner > div > div > div.info-primary > p')
        item_loader.add_css("work_years", '#main > div.job-banner > div > div > div.info-primary > p')

        item_loader.add_css("tags", '.job-tags span::text')
        item_loader.add_css("publish_time", "#main > div.job-banner > div > div > div.info-primary > div.job-author > span::text")
        item_loader.add_xpath("job_advantage", "//div[@class='job-sec company-info']/div/text()")
        item_loader.add_xpath("job_desc", '//*[@id="main"]/div[3]/div/div[2]/div[3]/div[1]/div/text()')
        item_loader.add_css("job_addr", ".location-address::text")
        item_loader.add_css("company_name", "#main > div.job-banner > div > div > div.info-company > h3 > a::text")
        item_loader.add_css("company_url", "#main > div.job-banner > div > div > div.info-company > h3 > a::attr(href)")
        item_loader.add_value("crawl_time", datetime.datetime.now())

        job_item = item_loader.load_item()

        return job_item
