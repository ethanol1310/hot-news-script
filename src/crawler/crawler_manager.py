from src.logger import logger


class CrawlerManager:
    def __init__(self, crawlers):
        self.crawlers = crawlers

    def run_article_crawlers(self):
        for site_name, crawler in self.crawlers.items():
            logger.info(f"Starting crawl for {site_name}...")
            crawler.crawl_article()

    def ranking(self, crawler):
        return self.crawlers[crawler].ranking.ranking_by_total_comment_likes()
