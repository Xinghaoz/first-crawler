import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from first_crawler.items import FashionItem
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
import time
import re
#from scrapy_splash import SplashRequest


class MogujieSpider (CrawlSpider):
    name = 'mogujie_mac'
    allowed_domains = ['mogujie.com']
    #start_urls = ["http://www.mogujie.com/"]

    # Test Links
    start_urls = ["http://www.mogujie.com/book/clothing/50249?from=hpc_6&ptp=1.BtWxRgdy.0.39.TY4Kc"]
    #start_urls = ["http://shop.mogujie.com/1qfnyw/list/index?categoryId=20005650&order=sale&shopwebtag=1&mt=10.6464.r78321&ptp=1.BtWxRgdy._mt-6464-r78321.1.FvR1m"]
    #start_urls = ["http://www.mogujie.com/book/clothing/50003?from=hpc_2"]

    rules = (
        Rule(LinkExtractor( allow = ("http://www.mogujie.com/book/", "http://shop.mogujie.com/", "http://act.mogujie.com/", "http://list.mogujie.com/"), deny = ("http://shop.mogujie.com/detail/",)), follow = True), # follow = True !!
        Rule(LinkExtractor( allow = ("http://shop.mogujie.com/detail/",)), callback = 'parse_item', follow = True),
    )

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, self.parse, meta={
                'splash': {
                    'args': {
                        # set rendering arguments here
                        'html': 1,
                        'png': 1,

                        # 'url' is prefilled from request url
                        # 'http_method' is set to 'POST' for POST requests
                        # 'body' is set to request body for POST requests
                    },
                    'endpoint': 'render.html'
                }
            })

    def process_links(self, links):
        for link in links:
            link.url = "http://192.168.99.100:8050/?" + urlencode({ 'url' : link.url })
        return links

    def parse_item(self, response):
        pattern = re.compile('/detail/')
        if pattern.findall(response.url):
            print '==========================', response.url

        url_trim = response.url.split('?')[0]

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
