import scrapy
from scrapy import Selector,Request
from scrapy.http import HtmlResponse

from spider202301.items import MovieItem


class DoubanSpider(scrapy.Spider):
    name = "douban"
    allowed_domains = ["movie.douban.com"]
    start_urls = ["https://movie.douban.com/top250"]

    def start_requests(self):
        for page in range(10):
            yield Request(url=f'https://movie.douban.com/top250?start={page*25}&filter=')

    def parse(self, response:HtmlResponse):
        sel=Selector(response)
        ls_items=sel.css('#content > div > div.article > ol > li')
        for ls_item in ls_items:
            movie_item=MovieItem()
            movie_item['title']=ls_item.css('span.title::text').extract_first()
            movie_item['rank']=ls_item.css('span.rating_num::text').extract_first()
            movie_item['subject']=ls_item.css('span.inq::text').extract_first()
            yield movie_item



