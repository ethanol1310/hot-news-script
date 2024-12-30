Sure, here is a basic `README.md` for your project:

# News Crawl

## Description
`news-crawl` is a Python-based web scraping project that uses Scrapy to crawl and extract news articles and their associated comments from various news websites.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/news-crawl.git
    cd news-crawl
    ```

2. Install dependencies using Poetry:
    ```sh
    poetry install
    ```

3. Init shell
    ```sh
    poetry shell
   ```

## Usage

1. To run the spider, use the following command:
    ```sh
   # run last 7 days (default)
     poetry run python main.py --crawler=vnexpress 
   
   # run from start_date to end_date
     poetry run python main.py --crawler=tuoitre --start_date=YYYY-MM-DD --end_date=YYYY-MM-DD
    ```

## Project Structure

- `pyproject.toml`: Configuration file for Poetry, including project dependencies.


