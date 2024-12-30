from enum import StrEnum


class Crawler(StrEnum):
    VNEXPRESS = "vnexpress"
    TUOITRE = "tuoitre"


class Spider(StrEnum):
    TOP_ARTICLE_VNEXPRESS = "top_article_vnexpress_spider"
    TOP_ARTICLE_TUOITRE = "top_article_tuoitre_spider"
