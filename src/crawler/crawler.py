from src.crawler.base import BaseCrawler
from src.spider.spider import VnExpressSpider, TuoiTreSpider


class VnExpressCrawler(BaseCrawler):
    def get_article_spider(self):
        return VnExpressSpider


class TuoiTreCrawler(BaseCrawler):
    def get_article_spider(self):
        return TuoiTreSpider
