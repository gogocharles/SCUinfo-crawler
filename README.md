# SCUinfo-crawler 四川大学匿名论坛爬虫

![](https://img.shields.io/apm/l/vim-mode)

## 简介

基于Python编写的网络爬虫，获取并归档SCUinfo从2018年1月1日后任意日期至今的所有帖子

SCUinfo为动态加载的页面，需要向其AJAX接口发起请求抓取json数据包。关于这一部分如何实现，可以参考我的[这篇博文](https://blog.gogocharles.xyz/2020/03/16/scuinfo-crawler/)。

注意，SCUinfo的AJAX接口是有可能更换的，所以如果无法正确访问，请用刚刚那篇文章的方法调用开发者工具获取API的URL以及header中的重要信息。

## 如何使用

在执行程序之前请确保你安装了requests

```bash
pip install requests
```

运行main.py

```bash
python main.py
```

输入截止日期，比如你要获取2020年7月1日至今的所有帖子，就输入`2020-07-01`，请严格按照“年-月-日”的格式，月和日不满两位请用0补齐

如果你需要爬取大量数据（一次3000条以上），SCUinfo服务器会因为过于频繁的访问而暂时拒绝你的IP，这时候程序会将警告信息输出到crawler_report.log，然后等待3分钟，因此爬取大量数据会需要比较长的时间

获取到的数据存放在data/目录按年份归档，帖子以json格式，按月存储，发帖人性别与文本一一对应：

```json
{
  "date": [
      [
        "gender",
        "text"
    ],
      [
        "gender",
        "text"
    ]
  ]
}
```

在本项目的data目录下已经存放了我爬好的从2018年1月1日到2020年7月24日的所有帖子。因为SCUinfo的服务器只保存了2018年1月1日至今的数据，所以无法获取更早的。
