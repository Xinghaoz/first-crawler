import scrapy
from scrapy.spiders import BaseSpider
from scrapy.selector import Selector
from first_crawler.items import FashionItem
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
import time
import re
import pymongo
from pymongo import MongoClient

import scrapy_splash
from scrapy_splash import SplashRequest, SplashResponse


class MeilishuoSpider (BaseSpider):
    name = 'meilishuo'
    allowed_domains = ['meilishuo.com']
    start_urls = ["http://www.meilishuo.com/"]

    # Test Links
    #start_urls = ["http://www.meilishuo.com/guang/catalog/hot?nid=223229&cata_id=1000000000000&pstrc=fe_pos%3Awlc_navwords_0_0_0&ptp=1.YUGqAYIU.0.0.tAzXw"]

    # For MongoDB
    client = MongoClient()
    db = client.meilishuo

    # No need to execute Javascript in the main page.
    '''
    # For getting the Javascript Content
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, self.parse, meta={
                'splash': {
                    'endpoint': 'render.html'
                }
            })
    '''

    # Parse and find the categories links in the main page.
    def parse(self, response):
        pattern_list = re.compile(r'/guang/catalog/hot\S*')

        i = 0
        for item_list in pattern_list.findall(response.body):
            i += 1
            url_complete = r'http://www.meilishuo.com' + item_list
            url_complete = url_complete.split("\"")[0]
            print '+++++++++++++++++++++++++', i, url_complete
            req = Request(url = url_complete, callback = self.parse_list)
            yield req

    # Parse and find the item links in the categories links.
    def parse_list(self, response):
        mongo = self.db.url
        url = response.url
        print '&&&&&&&&&&&&&&&&&&&&&&&&&', response.status, url
        pattern = re.compile(r'page=\d+')

        if (pattern.search(url)):
            page = pattern.findall(url)[0]
            page = int(re.findall('\d+', page)[0])
            page += 1
            page = 'page=' + str(page)
            url = pattern.sub(page, url)
        else:
            url = url + '&page=2'

        print '+++++++++++++++++++++++++', url
        req = Request(url = url, callback = self.parse_list)
        yield req

        pattern_detail = re.compile(r'/share/item/\S*')
        i = 0
        for item_url in pattern_detail.findall(response.body):
            i += 1
            url_complete = r'http://www.meilishuo.com' + item_url
            url_complete = url_complete.split("\"")[0]
            url_trim = url_complete.split('?')[0]

            # Use MongoDB to check the duplicate.
            if mongo.find_one({"url": url_trim}):
                print "&&&&&&&&&&&&&&&&&&&&&&&&& This URL has been crawled &&&&&&&&&&&&&&&&&&&&&&&&&"
            else:
                req = Request(url = url_trim, callback = self.parse_item)
                newone = {
                    "url": url_trim,
                    "time": time.time(),
                }
                mongo.insert_one(newone)
                yield req

    # Parse the item links, get the expected information.
    def parse_item(self, response):
        page = Selector(response)
        title = page.xpath('//span[@itemprop="name"]/text()').extract_first()
        images = page.xpath('//img[@id="J_BigImg"]/@src').extract_first()
        availability = page.xpath('//dd[@class="num clearfix"]/div[@class="J_GoodsStock goods-stock fl"]/text()').extract_first()
        status = response.status

        item = FashionItem()
        url_trim = response.url.split('?')[0]
        item['url'] = url_trim
        item['title'] = title.encode('utf-8')
        item['images'] = images
        item['availability'] = availability.encode('utf-8')
        item['status'] = status
        return item
