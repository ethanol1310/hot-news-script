from news_crawl.crawler.base import BaseCrawler
from news_crawl.spider.spider import VnExpressTopArticleSpider, TuoiTreTopArticleSpider


class VnExpressCrawler(BaseCrawler):
    def get_top_article_spider(self):
        return VnExpressTopArticleSpider


class TuoiTreCrawler(BaseCrawler):
    def get_top_article_spider(self):
        return TuoiTreTopArticleSpider
