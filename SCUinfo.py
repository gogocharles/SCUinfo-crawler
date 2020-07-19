from json import loads

from getHTMLText import getDynamicText

url = "https://api.scuinfo.com/api/posts?pageSize=15"
nextPage = ""
posts = [] 

for i in range(10):

    page = loads(getDynamicText(url + nextPage, 'api.scuinfo.com', 'https://scuinfo.com/', 'gzip'))
    data = page['data']
    cnt = 0
    for item in data:
        cnt += 1
        posts.append(item['content'])
        if len(data) == cnt:
            nextPage = "&fromId=" + str(item['id'])

for post in posts:
    print(post)
    print("="*40)
