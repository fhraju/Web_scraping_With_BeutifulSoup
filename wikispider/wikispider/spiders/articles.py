"""
A Scrapy spider that traverses many pages.
"""
from gc import callbacks
import imp
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from wikispider.items import Article

class ArticleSpider(CrawlSpider):
    name = 'article_item'
    allowd_domains = ['wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/Benevolent_dictator_for_life']
    rules = [Rule(LinkExtractor(allow='(/wiki/)((?!:).)*$'), callback = 'parse_items', follow=True)]

    def purse_items(self, response):
        article = Article()
        article['url'] = response.url
        article['title'] = response.css('h1::text').extract_first()
        article['text'] = response.xpath('//div[@id="mw-content-text"]//text()').extract()
        last_updated = response.css('li#footer-info-lastmod::text').extract_first()
        article['last_updated'] = last_updated.replace('This page was last edited on ','')
        return article