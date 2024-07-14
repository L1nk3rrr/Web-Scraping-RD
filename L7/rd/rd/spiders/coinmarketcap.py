import scrapy


class CoinmarketcapSpider(scrapy.Spider):
    name = "coinmarketcap"
    allowed_domains = ["coinmarketcap.com"]
    start_urls = ["https://coinmarketcap.com/"]
    max_count_follow = 1

    custom_settings = {
        'DOWNLOAD_DELAY': 1
    }

    def parse(self, response):
        rows = response.xpath("//table[contains(@class, 'cmc-table')]/tbody/tr")
        name_xpath = ".//p[contains(@class, 'coin-item-symbol')]/text()|.//span[@class='crypto-symbol']/text()"
        price_xpath = "./td[4]/div/span/text()|./td[4]/text()"
        for row in rows:
            name = row.xpath(name_xpath).get()
            price = row.xpath(price_xpath).getall() # ['$', '0.13'] or ['0.13']
            price = "".join(price)

            yield {
                'name': name,
                'price': price,
            }

        next_btn = response.xpath("//li[@class='next']/a/@href").get()
        if next_btn and self.max_count_follow:
            self.max_count_follow -= 1
            yield response.follow(next_btn, callback=self.parse)
