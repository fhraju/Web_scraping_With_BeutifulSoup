"""
a spider that crawls Wikipedia, identifying all article pages and flagging nonarticle pages
"""
from turtle import title
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class ArticlSpider(CrawlSpider):
    name = 'articles'
    allowed_domain = ['wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/Benevolent_dictator_for_life']
    rules = [Rule(LinkExtractor(allow='^(/wiki/)((?!:).)*$'), callback='parse_items', follow=True, cb_kwargs={'is_article': False})]

    def parse_items(self, response, is_article):
        print(response.url)
        title = response.css('h1::text').extract_first()
        if is_article:
            url = response.url
            text = response.xpath('//div[@id="mw-content-text"]''//text()').extract()
            last_updated = response.css('li#footer-info-lastmod''::text').extract_first()
            last_updated = last_updated.replace('This page was last edited on ','')
            print("Title is: {}".format(title))
            print("title is: {}".format(title))
            print("text is: {}".format(text))
        else:
            print("This is not an article: {}".format(title))
