import scrapy
from quotes.items import QuotesItem

MAX_PAGE = 2
START_PAGE = 1


class QuotesspiderSpider(scrapy.Spider):
    name = "quotesspider"
    allowed_domains = ["quotes.toscrape.com"]
    base_url = "http://quotes.toscrape.com"
    start_urls = ["https://quotes.toscrape.com"]

    custom_settings = {
        "ITEM_PIPELINES": {
            'quotes.pipelines.QuotesPipeline': 300,
        },
        "FEEDS": {
            "scraped_data/%(name)s_%(time)s.csv": {"format": "csv", },
            "scraped_data/%(name)s_%(time)s.json": {"format": "json", },
        }
    }

    def parse(self, response):
        for page in range(START_PAGE, MAX_PAGE + 1):
            next_page_url = f"{self.base_url}/page/{page}"
            yield response.follow(next_page_url, callback=self.parse_page)

    def parse_page(self, response):
        quotes = response.xpath(".//div[@class='quote']")
        for quote in quotes:
            author = quote.xpath(".//small[@itemprop='author']/text()").get()
            text = quote.xpath(".//span[@class='text']/text()").get()
            yield QuotesItem(author=author, text=text)
