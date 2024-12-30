from enum import StrEnum


class Crawler(StrEnum):
    VNEXPRESS = "vnexpress"
    TUOITRE = "tuoitre"


class Spider(StrEnum):
    ARTICLE_VNEXPRESS = "article_vnexpress_spider"
    ARTICLE_TUOITRE = "article_tuoitre_spider"
