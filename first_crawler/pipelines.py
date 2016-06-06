# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json, codecs

class FirstCrawlerPipeline(object):
    def __init__(self):
        self.file_json = codecs.open('fashion_json.dat', 'wb', encoding = 'utf-8')
        self.file_quantity = open('quantity.dat', 'wb')
        #self.file = open('fashion.dat', 'wb')

    def process_item(self, item, spider):
        # Show Chinese, for checking the correctness
        if (spider.name == 'first_spider'):
            print '+++++++++++++++++++++++++'
            line = json.dumps(dict(item)) + "\n"
            self.file_json.write(line)

            #val = "{0}\t{1}\t{2}\t{3}\t{4}\n".format(item['url'], item['title'], item['images'], item['availability'], item['status'])
            #self.file.write(val)

        if (spider.name == 'quantity_checker'):
            print '-------------------------'
            line = json.dumps(dict(item)) + "\n"
            self.file_quantity.write(line)

        return item
