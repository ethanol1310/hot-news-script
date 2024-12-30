import argparse
import os
from datetime import datetime, timedelta
import time
import pytz
from news_crawl.model.article import ArticleTracker
from news_crawl.crawler.crawler import VnExpressCrawler, TuoiTreCrawler
from news_crawl.crawler.crawler_manager import CrawlerManager
from news_crawl.utils.constant import Crawler


def get_available_crawlers():
    return {
        Crawler.VNEXPRESS: lambda tracker, start_date, end_date, setting_options: VnExpressCrawler(
            tracker, start_date, end_date, setting_options
        ),
        Crawler.TUOITRE: lambda tracker, start_date, end_date, setting_options: TuoiTreCrawler(
            tracker, start_date, end_date, setting_options
        ),
    }


def validate_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"Invalid date format: {date_str}. Use YYYY-MM-DD"
        )


def print_top_articles(manager, crawler_name, top):
    top_articles = manager.get_top_articles_by_crawler(crawler_name)
    print(f"\n{'='*50}")
    print(f"Results for {crawler_name}")
    print(f"Total articles: {len(top_articles)}")
    print(f"{'='*50}")

    if not top_articles:
        print("No articles found")
        return

    for i, article in enumerate(top_articles[:10], 1):
        print(f"\n{i}. {article.title}")
        print(f"   URL: {article.url}")
        print(f"   Likes: {article.total_likes}")


def export_top_articles(
    manager, crawler_name, top, start_date, end_date, output_dir="output"
):
    top_articles = manager.get_top_articles_by_crawler(crawler_name)
    start_date_str = start_date.strftime("%Y%m%d")
    end_date_str = end_date.strftime("%Y%m%d")
    output_file = os.path.join(
        output_dir, f"{crawler_name}_{top}_{start_date_str}_{end_date_str}.txt"
    )

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(output_file, "w") as file:
        if not top_articles:
            file.write("No articles found\n")
            return

        for i, article in enumerate(top_articles[:top], 1):
            file.write(
                f"{i}. {article.title} - {article.url} - Likes: {article.total_likes}\n"
            )
    print(f"Top articles for {crawler_name} have been written to {output_file}")


def get_date_range(arg_start_date, arg_end_date):
    timezone_vn = pytz.timezone("Asia/Bangkok")
    today = datetime.now(timezone_vn)

    start_date = arg_start_date or (today - timedelta(days=7))
    end_date = arg_end_date or today

    start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
    end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=999999)

    start_date = timezone_vn.localize(start_date)
    end_date = timezone_vn.localize(end_date)

    return start_date, end_date


def main():
    parser = argparse.ArgumentParser(description="Top News Crawler")
    parser.add_argument(
        "--crawler",
        default=Crawler.VNEXPRESS,
        help="Specify which crawlers to run (vnexpress, tuoitre)",
    )
    parser.add_argument(
        "--top", default=10, help="Number of top articles to display (default: 10)"
    )
    parser.add_argument(
        "--start-date",
        type=validate_date,
        help="Start date in YYYY-MM-DD format (default: 7 days ago)",
    )
    parser.add_argument(
        "--end-date",
        type=validate_date,
        help="End date in YYYY-MM-DD format (default: today)",
    )

    args = parser.parse_args()
    start_date, end_date = get_date_range(args.start_date, args.end_date)

    crawler_name = args.crawler
    settings_options = {
        "custom_settings": {
            "DOWNLOAD_DELAY": 0.0,
            "HTTPCACHE_ENABLED": True,
            "HTTPCACHE_EXPIRATION_SECS": 600,
            "HTTPCACHE_DIR": "httpcache",
        },
    }
    crawlers = {}
    available_crawler = get_available_crawlers()
    crawlers[crawler_name] = available_crawler[crawler_name](
        ArticleTracker(), start_date, end_date, settings_options
    )
    print(f"Initialized {crawler_name} crawler")

    if not crawlers:
        print("No valid crawlers specified")
        return

    manager = CrawlerManager(crawlers)

    try:
        print(f"\nCrawling top articles from {start_date} to {end_date}")
        print(f"Selected crawler: {args.crawler}\n")
        start_process_time = time.time()

        manager.run_top_article_crawlers()
        for crawler in crawlers.values():
            crawler.process.start(stop_after_crawl=True)
            end_process_time = time.time()
        elapsed_time = end_process_time - start_process_time

        print(f"\n{'='*50}")
        print(f"\nCrawling completed in {elapsed_time:.2f} seconds")
        print(f"\n{'='*50}")

        for crawler_name in crawlers.keys():
            print_top_articles(manager, crawler_name, args.top)
            export_top_articles(manager, crawler_name, args.top, start_date, end_date)

    except KeyboardInterrupt:
        print("\nStopping crawlers...")
    except Exception as e:
        print(f"Error during crawling: {e}")


if __name__ == "__main__":
    main()
