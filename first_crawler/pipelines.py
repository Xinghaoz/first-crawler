# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json, codecs

class FirstCrawlerPipeline(object):
    def __init__(self):
        self.mogujie = codecs.open('mogujie.dat', 'wb', encoding = 'utf-8')
        self.file_quantity = open('quantity.dat', 'wb')
        self.meilishuo = codecs.open('meilishuo.dat', 'wb', encoding = 'utf-8')
        #self.file = open('fashion.dat', 'wb')

    def process_item(self, item, spider):
        # Show Chinese, for checking the correctness
        if (spider.name == 'mogujie' or spider.name == 'mogujie_mac' or spider.name == 'test'):
            line = json.dumps(dict(item)) + "\n"
            self.mogujie.write(line)

            #val = "{0}\t{1}\t{2}\t{3}\t{4}\n".format(item['url'], item['title'], item['images'], item['availability'], item['status'])
            #self.file.write(val)
        if (spider.name == 'meilishuo'):
            line = json.dumps(dict(item)) + "\n"
            self.meilishuo.write(line)

        if (spider.name == 'quantity_checker'):
            line = json.dumps(dict(item)) + "\n"
            self.file_quantity.write(line)

        return item
