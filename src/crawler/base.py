from abc import ABC, abstractmethod
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class BaseCrawler(ABC):
    DEFAULT_SETTINGS = {
        "LOG_LEVEL": "ERROR",
        "DOWNLOAD_DELAY": 0.1,
        "CONCURRENT_REQUESTS": 16,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 8,
    }

    USER_AGENT_SETTINGS = {
        "FAKEUSERAGENT_PROVIDERS": [
            "scrapy_fake_useragent.providers.FakeUserAgentProvider",
            "scrapy_fake_useragent.providers.FakerProvider",
            "scrapy_fake_useragent.providers.FixedUserAgentProvider",
        ],
        "FAKEUSERAGENT_FALLBACK": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/",
    }

    def __init__(self, ranking, start_date, end_date, settings_options=None):
        self.ranking = ranking
        self.start_date = start_date
        self.end_date = end_date
        self.settings_options = settings_options or {}
        self.process = self._create_crawler_process()

    def _create_crawler_process(self):
        settings = get_project_settings()

        combined_settings = self.DEFAULT_SETTINGS.copy()
        combined_settings.update(self.USER_AGENT_SETTINGS)

        custom_settings = self.settings_options.get("custom_settings", {})

        combined_settings.update(custom_settings)
        settings.update(combined_settings)

        return CrawlerProcess(settings)

    @abstractmethod
    def get_article_spider(self):
        pass

    def crawl_article(self):
        spider_class = self.get_article_spider()
        self.process.crawl(
            spider_class,
            ranking=self.ranking,
            start_date=self.start_date,
            end_date=self.end_date,
        )
