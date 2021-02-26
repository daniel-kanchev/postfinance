import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from postfinance.items import Article


class PostfinanceSpider(scrapy.Spider):
    name = 'postfinance'
    start_urls = ['https://www.postfinance.ch/en/about-us/media/newsroom.morenews.html']

    def parse(self, response):
        links = response.xpath('//a[@class="news_wall--item"]/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        if 'pdf' in response.url:
            return

        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h1[@class="newsheader--title"]/text()').get()
        if title:
            title = title.strip()

        date = response.xpath('//span[@class="newsheader--date"]/text()').get()
        if date:
            date = date.strip()

        content = response.xpath('//div[@class="articletext-component"]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
