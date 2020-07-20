import time
import requests

def getDate(timeStamp):
    timeArray = time.localtime(timeStamp)
    timeStyled = time.strftime("%Y-%m-%d", timeArray)
    return timeStyled

def getDynamicText(url, host, referer, encoding):
    try:
        kv = {'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/80.0.3987.132 Safari/537.36',
              'host': host,
              'referer': referer
              }
        r = requests.get(url, headers=kv)
        r.raise_for_status()
        r.encoding = encoding
        return r.text
    except:
        return "Mission failed! Error Code: " + str(r.status_code)


def getStaticText(url):
    try:
        kv = {'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/80.0.3987.132 Safari/537.36'}
        r = requests.get(url, headers=kv)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "Mission failed! Error Code: " + str(r.status_code)

if __name__=="__main__":
    u = "https://api.scuinfo.com/api/posts?pageSize=15"
    print(getDynamicText(u, 'api.scuinfo.com', 'https://scuinfo.com/', 'gzip'))
    print(getStaticText("http://www.baidu.com"))
    print(getDate(1563796861))