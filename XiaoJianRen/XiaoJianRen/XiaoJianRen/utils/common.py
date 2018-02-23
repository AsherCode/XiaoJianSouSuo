# -*- coding: utf-8 -*-
__author__ = 'bobby'
import hashlib
import re
import json
from datetime import date, datetime


def get_md5(url):
    if isinstance(url, str):	#若是unicode则转为utf-8
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


def extract_num(text):
    #从字符串中提取出数字
    match_re = re.match(".*?(\d+.*\d+).*", text)
    if match_re:
        nums = int(re.sub(",","",match_re.group(1)))
    else:
        nums = 0

    return nums

class DateEncoder(json.JSONEncoder):
    # json.dumps无法序列化datetime，新写函数实现
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)

if __name__ == "__main__":
    print (get_md5("http://jobbole.com".encode("utf-8"))) # unicode不支持hashlib.md5编码

