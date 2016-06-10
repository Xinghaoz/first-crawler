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


class TestSpider (BaseSpider):
    name = 'mogujie'
    allowed_domains = ['mogujie.com']
    start_urls = ["http://www.mogujie.com/"]

    # Test Links
    #start_urls = ["http://www.mogujie.com/book/clothing/50249"]
    #start_urls = ["http://shop.mogujie.com/1qfnyw/list/index?categoryId=20005650&order=sale&shopwebtag=1&mt=10.6464.r78321&ptp=1.BtWxRgdy._mt-6464-r78321.1.FvR1m"]
    #start_urls = ["http://www.mogujie.com/book/clothing/50003?from=hpc_2"]

    # For MongoDB
    client = MongoClient()
    db = client.mogujie

    # For getting the Javascript Content
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, self.parse, meta={
                'splash': {
                    'endpoint': 'render.html'
                }
            })


    def parse(self, response):
        #print '=========================', response.url
        pattern_list = re.compile(r'http://www.mogujie.com/book/\w+/\d+')
        #print '+++++++++++++++++++++++++', pattern_list.findall(response.body)

        '''
        for item_list in pattern_list.findall(response.body):
            req = Request(url = item_list, callback = self.parse_list)
            yield req
        '''

        '''
        req = Request(url = 'http://www.mogujie.com/book/clothing/50249/', callback = self.parse_list, meta={
                'splash': {
                    'endpoint': 'render.html'
                },
                #'dont_send_headers': True,
        })
        '''

        for item_list in pattern_list.findall(response.body):
            #req = SplashRequest(url = 'http://www.mogujie.com/book/clothing/50249/', callback = self.parse_list)
            req = SplashRequest(url = item_list, callback = self.parse_list)
            yield req

    def parse_list(self, response):
        #print '+++++++++++++++++++++++++443', response.url
        url = response.meta['splash']['args']['url']
        print '&&&&&&&&&&&&&&&&&&&&&&&&&', response.status, url
        pattern = re.compile(r'http://www.mogujie.com/book/\w+/\d+/')

        if (pattern.match(url)):
            page = int(pattern.split(url)[1])
            url = pattern.findall(url)[0]
            page += 1
            url = url + str(page)
        else:
            url = url + '/2'

        print '+++++++++++++++++++++++++', url
        req = SplashRequest(url = url, callback = self.parse_list)
        yield req

        #print '+++++++++++++++++++++++++', response.url
        pattern_detail = re.compile(r'http://shop.mogujie.com/detail/.{7}')
        #print '==========================', len(pattern_detail.findall(response.body))
        for item_url in pattern_detail.findall(response.body):
            req = Request(url = item_url, callback = self.parse_item)
            yield req


    def parse_item(self, response):
        mongo = self.db.url
        # url = response.meta['splash']['args']['url'] # Used for SplashRequest
        url = response.url
        url_trim = url.split('?')[0]
        if mongo.find_one({"url": url_trim}):
    	    print "&&&&&&&&&&&&&&&&&&&&&&&&& This URL has been crawled &&&&&&&&&&&&&&&&&&&&&&&&&"
    	    return

        # Insert the new link into MongoDB
        newone = {
            "url": url_trim,
            "time": time.time(),
        }
        mongo.insert_one(newone)

        page = Selector(response)
        title = page.xpath('//span[@itemprop="name"]/text()').extract_first()
        images = page.xpath('//img[@id="J_BigImg"]/@src').extract_first()
        availability = page.xpath('//dd[@class="num clearfix"]/div[@class="J_GoodsStock goods-stock fl"]/text()').extract_first()
        status = response.status

        item = FashionItem()
        item['url'] = url_trim
        item['title'] = title.encode('utf-8')
        item['images'] = images
        item['availability'] = availability.encode('utf-8')
        item['status'] = status
        return item
