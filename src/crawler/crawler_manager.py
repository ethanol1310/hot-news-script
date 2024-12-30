from src.logger import logger


class CrawlerManager:
    def __init__(self, crawlers):
        self.crawlers = crawlers

    def run_top_article_crawlers(self):
        for site_name, crawler in self.crawlers.items():
            logger.info(f"Starting crawl for {site_name}...")
            crawler.crawl_top_article()

    def get_top_articles_by_crawler(self, crawler):
        return self.crawlers[crawler].tracker.get_top_articles()
