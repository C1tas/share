# Scrapy Tutorial

[文档](https://doc.scrapy.org/en/latest/)

## scrapy structure

scrapy 的结构要简单不少就是各个部分拼接起来最后完成整个功能的过程

所以下面这个结构图要看

![结构图](./scrapy_architecture.png)

在这个结构中的各个步骤就是scrapy运行的步骤

一个scrapy的项目结构是

```shell
 ~/apps/hack   master  tree
.
├── hack
│   ├── __init__.py
│   ├── items.py
│   ├── middlewares.py
│   ├── pipelines.py
│   ├── __pycache__
│   │   ├── __init__.cpython-36.pyc
│   │   ├── items.cpython-36.pyc
│   │   ├── middlewares.cpython-36.pyc
│   │   ├── pipelines.cpython-36.pyc
│   │   └── settings.cpython-36.pyc
│   ├── settings.py
│   └── spiders
│       ├── doubangroup.py
│       ├── get_comments.py
│       ├── hack_douban.py
│       ├── __init__.py
│       ├── __pycache__
│       │   ├── doubangroup.cpython-36.pyc
│       │   ├── get_comments.cpython-36.pyc
│       │   ├── hack_douban.cpython-36.pyc
│       │   └── __init__.cpython-36.pyc
│       └── sitemap.py
├── README.md
└── scrapy.cfg

4 directories, 21 files

```
大致是这样的，主要是主目录hack下的
- items.py 设置该项目中的关键字变量，比如标题，作者，地址，等等你希望爬取下来的值
- middlewares.py 用来处理你的爬取过程中的reqest请求
- pipelines.py 用来处理爬取后的items
- settings.py 整个项目的设置

以及spiders文件夹下的爬虫脚本

一个个文件往下看
`items.py`

```python
import scrapy


class HackItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    alt = scrapy.Field()
    author = scrapy.Field()
    comments_count = scrapy.Field()
    content = scrapy.Field()
    created = scrapy.Field()
    id = scrapy.Field()
    like_count = scrapy.Field()
    locked = scrapy.Field()
    photos = scrapy.Field()
    share_url = scrapy.Field()
    title = scrapy.Field()
    updated = scrapy.Field()
```
形如这样不用管类型，目的就是告诉scrapy有这么几个值需要填充

`middlewares.py`
```python
# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals


class HackSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    # def process_spider_input(response, spider):
    #     # Called for each response that goes through the spider
    #     # middleware and into the spider.

    #     # Should return None or raise an exception.
    #     return None

    # def process_spider_output(response, result, spider):
    #     # Called with the results returned from the Spider, after
    #     # it has processed the response.

    #     # Must return an iterable of Request, dict or Item objects.
    #     for i in result:
    #         yield i

    # def process_spider_exception(response, exception, spider):
    #     # Called when a spider or process_spider_input() method
    #     # (from other spider middleware) raises an exception.

    #     # Should return either None or an iterable of Response, dict
    #     # or Item objects.
    #     pass

    # def process_start_requests(self, start_requests, spider):
    #     # Called with the start requests of the spider, and works
    #     # similarly to the process_spider_output() method, except
    #     # that it doesn’t have a response associated.

    #     # Must return only requests (not items).
    #     for r in start_requests:
    #         yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class HackDownloaderMiddleware(object):

    def process_request(self, request, spider):
        print (request.headers)
        request.headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36".encode('UTF-8')
        print (request.headers)


```
你们可以看到，这里有两个类，一个HackSpiderMiddleware一个HackDownloaderMiddleware

第一个是用来设置爬虫处理的

第二个是我写来在每个请求中改变User-Agent的

写好了后往settings.py中的对应条目中添加这个类就好了

`pipelines.py`

``` python
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import logging

from scrapy.conf import settings
from scrapy.exceptions import DropItem



class HackPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoDBPipeline(object):
    collection_name = 'house'
    def __init__(self, mongo_url, mongo_port, mongo_db):
        self.mongo_url = mongo_url
        self.mongo_port = mongo_port
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_url = settings['MONGODB_SERVER'],
            mongo_port = settings['MONGODB_PORT'],
            mongo_db = settings['MONGODB_DB']
        )

    def open_spider(self, spider):
        try:
            self.client = pymongo.MongoClient(
                self.mongo_url,
                self.mongo_port
            )
            self.db = self.client[self.mongo_db]
        except Exception as e:
            logging.log(logging.ERROR, "There is a error happend")

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if item:
            # print(item)
            self.db[self.collection_name].insert(dict(item))
            # logging.log(logging.WARNING, "FUCKC!!!!THAT!!!!!!!!!!!!!!!!!!!!")
            # raise DropItem("Duplicate item found: %s" % item)
        else:
            # raise DropItem("Duplicate item found: %s" % item)
            logging.log(logging.WARNING, "FUCKC!!!!!!!!!!!!!!!!!!!!!!!!")
        return item
```
代码应该浅显易懂就不过多解释

`spiders/hack_douban.py`

```python
import scrapy
import json

from scrapy.exceptions import CloseSpider
from hack.items import HackItem

class Num_Generator:
    def __init__(self, start, end, step):
        self.i = start
        self.n = end
        self.step = step
        pass

    def __iter__(self):
        return self

    def next(self):
        if self.i < self.n:
            i = self.i
            self.i += self.step
            return i
        else:
            raise StopIteration


class Hack_Douban(scrapy.Spider):
    name = "hack_douban"

    start_urls = [
        'https://api.douban.com/v2/group/beijingzufang/',
    ]

    url = "https://api.douban.com/v2/group/beijingzufang/topics?count=%d&start=%d"
    a = Num_Generator(0, 25000, 100)
    def parse(self, response):
        try:
            x = self.a.next()
        except StopIteration:
            raise CloseSpider('finished')
        url = self.url % (100, x)
        yield scrapy.Request(url, self.parse)

        tmp_json = json.loads(response.body.decode('UTF-8'))
        for i in range(0, 100, 1):
            item = HackItem()
            tmp = tmp_json['topics'][i]
            item['alt'] = tmp['alt']
            item['author'] = tmp['author']
            item['comments_count'] = tmp['comments_count']
            item['content'] = tmp['content']
            item['created'] = tmp['created']
            item['id'] = tmp['id']
            item['like_count'] = tmp['like_count']
            item['locked'] = tmp['locked']
            item['photos'] = tmp['photos']
            item['share_url'] = tmp['share_url']
            item['title'] = tmp['title']
            item['updated'] = tmp['updated']
            yield item

```
这个代码也很简单

只有最后的yield 将item这个被实例化的HackItem抛出给下一个流程处理

这样一个十分简单的爬虫就完成了


我写来练习的源码

[github](https://github.com/C1tas/scrapy_hack)
 
