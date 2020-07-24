import logging
from json import loads, dump
from os import mkdir
from time import time, sleep

from requests import HTTPError

from functions import getdate, fetch_json_package

DATA_PATH = "data/"  # 存放post数据的路径
logging.basicConfig(filename="crawler_report.log", format="%(asctime)s - %(levelname)s: %(message)s")
URL = "https://api.scuinfo.com/api/posts?pageSize=150"


def request(start_id=None):
    """
    想SCUinfo服务器发起请求

    :param start_id: 当前请求的post ID
    :return: 字典格式的JSON数据包
    """

    url = URL + "&fromId=" + start_id if start_id else URL
    while True:
        try:
            return fetch_json_package(url, 'api.scuinfo.com',
                                      'https://scuinfo.com/', 'gzip')
        except HTTPError:
            # 如果因为请求太密集拒绝访问, 则等待一段时间
            logging.warning("Request denied at ID: "+start_id)
            sleep(180)


def fetch(end, start_id=None):
    """
    爬取截止到指定日期前的所有post

    :param start_id: 起始post id, 默认为当前时间最新的post id
    :param end: 爬取post的截止日期, 形式为: "%Y-%m-%d"
    :return: 结果写入/data/%Y/路径下对应月份的JSON文件, 无返回值
    """

    yesterday = getdate(time() - 86400).split("-")
    monthly_posts = dict()
    last_year = ""
    this_year, this_month = yesterday[0], yesterday[1]
    try:
        mkdir(DATA_PATH + this_year)
    except FileExistsError:
        pass
    flag = True
    current_id = start_id
    last_date = ""

    while flag:
        page = loads(request(current_id))
        data = page['data']
        cnt = 0
        for item in data:
            cnt += 1
            post_date = getdate(item['date'])
            date = post_date.split("-")
            year, month, day = date[0], date[1], date[2]
            if year != this_year:
                try:
                    mkdir(DATA_PATH + year)
                except FileExistsError:
                    pass
                last_year = this_year
                this_year = year
            if month != this_month:
                if month == "12":
                    out = open(DATA_PATH + last_year + "/01.json", "w", encoding="utf-8")
                else:
                    out = open(DATA_PATH + this_year + "/" + this_month + ".json", "w", encoding="utf-8")
                dump(monthly_posts, out, ensure_ascii=False, indent=4)
                out.close()
                this_month = month
                monthly_posts = dict()
            if last_date == end and post_date != end or post_date == "2018-01-01" and len(data) == cnt:
                with open(DATA_PATH + this_year + "/" + this_month + ".json", "w", encoding="utf-8") as out:
                    dump(monthly_posts, out, ensure_ascii=False, indent=4)
                flag = False
                break
            if day in monthly_posts.keys():
                monthly_posts[day].append((item["gender"], item["content"]))
            else:
                monthly_posts[day] = [(item["gender"], item["content"]), ]
            if len(data) == cnt:
                current_id = str(item['id'])
            last_date = post_date


if __name__ == "__main__":
    fetch("2018-01-01", "10000671")
