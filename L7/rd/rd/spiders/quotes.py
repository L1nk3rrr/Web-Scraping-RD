import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/login"]

    def parse(self, response):
        token = response.xpath("//input[@name='csrf_token']/@value").get()
        return scrapy.FormRequest.from_response(
            response,
            formdata={
                "csrf_token": token,
                "username": 'admin',
                "password": 'admin'
            },
            callback=self.after_login
        )

    def after_login(self, response):
        logout = response.xpath("//a[@href='/logout']/text()").get()
        yield {
            "is_logout": logout
        }
