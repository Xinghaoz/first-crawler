import scrapy
from scrapy.spiders import CrawlSpider, Rule
#from scrapy.linkextractors.sgml import SgmlLinkExtractor
#from scrapy.spiders import BaseSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request

class FirstSpider (CrawlSpider):
    name = 'first_crawler'
    allowed_domains = ['wikipedia.org']
    start_urls = ["https://en.wikipedia.org/wiki/Mathematics"]


    rules = (
        #Rule(LinkExtractor(restrict_xpaths = ('//div[@class="mw-body"]//a/@href'))),
        Rule(LinkExtractor( allow = ("https://en.wikipedia.org/wiki/",)), callback = 'parse_item'),
        )

    def parse_item(self, response):
        print '#########################'
        hxs = HtmlXPathSelector(response)
        #print hxs.select('//h1[@class="firstHeading"]/span/text()').extract()
        heading = hxs.select('//h1[@class="firstHeading"]/span/text()').extract()
        #heading = hxs.select('//div').extract()
        print '=======', heading
