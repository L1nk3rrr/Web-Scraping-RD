import scrapy
from quotes.items import QuotesItem

MAX_PAGE = 2
START_PAGE = 1

QUOTES_XPATH = ".//div[@class='quote']"
AUTHOR_XPATH = ".//small[@itemprop='author']/text()"
TEXT_XPATH = ".//span[@class='text']/text()"


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
        quotes = response.xpath(QUOTES_XPATH)
        for quote in quotes:
            author = quote.xpath(AUTHOR_XPATH).get()
            text = quote.xpath(TEXT_XPATH).get()
            yield QuotesItem(author=author, text=text)
