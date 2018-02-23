# _*_ coding: utf-8 _*_
__author__ = 'AsherCode'
__date__ = '2017/6/25 10:18'


from datetime import datetime
from elasticsearch_dsl import DocType, Date, Nested, Boolean, \
    analyzer, InnerObjectWrapper, Completion, Keyword, Text, Integer

from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer

from elasticsearch_dsl.connections import connections
connections.create_connection(hosts=["localhost"])


class CustomAnalyzer(_CustomAnalyzer):
    def get_analysis_definition(self):
        return {}


ik_analyzer = CustomAnalyzer("ik_max_word", filter=["lowercase"])


class FoodType(DocType):
    suggest = Completion(analyzer=ik_analyzer)
    title = Text(analyzer="ik_max_word")
    author = Keyword()
    consume = Keyword()
    description = Text(analyzer="ik_max_word")
    popularity = Keyword()
    create_date = Keyword()
    advantage = Text(analyzer="ik_max_word")
    url = Keyword()
    url_object_id = Keyword()
    image_url = Keyword()
    class Meta:
        index = "meishijie"
        doc_type = "food"


if __name__ == "__main__":
    FoodType.init()
