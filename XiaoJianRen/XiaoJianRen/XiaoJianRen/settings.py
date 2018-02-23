# -*- coding: utf-8 -*-

# Scrapy settings for XiaoJianRen project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'XiaoJianRen'

SPIDER_MODULES = ['XiaoJianRen.spiders']
NEWSPIDER_MODULE = 'XiaoJianRen.spiders'
# 云打码相关配置到yundama.com申请注册
# 普通用户信息
YUNDAMA_USERNAME = 'AsherCode'
YUNDAMA_PASSWORD = 'Wangjian123456'
# 开发者申请的app信息
YUNDAMA_APP_ID = '4453'
YUNDAMA_APP_KEY = '0e40de4290c1b4f2baefe7ba588496e4'
YUNDAMA_API_URL = 'http://api.yundama.com/api.php'
# 云打码最大尝试次数
YUNDAMA_MAX_RETRY = 20

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'XiaoJianRen (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
COOKIES_ENABLED = False
RANDOM_UA_TYPE = "random"
PROXY_URL = 'http://localhost:5000/get'
DOWNLOADER_MIDDLEWARES = {
    'XiaoJianRen.middlewares.RandomUserAgent': 10,
    'XiaoJianRen.middlewares.ProxyMiddleware': 11,
    # 'XiaoJianRen.middlewares.SeleniumMiddleware': 12,# caipu时才打开
}
ITEM_PIPELINES = {
    # 'XiaoJianRen.pipelines.MysqlTwistedPipline': 2,#连接池异步插入
    # 'XiaoJianRen.pipelines.MongoPipeline': 3,
    # 'scrapy_redis.pipelines.RedisPipeline': 301	#将不存储爬取的item到redis
    'XiaoJianRen.pipelines.ElasticsearchPipeline': 1
}
DOWNLOAD_DELAY = 5
MYSQL_HOST = "127.0.0.1"
MYSQL_DBNAME = "xjr"
MYSQL_USER = "root"
MYSQL_PASSWORD = "123456"
SQL_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
SQL_DATE_FORMAT = "%Y-%m-%d"
import sys
import os
BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'XiaoJianRen'))
LOG_LEVEL = 'DEBUG'
HTTPERROR_ALLOWED_CODES = [404,403,401]
SELENIUM_TIMEOUT = 20
MAX_PAGE = 56
PHANTOMJS_SERVICE_ARGS = ['--load-images=false', '--disk-cache=true']

#redis配置
# SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# REDIS_URL = 'redis://root:123456@192.168.56.101:6379'

MONGO_URI ='127.0.0.1'
MONGO_DB = 'xjr'
# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'XiaoJianRen.middlewares.XiaojianrenSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'XiaoJianRen.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'XiaoJianRen.pipelines.XiaojianrenPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'