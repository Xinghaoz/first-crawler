import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from first_crawler.items import FashionItem
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request


from scrapy.contrib.loader import ItemLoader


class FirstSpider (CrawlSpider):
    name = 'first_crawler'
    allowed_domains = ['mogujie.com']
    #start_urls = ["http://www.mogujie.com/"]
    start_urls = ["http://www.mogujie.com/book/clothing/50003?from=hpc_2"]


    rules = (
        #Rule(LinkExtractor(restrict_xpaths = ('//div[@class="mw-body"]//a/@href'))),
        #Rule(LinkExtractor( allow = ("http://www.mogujie.com/",)), callback = 'parse_url'),
        #Rule(LinkExtractor( allow = ("http://shop.mogujie.com/detail/",)), callback = 'parse_item'),
        Rule(LinkExtractor( allow = ("http://www.mogujie.com/book/shoes",)), callback = 'parse_item'),
    )

    def parse_url(self, response):
        print '#########################'
        #page = Selector(response)
        #divs = page.xpath('//a[@rel="nofollow"]')
        #divs = page.xpath('//div[@class="nav_more"]/dl[@class="nav_more_warp"]/dd')
        #divs = page.xpath('//div[@class="nav_more"]')
        #divs = page.xpath('//dl[@class="nav_more_warp"]/dd/a[@rel="nofollow"]')
        #print '#######', response.url

        return Request(url = response.url, callback = self.parse_item)

        '''
        for div in divs:
            #item = FashionItem()
            url = div.xpath('./@href').extract_first()
            category = div.xpath('./text()').extract_first()
            if category:
                category = category.encode('utf-8')
            #item['url'] = url
            #if category:
                #item['categories'] = category

            #print '=======' div
            print '=======', url
        #yield item
        '''

    def parse_item(self, response):
        print '========================='
        file = open('body', 'wb')
        file.write(response.body)
