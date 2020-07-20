from json import loads

from getHTMLText import getDynamicText

import time

import functions

url = "https://api.scuinfo.com/api/posts?pageSize=15"
nextPage = ""
posts = []

date = time.strftime("%Y-%m-%d", time.localtime(time.time()-86400))
end = time.strftime("%Y-%m-%d", time.localtime(time.time()-172800))
out = open("corpus\\"+date+".txt", "w", encoding="utf-8")
text = ""
flag = True

while flag:
    page = loads(getDynamicText(url + nextPage, 'api.scuinfo.com',
                                'https://scuinfo.com/', 'gzip'))
    data = page['data']
    cnt = 0
    for item in data:
        cnt += 1
        postDate = functions.getDate(item['date'])
        if postDate == date:
            text = text + "="*20+"\n"+item['content']+"\n"
        elif postDate == end:
            flag = False
            break
        if len(data) == cnt:
            nextPage = "&fromId=" + str(item['id'])

out.write(text)
out.close()
