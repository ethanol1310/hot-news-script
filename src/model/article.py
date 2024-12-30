from src.logger import logger


class Article:
    def __init__(self, title, url, total_likes):
        self.title = title
        self.url = url
        self.total_likes = total_likes

    def __lt__(self, other):
        return self.total_likes < other.total_likes


class ArticleTracker:
    def __init__(self):
        self.articles = []

    def add_article(self, article):
        self.articles.append(article)
        logger.info(f"Added article: {article.url} - Likes: {article.total_likes}")

    def get_top_articles(self):
        self.articles.sort(reverse=True, key=lambda x: x.total_likes)
        return self.articles


class VnExpressCategory:
    def __init__(self, name, id, class_name, share_url):
        self.name = name
        self.id = id
        self.class_name = class_name
        self.share_url = share_url

    def __repr__(self):
        return f"Category(name='{self.name}', id={self.id}, class_name='{self.class_name}', share_url='{self.share_url}')"
