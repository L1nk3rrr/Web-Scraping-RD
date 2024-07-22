from scrapy import signals

from utils.scrape_ops_fake_agent import get_user_agent_list, get_random_user_agent

USER_AGENT_LIST = get_user_agent_list()


class CustomUserAgentMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        request.headers["User-Agent"] = get_random_user_agent(USER_AGENT_LIST)

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)
