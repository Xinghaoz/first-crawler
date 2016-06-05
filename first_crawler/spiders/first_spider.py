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

    ''' For Further use.
    def parse_url(self, response):
        print '#########################'
        #page = Selector(response)
        #divs = page.xpath('//a[@rel="nofollow"]')
        #divs = page.xpath('//div[@class="nav_more"]/dl[@class="nav_more_warp"]/dd')
        #divs = page.xpath('//div[@class="nav_more"]')
        #divs = page.xpath('//dl[@class="nav_more_warp"]/dd/a[@rel="nofollow"]')
        #print '#######', response.url

        return Request(url = response.url, callback = self.parse_shop)


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

    #def parse_shop(self, response):
        #print '========================='
        #return Request(url = response.url)

    def parse_item(self, response):
        print '========================='
        page = Selector(response)
        title = page.xpath('//span[@itemprop="name"]/text()').extract_first()
        images = page.xpath('//img[@id="J_BigImg"]/@src').extract_first()
        availability = page.xpath('//dd[@class="num clearfix"]/div[@class="J_GoodsStock goods-stock fl"]/text()').extract_first()

        #color_array = page.xpath('//ol[@class="J_StyleList style-list clearfix"]')
        #for li in color_array:
            #color = li.xpath('.//li[@class="img"]/@title').extract_first()
            #print '*************************', color

        item = FashionItem()
        item['url'] = response.url
        item['title'] = title.encode('utf-8')
        item['images'] = images
        item['availability'] = availability.encode('utf-8')
        return item
