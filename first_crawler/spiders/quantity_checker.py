import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from first_crawler.items import QuantityItem
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
import re



class QuantityChecker (CrawlSpider):
    name = 'quantity_checker'
    allowed_domains = ['mogujie.com']
    start_urls = ["http://www.mogujie.com/"]

    # Test Links
    #start_urls = ["http://shop.mogujie.com/1qfnyw/list/index?categoryId=20005650&order=sale&shopwebtag=1&mt=10.6464.r78321&ptp=1.BtWxRgdy._mt-6464-r78321.1.FvR1m"]
    #start_urls = ["http://www.mogujie.com/book/clothing/50003?from=hpc_2"]

    rules = (
        Rule(LinkExtractor( allow = ("http://shop.mogujie.com/",), deny = ("http://shop.mogujie.com/detail/",)), follow = True), # follow = True !!
        Rule(LinkExtractor( allow = ("http://shop.mogujie.com/detail/",)), callback = 'parse_item'),
    )

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, self.parse, meta={
                'splash': {
                    'endpoint': 'render.html'
                }
            })

    def parse_item(self, response):
        print '========================='
        page = Selector(response)
        availability = page.xpath('//dd[@class="num clearfix"]/div[@class="J_GoodsStock goods-stock fl"]/text()').extract_first()
        print '*************************', availability
        quantity = re.findall('\d+', availability)
        status = response.status

        item = QuantityItem()
        item['url'] = response.url
        item['quantity'] = quantity[0]
        item['status'] = status

        return item
