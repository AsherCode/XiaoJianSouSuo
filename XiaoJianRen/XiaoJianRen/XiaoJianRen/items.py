# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
from elasticsearch import TransportError
import datetime
import scrapy
import re
import codecs
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from w3lib.html import remove_tags

from settings import SQL_DATETIME_FORMAT
from models.es_jobbole import ArticleType
from models.es_lagou import LagouType
from models.es_food import FoodType
from models.es_movie import MovieType
from models.es_zhihu import ZhiHuQuestionType, ZhiHuAnswerType
from elasticsearch_dsl.connections import connections
import redis
es = connections.create_connection(ArticleType._doc_type.using)	#连接到es
redis_cli = redis.StrictRedis()
def Null_if(value):
    try:
        return  value
    except Exception as e:
        return "无"
def remove_chinaese(value):
    str = ''.join([i if ord(i) < 128 else ' ' for i in value])
    return str.strip()
def remove_html(value):
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub(' ', value)
    return dd.split(' ')
def get_city(value):
    value=remove_html(value)
    return value[1]
def get_degree(value):
    value = remove_html(value)
    return value[5]
def get_experience(value):
    value = remove_html(value)
    return value[3]
def remove_splash(value):
    #去掉工作城市的斜线
    return value.replace("/","")

def handle_jobaddr(value):
    addr_list = value.split("\n")
    addr_list = [item.strip() for item in addr_list if item.strip()!="查看地图"]
    return "".join(addr_list)
def date_convert(value):
    try:
        create_date = datetime.datetime.strptime(value, "%Y-%m-%d").date()
    except Exception as e:
        create_date = datetime.datetime.now().date()
    return create_date
def remove_comment_tags(value):
    #去掉tag中提取的评论
    if "评论" in value:
        return ""
    else:
        return value
def get_duration(value):
    try:
        duration = re.search("span>(.*?)<\/span>",value)
        return duration.group(1).strip()
    except Exception as e:
        return value
def get_score(value):
    try:
        score1 = re.search("span>(.*?)<\/span>",value)
        score2 = re.search(".*?(\d+.*)", value)
        if score1 is not None:
            return score1.group(1).strip()
        else:
            return score2.group(1).strip()
    except Exception as e:
            return value
def return_value(value):
    try:
        dr = re.compile(r'<[^>]+>', re.S)
        dd = dr.sub('', value)
        if dd.strip=='':
            return ''
    except Exception as e:
        return "无"
