import time
import requests


def getdate(time_stamp):
    """
    将时间戳还原为"%Y-%m-%d"形式的日期

    :param time_stamp: 时间戳
    :return: "%Y-%m-%d"形式的日期
    """

    time_array = time.localtime(time_stamp)
    time_styled = time.strftime("%Y-%m-%d", time_array)
    return time_styled


def fetch_json_package(url, host, referer, encoding):
    """
    JSON抓包函数

    :param url: AJAX API地址
    :param host: 目标服务器
    :param referer: header的引用页
    :param encoding: 编码
    :return: 字典格式的JSON数据包
    """

    kv = {'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/80.0.3987.132 Safari/537.36',
          'host': host,
          'referer': referer
          }
    r = requests.get(url, headers=kv)
    r.raise_for_status()
    r.encoding = encoding
    return r.text


if __name__ == "__main__":
    u = "https://api.scuinfo.com/api/posts?pageSize=150"
    print(fetch_json_package(u, 'api.scuinfo.com', 'https://scuinfo.com/', 'gzip'))
