# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class FirstCrawlerPipeline(object):
    def __init__(self):
        self.file = open('fashion', 'wb')

    def process_item(self, item, spider):
        val = "{0}\t{1}\n".format(item['url'], item['title'])
        self.file.write(val)
        return item
