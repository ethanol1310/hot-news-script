import json
import traceback
from datetime import datetime, timedelta

import scrapy

from src.model.article import Article, VnExpressCategory

from src.logger import logger
from src.utils.constant import Spider


class VnExpressSpider(scrapy.Spider):
    name = Spider.ARTICLE_VNEXPRESS
    allowed_domains = ["vnexpress.net", "usi-saas.vnexpress.net"]

    def __init__(self, ranking, start_date, end_date, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ranking = ranking
        self.base_url = "https://vnexpress.net"
        self.comment_api_url = "https://usi-saas.vnexpress.net/index/get"
        self.start_date_unix = int(start_date.timestamp())
        self.end_date_unix = int(end_date.timestamp())

    def start_requests(self):
        logger.info(
            f"Start date: {datetime.fromtimestamp(self.start_date_unix)} - End date: {datetime.fromtimestamp(self.end_date_unix)}"
        )
        categories = self.fetch_categories()
        for category in categories:
            url = f"{self.base_url}/category/day/cateid/{category.id}/fromdate/{self.start_date_unix}/todate/{self.end_date_unix}/allcate/0/page/1"
            yield scrapy.Request(
                url=url, callback=self.parse, meta={"category": category}
            )

    def parse(self, response):
        articles = response.css("article.item-news.item-news-common")
        for article in articles:
            link = article.css("a::attr(href)").get()
            title = article.css("a::attr(title)").get()
            if link and title:
                yield scrapy.Request(
                    url=link,
                    callback=self.parse_article,
                    meta={"title": title, "url": link},
                )

        if articles:
            category = response.meta["category"]
            current_page = int(response.url.split("page/")[-1])
            next_page = current_page + 1
            next_url = f"{self.base_url}/category/day/cateid/{category.id}/fromdate/{self.start_date_unix}/todate/{self.end_date_unix}/allcate/0/page/{next_page}"
            yield scrapy.Request(
                url=next_url, callback=self.parse, meta={"category": category}
            )

    def parse_article(self, response):
        try:
            object_id = response.css(
                "span.number_cmt.txt_num_comment.num_cmt_detail::attr(data-objectid)"
            ).get()
            if object_id:
                object_type = response.css(
                    "span.number_cmt.txt_num_comment.num_cmt_detail::attr(data-objecttype)"
                ).get()
                if object_id and object_type:
                    url = f"{self.comment_api_url}?offset=0&limit=1000&sort_by=like&objectid={object_id}&objecttype={object_type}&siteid=1000000"
                    yield scrapy.Request(
                        url=url,
                        callback=self.parse_comments,
                        meta={
                            "title": response.meta["title"],
                            "url": response.meta["url"],
                        },
                    )
            else:
                self.ranking.add_article(
                    Article(response.meta["title"], response.meta["url"], 0)
                )
        except Exception as e:
            logger.error(message=f"Exception:{e}\n traceback:{traceback.format_exc()}")

    def parse_comments(self, response):
        try:
            data = response.json()
            if data is None:
                logger.warn(f"Empty response: {response.url}")
                return
            comments = data.get("data", {}).get("items", [])
            total_likes = sum(comment["userlike"] for comment in comments)
            self.ranking.add_article(
                Article(response.meta["title"], response.meta["url"], total_likes)
            )
        except Exception as e:
            logger.error(msg=f"Exception:{e}\n traceback:{traceback.format_exc()}")

    def fetch_categories(self):
        return [
            VnExpressCategory(
                name="Thời sự", id=1001005, class_name="thoisu", share_url="/thoi-su"
            ),
            VnExpressCategory(
                name="Góc nhìn", id=1003450, class_name="gocnhin", share_url="/goc-nhin"
            ),
            VnExpressCategory(
                name="Thế giới", id=1001002, class_name="thegioi", share_url="/the-gioi"
            ),
            VnExpressCategory(
                name="Video",
                id=1003834,
                class_name="video",
                share_url="https://video.vnexpress.net",
            ),
            VnExpressCategory(
                name="Podcasts", id=1004685, class_name="podcasts", share_url="/podcast"
            ),
            VnExpressCategory(
                name="Kinh doanh",
                id=1003159,
                class_name="kinhdoanh",
                share_url="/kinh-doanh",
            ),
            VnExpressCategory(
                name="Bất động sản",
                id=1005628,
                class_name="kinhdoanh",
                share_url="/bat-dong-san",
            ),
            VnExpressCategory(
                name="Khoa học", id=1001009, class_name="khoahoc", share_url="/khoa-hoc"
            ),
            VnExpressCategory(
                name="Giải trí", id=1002691, class_name="giaitri", share_url="/giai-tri"
            ),
            VnExpressCategory(
                name="Thể thao", id=1002565, class_name="thethao", share_url="/the-thao"
            ),
            VnExpressCategory(
                name="Pháp luật",
                id=1001007,
                class_name="phapluat",
                share_url="/phap-luat",
            ),
            VnExpressCategory(
                name="Giáo dục", id=1003497, class_name="giaoduc", share_url="/giao-duc"
            ),
            VnExpressCategory(
                name="Sức khỏe", id=1003750, class_name="suckhoe", share_url="/suc-khoe"
            ),
            VnExpressCategory(
                name="Đời sống", id=1002966, class_name="doisong", share_url="/doi-song"
            ),
            VnExpressCategory(
                name="Du lịch", id=1003231, class_name="dulich", share_url="/du-lich"
            ),
            VnExpressCategory(
                name="Số hóa", id=1002592, class_name="sohoa", share_url="/so-hoa"
            ),
            VnExpressCategory(
                name="Xe", id=1001006, class_name="xe", share_url="/oto-xe-may"
            ),
            VnExpressCategory(
                name="Ý kiến", id=1001012, class_name="ykien", share_url="/y-kien"
            ),
            VnExpressCategory(
                name="Tâm sự", id=1001014, class_name="tamsu", share_url="/tam-su"
            ),
            VnExpressCategory(
                name="Thư giãn", id=1001011, class_name="cuoi", share_url="/thu-gian"
            ),
        ]


class TuoiTreSpider(scrapy.Spider):
    name = Spider.ARTICLE_TUOITRE
    allowed_domains = ["tuoitre.vn", "id.tuoitre.vn"]

    def __init__(self, ranking, start_date, end_date, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ranking = ranking
        self.base_url = "https://tuoitre.vn"
        self.comment_api_url = "https://id.tuoitre.vn/api/getlist-comment.api"
        self.start_date = start_date
        self.end_date = end_date

    def start_requests(self):
        logger.info(f"Start date: {self.start_date} - End date: {self.end_date}")
        current_date = self.start_date
        while current_date <= self.end_date:
            date_str = current_date.strftime("%d-%m-%Y")
            url = f"{self.base_url}/timeline-xem-theo-ngay/0/{date_str}/trang-1.htm"
            yield scrapy.Request(
                url=url, callback=self.parse, meta={"date": date_str, "page": 1}
            )
            current_date += timedelta(days=1)

    def parse(self, response):
        articles = response.css("li.news-item")
        for article in articles:
            link = article.css("a::attr(href)").get()
            title = article.css("a::attr(title)").get()
            if link and title:
                article_url = f"{self.base_url}{link}"
                yield scrapy.Request(
                    url=article_url,
                    callback=self.parse_article,
                    meta={"title": title, "url": article_url},
                )

        if articles:
            date = response.meta["date"]
            current_page = response.meta["page"]
            next_page = current_page + 1
            next_url = (
                f"{self.base_url}/timeline-xem-theo-ngay/0/{date}/trang-{next_page}.htm"
            )
            yield scrapy.Request(
                url=next_url,
                callback=self.parse,
                meta={"date": date, "page": next_page},
            )

    def parse_article(self, response):
        try:
            comment_section = response.css("section.comment-wrapper")
            if comment_section:
                object_id = comment_section.css("::attr(data-objectid)").get()
                object_type = comment_section.css("::attr(data-objecttype)").get()
                if object_id and object_type:
                    url = f"{self.comment_api_url}?pageindex=1&objId={object_id}&objType={object_type}&sort=2"
                    yield scrapy.Request(
                        url=url,
                        callback=self.parse_comments,
                        meta={
                            "title": response.meta["title"],
                            "url": response.meta["url"],
                            "object_id": object_id,
                            "object_type": object_type,
                            "page": 1,
                            "total_likes": 0,
                        },
                    )
        except Exception as e:
            logger.error(msg=f"Exception:{e}\n traceback:{traceback.format_exc()}")

    def parse_comments(self, response):
        try:
            data = response.json()
            if data is None:
                logger.warn(f"Empty response: {response.url}")
                return
            comments = json.loads(data.get("Data", "[]"))
            total_likes = response.meta["total_likes"] + sum(
                sum(comment.get("reactions", {}).values()) for comment in comments
            )

            if comments:
                page = response.meta["page"] + 1
                url = f"{self.comment_api_url}?pageindex={page}&objId={response.meta['object_id']}&objType={response.meta['object_type']}&sort=2"
                yield scrapy.Request(
                    url=url,
                    callback=self.parse_comments,
                    meta={
                        "title": response.meta["title"],
                        "url": response.meta["url"],
                        "total_likes": total_likes,
                        "object_id": response.meta["object_id"],
                        "object_type": response.meta["object_type"],
                        "page": page,
                    },
                )
            else:
                self.ranking.add_article(
                    Article(response.meta["title"], response.meta["url"], total_likes)
                )
        except Exception as e:
            logger.error(msg=f"Exception:{e}\n traceback:{traceback.format_exc()}")
