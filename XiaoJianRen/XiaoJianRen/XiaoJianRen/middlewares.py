# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random
import logging
import requests

from fake_useragent import UserAgent
from scrapy import signals
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.http import HtmlResponse
from logging import getLogger
class RandomUserAgent(object):
    """根据预定义的列表随机更换用户代理"""
    def __init__(self,crawler):
        super(RandomUserAgent,self).__init__()
        self.ua = UserAgent()
        self.ua_type = crawler.settings.get("RANDOM_UA_TYPE","random")


    @classmethod
    def from_crawler(cls,crawler):
        return cls(crawler)


    def process_request(self,request,spider):
        def get_ua():
            return getattr(self.ua,self.ua_type)
        random_ua = get_ua()
        request.headers.setdefault('User-Agent',get_ua())




class ProxyMiddleware():
	def __init__(self, proxy_url):
		self.logger = logging.getLogger(__name__)
		self.proxy_url = proxy_url

	def get_random_proxy(self):
		try:
			response = requests.get(self.proxy_url)
			if response.status_code == 200:
				proxy = response.text
				return proxy
		except requests.ConnectionError:
			return False

	def process_request(self, request, spider):
		if request.meta.get('retry_times'):
			proxy = self.get_random_proxy()
			if proxy:
				uri = 'https://{proxy}'.format(proxy=proxy)
				self.logger.debug('使用代理 ' + proxy)
				request.meta['proxy'] = uri

	@classmethod
	def from_crawler(cls, crawler):
		settings = crawler.settings
		return cls(
			proxy_url=settings.get('PROXY_URL')
		)





class SeleniumMiddleware():
    def __init__(self, timeout=None, service_args=[]):
        self.logger = getLogger(__name__)
        self.timeout = timeout
        self.browser = webdriver.PhantomJS(service_args=service_args)
        self.browser.set_window_size(1400, 700)
        self.browser.set_page_load_timeout(self.timeout)
        self.wait = WebDriverWait(self.browser, self.timeout)

    def __del__(self):
        self.browser.close()

    def process_request(self, request, spider):
        """
        用PhantomJS抓取详情页面
        :param request: Request对象
        :param spider: Spider对象
        :return: HtmlResponse
        """
        self.logger.debug('PhantomJS is Starting')
        page = request.meta.get('page')
        try:
            self.browser.get(request.url)
            if page > 1:
                input = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '.gopage>form > input:nth-child(2)')))
                submit = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '.gopage>form > input:nth-child(3)')))
                input.clear()
                input.send_keys(page)
                submit.click()
            self.wait.until(
                EC.text_to_be_present_in_element((By.CSS_SELECTOR, '.listtyle1_page_w>.current'), str(page)))
            self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.listtyle1_list .listtyle1')))
            return HtmlResponse(url=request.url, body=self.browser.page_source, request=request, encoding='utf-8',
                                status=200)
        except TimeoutException:
            return HtmlResponse(url=request.url, status=500, request=request)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(timeout=crawler.settings.get('SELENIUM_TIMEOUT'),
                   service_args=crawler.settings.get('PHANTOMJS_SERVICE_ARGS'))
