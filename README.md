# SCUinfo-crawler 四川大学匿名论坛爬虫

## Introduction

基于Python编写的网络爬虫，获取并归档SCUinfo从2018年1月1日起至今的所有帖子

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
