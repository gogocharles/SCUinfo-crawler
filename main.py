import logging
from json import loads, dump
from os import mkdir
from time import time, sleep

from requests import HTTPError

from functions import getdate, fetch_json_package

DATA_PATH = "data/"  # 存放post数据的路径
# logging的基本设置, 如果访问太密集被服务器拒绝, 日志则会记录拒绝访问的时间, 与当前所在的锚点ID
logging.basicConfig(filename="crawler_report.log", format="%(asctime)s - %(levelname)s: %(message)s")
URL = "https://api.scuinfo.com/api/posts?pageSize=150"  # SCUinfo API的URL, 通过设置pagesize让每次请求抓取150条post


def request(start_id=None):
    """
    向SCUinfo服务器发起请求, 抓取json数据包

    :param start_id: 当前请求的post ID
    :return: 字典格式的JSON数据包
    """

    url = URL + "&fromId=" + start_id if start_id else URL
    while True:
        try:
            return fetch_json_package(url, 'api.scuinfo.com',
                                      'https://scuinfo.com/', 'gzip')
        except HTTPError:
            # 如果因为请求太密集拒绝访问, 则等待一段时间, SCUinfo的等待时间大致为3分钟
            logging.warning("Request denied at ID: " + start_id)
            sleep(180)


def fetch(end):
    """
    爬取截止到指定日期前的所有post

    :param end: 爬取post的截止日期, 形式为: "%Y-%m-%d"
    :return: 结果写入/data/%Y/路径下对应月份的JSON文件, 无返回值
    """

    today = getdate(time()).split("-")
    monthly_posts = dict()  # 按月存储post信息的字典, 以日期为键, 以[["gender", "text"], ...]形式的嵌套列表为值
    this_year, this_month = today[0], today[1]
    try:
        mkdir(DATA_PATH + this_year)
    except FileExistsError:
        pass
    flag = True  # 用来标记程序结束
    current_id = ""  # 当前post的ID, 当一轮post遍历完毕, 则以最后一个post的ID为锚点发起下一轮请求
    last_date = ""  # 上一个post的日期, 用来判断程序是否达到终点
    rnd = 0  # 抓取json数据包的轮数

    while flag:
        page = loads(request(current_id))
        data = page['data']
        cnt = 0
        if rnd == 0 and cnt == 0:
            # 第一条帖子为公告, 去除
            data.pop(0)
        for item in data:
            cnt += 1
            post_date = getdate(item['date'])
            date = post_date.split("-")
            year, month, day = date[0], date[1], date[2]
            last_year = this_year
            # 如果到达了指定日期的下一天, 或者已经爬完了所有贴子, 则输出已有数据结束程序
            if last_date == end and post_date != end or post_date == "2018-01-01" and len(data) == cnt:
                with open(DATA_PATH + last_year + "/" + this_month + ".json", "w", encoding="utf-8") as out:
                    dump(monthly_posts, out, ensure_ascii=False, indent=4)
                flag = False
                break
            # 进入下一月份, 则输出上一个月份的数据
            if month != this_month:
                # 跨年的情况
                if month == "12":
                    # 进入新一年, 则为新一年创建目录
                    try:
                        mkdir(DATA_PATH + year)
                    except FileExistsError:
                        pass
                    last_year = this_year
                    this_year = year
                    # 写入去年一月的数据
                    out = open(DATA_PATH + last_year + "/01.json", "w", encoding="utf-8")
                else:
                    # 非跨年情形, 则写入上个月数据
                    out = open(DATA_PATH + this_year + "/" + this_month + ".json", "w", encoding="utf-8")
                dump(monthly_posts, out, ensure_ascii=False, indent=4)
                out.close()
                # 将当前post的月份设置为"当前月"
                this_month = month
                monthly_posts = dict()
            # 将当前post的发帖人性别与文本写入monthly_posts
            if day in monthly_posts.keys():
                monthly_posts[day].append((item["gender"], item["content"]))
            else:
                monthly_posts[day] = [(item["gender"], item["content"]), ]
            # 如果一轮遍历完成, 则记录最后一个post的ID, 以此为锚点向服务器发起请求
            if len(data) == cnt:
                current_id = str(item['id'])
            last_date = post_date
        rnd += 1


if __name__ == "__main__":
    end_date = input("输入截止日期(请按'年-月-日'格式, 例如'2020-07-01', 则爬取2020年7月1日至今的所有帖子): ")
    fetch(end_date)