def get_nums(value):
    match_re = re.match(".*?(\d+).*", value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0
def get_desc(value):
    try:
        # value = re.findall(u'[\u4e00-\u9fa5].+?', value)
        # value=''.join(str(n) for n in value)
        description1 = re.search("span>(.*?)<a",value,re.S)
        description2 = re.search("span>(.*?)</div>", value, re.S)
        if description1 is not None:
            return description1.group(1).strip()
        else:
            return description2.group(1).strip()
    except Exception as e:
        return value
def extract_num(text):
    #从字符串中提取出数字
    match_re = re.match(".*?(\d+.*\d+).*", text)
    if match_re:
        nums = int(re.sub(",","",match_re.group(1)))
    else:
        nums = 0

    return nums
def get_value(value):
    return value
def gen_suggests(index, info_tuple):
	#根据字符串生成搜索建议数组
	used_words = set()
	suggests = []
	for text, weight in info_tuple:
		if text:
			#调用es的analyze接口分析字符串
			words = es.indices.analyze(index=index, analyzer="ik_max_word", params={'filter':["lowercase"]}, body=text)
			anylyzed_words = set([r["token"] for r in words["tokens"] if len(r["token"])>1])
			new_words = anylyzed_words - used_words
		else:
			new_words = set()
		if new_words:
			suggests.append({"input":list(new_words), "weight":weight})
	return suggests
class XiaojianrenItemLoader(ItemLoader):
    #自定义itemloader
    default_output_processor = TakeFirst()
class movie80sItem(scrapy.Item):
    title = scrapy.Field()
    create_date = scrapy.Field(
        input_processor=MapCompose(date_convert),  # 传递进来可以预处理
    )
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    front_image_url = scrapy.Field()
    tags = scrapy.Field(
        output_processor=Join(",")
    )
    description = scrapy.Field(
        input_processor = MapCompose(get_desc)
    )
    score = scrapy.Field(
        input_processor=MapCompose(get_score),
    )
    duration = scrapy.Field(
        input_processor=MapCompose(get_duration),
    )
    def get_insert_sql(self):
        insert_sql="""
        insert into movies(title,create_date,url,url_object_id,front_image_url,tags,description,score,duration)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON DUPLICATE KEY UPDATE url=VALUES(url),tags=VALUES(tags),score=VALUES(score),title=VALUES(title)
        """
        params = (self["title"],self["create_date"],self["url"],self["url_object_id"],self["front_image_url"],self["tags"],self["description"],self["score"],self["duration"])
        return insert_sql,params
    def save_to_es(self):
        movie = MovieType()
        movie.title = self['title']
        movie.url = self['url']
        movie.meta.id = self["url_object_id"]
        movie.create_date = self['create_date']
        movie.front_image_url = self['front_image_url']
        movie.tags = self['tags']
        movie.duration = self['duration']
        movie.score = self['score']
        movie.description = self['description']
        movie.suggest = gen_suggests(MovieType._doc_type.index, ((movie.title, 10), (movie.tags, 7)))
        movie.save()
        redis_cli.incr("jobbole_count")
        return
class xunyingItem(scrapy.Item):
    title = scrapy.Field()
    create_date = scrapy.Field(
        input_processor=MapCompose(date_convert),  # 传递进来可以预处理
    )
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    front_image_url = scrapy.Field()
    tags = scrapy.Field()
    description = scrapy.Field(
        input_processor=MapCompose(get_desc)
    )
    score = scrapy.Field(
        input_processor=MapCompose(get_score),
    )
    duration = scrapy.Field(
        input_processor=MapCompose(get_duration),
    )
    def get_insert_sql(self):
        insert_sql="""
        insert into movies(title,create_date,url,url_object_id,front_image_url,tags,description,score,duration)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON DUPLICATE KEY UPDATE url=VALUES(url),tags=VALUES(tags),score=VALUES(score),title=VALUES(title)
        """
        params = (self["title"],self["create_date"],self["url"],self["url_object_id"],self["front_image_url"],self["tags"],self["description"],self["score"],self["duration"])
        return insert_sql,params
    def save_to_es(self):
        movie = MovieType()
        movie.title = self['title']
        movie.url = self['url']
        movie.meta.id = self["url_object_id"]
        movie.create_date = self['create_date']
        movie.front_image_url = self['front_image_url']
        movie.tags = self['tags']
        movie.duration = self['duration']
        movie.score = self['score']
        movie.description = self['description']
        movie.suggest = gen_suggests(MovieType._doc_type.index, ((movie.title, 10), (movie.tags, 7)))
        movie.save()
        redis_cli.incr("jobbole_count")
        return
class ZhihuQuestionItem(scrapy.Item):
    #知乎的问题 item
    zhihu_id = scrapy.Field()
    topics = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field(
        input_processor=MapCompose(get_value),
    )
    answer_num = scrapy.Field()
    comments_num = scrapy.Field()
    watch_user_num = scrapy.Field()
    click_num = scrapy.Field()
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        # 插入知乎question表的sql语句
        insert_sql = """
                insert into zhihu_question(zhihu_id, topics, url, title, content, answer_num, comments_num,
                  watch_user_num, click_num, crawl_time
                  )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE content=VALUES(content), answer_num=VALUES(answer_num), comments_num=VALUES(comments_num),
                  watch_user_num=VALUES(watch_user_num), click_num=VALUES(click_num)
            """
        zhihu_id = self["zhihu_id"][0]
        topics = self["topics"]
        url = self["url"]
        title = "".join(self["title"])
        try:
            content = "".join(self["content"])
        except BaseException:
            content = "无"
        try:
            answer_num = extract_num("".join(self["answer_num"]))
        except BaseException:
            answer_num = 0
        comments_num = extract_num("".join(self["comments_num"]))

        if len(self["watch_user_num"]) == 2:
            watch_user_num = extract_num(self["watch_user_num"][0])
            click_num = extract_num(self["watch_user_num"][1])
        else:
            watch_user_num = extract_num(self["watch_user_num"][0])
            click_num = 0

        crawl_time = datetime.datetime.now().strftime(SQL_DATETIME_FORMAT)

        params = (
            zhihu_id,
            topics,
            url,
            title,
            content,
            answer_num,
            comments_num,
            watch_user_num,
            click_num,
            crawl_time)

        return insert_sql, params
    def save_to_es(self):
            question = ZhiHuQuestionType()
            question.title = self['title']
            question.url = self["url"]
            question.topics = self["topics"]
            try:
                question.answer_num = extract_num(self["answer_num"][0])
            except BaseException:
                question.answer_num = 0
            try:
                question.crawl_time = self["crawl_time"]
            except BaseException:
                question.crawl_time = datetime.datetime.now().strftime(SQL_DATETIME_FORMAT)

            question.comments_num = extract_num(self["comments_num"][0])
            question.watch_user_num = extract_num(self["watch_user_num"][0])
            question.click_num = extract_num(self["watch_user_num"][1])
            question.meta.id = self["zhihu_id"]
            try:
                question.content = remove_tags(self["content"])
            except BaseException:
                question.content =  self['title']

            question.suggest = gen_suggests(ZhiHuQuestionType._doc_type.index, ((question.title, 10), (question.topics, 7)))
            question.save()
            redis_cli.incr("jobbole_count")
            return



class ZhihuAnswerItem(scrapy.Item):
    #知乎的问题回答item
    zhihu_id = scrapy.Field()
    url = scrapy.Field()
    title=scrapy.Field()
    question_id = scrapy.Field()
    author_id = scrapy.Field()
    content = scrapy.Field()
    parise_num = scrapy.Field()
    question_url=scrapy.Field()
    try:
        comments_num = scrapy.Field()
    except TransportError:
        comments_num = 0
    create_time = scrapy.Field()
    update_time = scrapy.Field()
    crawl_time = scrapy.Field()
    author_name = scrapy.Field()

    def get_insert_sql(self):
        #插入知乎question表的sql语句
        insert_sql = """
            insert into zhihu_answer(zhihu_id, url,question_url, title,question_id, author_id, content, parise_num, comments_num,
              create_time, update_time, crawl_time,author_name
              ) VALUES (%s, %s,%s, %s, %s, %s,%s, %s, %s, %s, %s, %s,%s)
              ON DUPLICATE KEY UPDATE content=VALUES(content), comments_num=VALUES(comments_num), parise_num=VALUES(parise_num),
              update_time=VALUES(update_time),author_name=VALUES(author_name)
        """

        create_time = datetime.datetime.fromtimestamp(self["create_time"]).strftime(SQL_DATETIME_FORMAT)
        update_time = datetime.datetime.fromtimestamp(self["update_time"]).strftime(SQL_DATETIME_FORMAT)
        params = (
            self["zhihu_id"], self["url"],self["question_url"],self["title"], self["question_id"],
            self["author_id"], self["content"], self["parise_num"],
            self["comments_num"], create_time, update_time,
            self["crawl_time"].strftime(SQL_DATETIME_FORMAT),
            self["author_name"],
        )

        return insert_sql, params
    def save_to_es(self):
        answer = ZhiHuAnswerType()
        answer.url = self["question_url"]
        answer.title = self["title"]
        answer.crawl_time = self["crawl_time"]
        answer.comments_num = self["comments_num"]
        answer.author_name = self["author_name"]
        answer.parise_num = self["parise_num"]
        answer.comments_num = self["comments_num"]
        answer.author_id = self["author_id"]
        answer.question_id = self["question_id"]
        answer.meta.id = self["zhihu_id"]
        answer.content = remove_tags(self["content"])
        answer.suggest = gen_suggests(ZhiHuQuestionType._doc_type.index, ((answer.title, 10), (answer.content, 7)))
        answer.save()
        redis_cli.incr("jobbole_count")
        return

class LagouJobItem(scrapy.Item):
    #拉勾网职位信息
    title = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    salary = scrapy.Field()
    job_city = scrapy.Field(
        input_processor=MapCompose(remove_splash),
    )
    work_years = scrapy.Field(
        input_processor=MapCompose(remove_splash),
    )
    degree_need = scrapy.Field(
        input_processor = MapCompose(remove_splash),
    )
    job_type = scrapy.Field()
    publish_time = scrapy.Field()
    job_advantage = scrapy.Field()
    job_desc = scrapy.Field()
    job_addr = scrapy.Field(
        input_processor=MapCompose(remove_tags, handle_jobaddr), #去除html的tags
    )
    company_name = scrapy.Field()
    company_url = scrapy.Field()
    tags = scrapy.Field(
        input_processor = Join(",")
    )
    crawl_time = scrapy.Field()
    def get_insert_sql(self):
        insert_sql = """
            insert into job(title, url, url_object_id, salary, job_city, work_years, degree_need,
            job_type, publish_time, job_advantage, job_desc, job_addr, company_name, company_url,
            tags, crawl_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE salary=VALUES(salary), job_desc=VALUES(job_desc)
        """
        params = (
            self["title"], self["url"], self["url_object_id"], self["salary"], self["job_city"],
            self["work_years"], self["degree_need"], self["job_type"],
            self["publish_time"], self["job_advantage"], self["job_desc"],
            self["job_addr"], self["company_name"], self["company_url"],
            self["tags"], self["crawl_time"].strftime(SQL_DATETIME_FORMAT),
        )
        return insert_sql, params

    def save_to_es(self):
         job = LagouType()
         job.title = self['title']
         if "create_date" in self:
            job.create_date = self["create_date"]
         job.url = self["url"]
         job.meta.id = self["url_object_id"]
         if "salary" in self:
            job.salary = self["salary"]
         job.job_city = self["job_city"]
         if "work_years" in self:
            job.work_years = self["work_years"]
         job.degree_need = self["degree_need"]
         job.job_type = self["job_type"]
         job.publish_time = self["publish_time"]
         job.job_advantage = self["job_advantage"]
         job.job_desc = self["job_desc"]
         job.job_addr = self["job_addr"]
         job.company_name = self["company_name"]
         job.company_url = self["company_url"]
         job.crawl_time = self["crawl_time"]
         job.suggest = gen_suggests(LagouType._doc_type.index, ((job.title, 10), (job.tags, 7)))
         job.save()
         redis_cli.incr("jobbole_count")
         return

class JobBoleArticleItem(scrapy.Item):
    title = scrapy.Field()
    create_date = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    front_image_url = scrapy.Field()
    front_image_path = scrapy.Field()
    praise_nums = scrapy.Field()
    comment_nums = scrapy.Field()
    fav_nums = scrapy.Field()
    tags = scrapy.Field()
    content = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            insert into jobbole_article(title, url, create_date, fav_nums,url_object_id,front_image_url,praise_nums,comment_nums,tags,content)
            VALUES (%s, %s, %s, %s,%s, %s, %s, %s,%s, %s) 
            ON DUPLICATE KEY UPDATE content=VALUES(content), praise_nums=VALUES(praise_nums), comment_nums=VALUES(comment_nums),
                  fav_nums=VALUES(fav_nums), title=VALUES(title)
        """
        params = (self["title"], self["url"],self["create_date"], self["fav_nums"],self["url_object_id"],self["front_image_url"],self["praise_nums"],self["comment_nums"],self["tags"],self["content"])

        return insert_sql, params

    def save_to_es(self):
        article = ArticleType()
        article.title = self['title']
        article.create_date = self["create_date"]
        article.content = remove_tags(self["content"])
        article.front_image_url = self["front_image_url"]
        if "front_image_path" in self:
            article.front_image_path = self["front_image_path"]
        article.praise_nums = self["praise_nums"]
        article.fav_nums = self["fav_nums"]
        article.comment_nums = self["comment_nums"]
        article.url = self["url"]
        article.tags = self["tags"]
        article.meta.id = self["url_object_id"]

        article.suggest = gen_suggests(ArticleType._doc_type.index, ((article.title, 10), (article.tags, 7)))

        article.save()

        redis_cli.incr("jobbole_count")

        return

class ZhipinItem(scrapy.Item):
    #boss直聘网职位信息
    title = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    salary = scrapy.Field()
    job_city = scrapy.Field(
        input_processor=MapCompose(get_city)
    )
    work_years = scrapy.Field(
        input_processor=MapCompose(get_experience)
    )
    degree_need = scrapy.Field(
        input_processor=MapCompose(get_degree)
    )
    publish_time = scrapy.Field(
        input_processor=MapCompose(remove_chinaese)
    )
    job_advantage = scrapy.Field(
        input_processor=MapCompose(Null_if),
        output_processor=Join(),
    )
    job_desc = scrapy.Field(
        input_processor=MapCompose(Null_if),
        output_processor = Join(),
    )
    job_addr = scrapy.Field(
        input_processor=MapCompose(remove_tags, handle_jobaddr), #去除html的tags
    )
    company_name = scrapy.Field()
    company_url = scrapy.Field()
    tags = scrapy.Field(
        input_processor = Join(",")
    )
    crawl_time = scrapy.Field()
    def get_insert_sql(self):
        insert_sql = """
            insert into job(title, url, url_object_id, salary, job_city, work_years, degree_need, publish_time, 
            job_advantage, job_desc, job_addr, company_name, company_url,
            tags, crawl_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE salary=VALUES(salary), job_desc=VALUES(job_desc)
        """
        params = (
            self["title"], self["url"], self["url_object_id"], self["salary"], self["job_city"],
            self["work_years"], self["degree_need"],self["publish_time"], self["job_advantage"], self["job_desc"],
            self["job_addr"], self["company_name"], self["company_url"],
            self["tags"], self["crawl_time"].strftime(SQL_DATETIME_FORMAT),
        )
        return insert_sql, params
    def save_to_es(self):
         job = LagouType()
         job.title = self['title']
         if "create_date" in self:
            job.create_date = self["create_date"]
         job.url = self["url"]
         job.meta.id = self["url_object_id"]
         if "salary" in self:
            job.salary = self["salary"]
         job.job_city = self["job_city"]
         if "work_years" in self:
            job.work_years = self["work_years"]
         job.degree_need = self["degree_need"]
         job.tags = self["tags"]
         job.publish_time = self["publish_time"]
         job.job_advantage = self["job_advantage"]
         job.job_desc = self["job_desc"]
         job.job_addr = self["job_addr"]
         job.company_name = self["company_name"]
         job.company_url = self["company_url"]
         job.crawl_time = self["crawl_time"]
         job.suggest = gen_suggests(LagouType._doc_type.index, ((job.title, 10), (job.tags, 7)))
         job.save()
         redis_cli.incr("jobbole_count")
         return



class CaiItem(scrapy.Item):
    consume = scrapy.Field()
    post_url=scrapy.Field()
    description=scrapy.Field()
    popularity=scrapy.Field()
    title=scrapy.Field()
    author=scrapy.Field()
    advantage=scrapy.Field()
    url_object_id=scrapy.Field()
    image_url = scrapy.Field()

    def get_insert_sql(self):
        insert_sql="""
        insert into cai (title) VALUES (%s)
        """
        insert_sql = """
                    insert into cai(consume, post_url,description,popularity,title,author,advantage,image_url,url_object_id)
                    VALUES (%s, %s, %s, %s,%s, %s, %s,%s, %s) 
                    ON DUPLICATE KEY UPDATE  popularity=VALUES(popularity), consume=VALUES(consume)
                """
        params = (self["consume"], self["post_url"], self["description"],self["popularity"],
                  self["title"], self["author"], self["advantage"], self["image_url"], self["url_object_id"])

        return insert_sql, params
    def save_to_es(self):
        food = FoodType()
        food.title = self['title']
        food.author = self['author']
        food.consume = self['consume']
        food.create_date = datetime.datetime.now().date()
        food.description = self['description']
        food.popularity = self['popularity']
        food.advantage = self['advantage']
        food.url = self['post_url']
        food.meta.id = self["url_object_id"]
        food.image_url = self['image_url']
        food.suggest = gen_suggests(FoodType._doc_type.index, ((food.title, 10), (food.description, 7)))
        food.save()
        redis_cli.incr("jobbole_count")
        return