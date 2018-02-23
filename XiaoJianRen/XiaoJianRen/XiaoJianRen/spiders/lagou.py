# -*- coding: utf-8 -*-
import datetime
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from items import LagouJobItem, XiaojianrenItemLoader
from utils.common import get_md5


class LagouSpider(CrawlSpider):
    '''
    没有parse函数，被CrawlSpider重载，继承Spider--start_requests--parse--_parse_response--lagou.parse_start_url,lagou.process_results\
    --Rule--LinkExtractor--_requests_to_follow--extract_link抽取所有link--—_response_download--lagou.rule.callback
    '''
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/']

    custom_settings = {  # 优先并覆盖项目，避免被重定向
        "COOKIES_ENABLED": False,  # 关闭cookies
        "DOWNLOAD_DELAY": 5,
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Cookie':'user_trace_token=20180113120608-47baf311-32d1-42bd-b7bd-e295a0ddf211; _ga=GA1.2.1935054305.1515816368; LGUID=20180113120609-16068441-f817-11e7-9429-525400f775ce; index_location_city=%E5%85%A8%E5%9B%BD; JSESSIONID=ABAAABAABEEAAJA83B6C797B4B4E28CF19CCC1154448377; _gid=GA1.2.498277084.1518311553; _gat=1; LGSID=20180211091235-a4e08259-0ec8-11e8-838e-525400f775ce; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1517882987,1517883024,1517910297,1518311555; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1518311556; LGRID=20180211091238-a67f391c-0ec8-11e8-afdf-5254005c3644',
            'Host':'www.lagou.com'
        }
    }
    # https://www.lagou.com/jobs/4039556.html
    rules = (
        Rule(LinkExtractor(allow=("zhaopin/.*",)), follow=True),
        Rule(LinkExtractor(allow=("gongsi/j\d+.html",)), follow=True),
        Rule(LinkExtractor(allow=r'jobs/\d+.html'), callback='parse_job', follow=True),# follow深入爬取
    )

    def parse_job(self, response):
        #解析拉勾网的职位
        item_loader = XiaojianrenItemLoader(item=LagouJobItem(), response=response)
        item_loader.add_css("title", ".job-name::attr(title)")
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_css("salary", ".job_request .salary::text")
        item_loader.add_xpath("job_city", "//*[@class='job_request']/p/span[2]/text()")
        item_loader.add_xpath("work_years", "//*[@class='job_request']/p/span[3]/text()")
        item_loader.add_xpath("degree_need", "//*[@class='job_request']/p/span[4]/text()")
        item_loader.add_xpath("job_type", "//*[@class='job_request']/p/span[5]/text()")

        item_loader.add_css("tags", '.position-label li::text')
        item_loader.add_css("publish_time", ".publish_time::text")
        item_loader.add_css("job_advantage", ".job-advantage p::text")
        item_loader.add_css("job_desc", ".job_bt div")
        item_loader.add_css("job_addr", ".work_addr")
        item_loader.add_css("company_name", "#job_company dt a img::attr(alt)")
        item_loader.add_css("company_url", "#job_company dt a::attr(href)")
        item_loader.add_value("crawl_time", datetime.datetime.now())

        job_item = item_loader.load_item()

        return job_item
