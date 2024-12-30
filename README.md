# Hot Articles Crawler Script

## Installation

1. Install dependencies using Poetry:
    ```sh
    poetry install
    ```

2. Init shell
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

```mermaid
flowchart TB
    subgraph UserInterface["User Interface"]
        CLI["Command Line Interface"]
        Config["Input Arguments
        - News Sources
        - Date Range
        - Top N Articles"]
    end

    subgraph CoreSystem["Core System"]
        Manager["Crawler Manager"]
        
        subgraph CrawlerLayer["Crawler Layer"]
            direction TB
            VECrawler["VnExpress Crawler"]
            TTCrawler["TuoiTre Crawler"]
        end
        
        subgraph SpiderLayer["Spider Layer"]
            subgraph NewsSpiders["News Spiders"]
                direction TB
                VESpider["VnExpress Spider"]
                TTSpider["TuoiTre Spider"]
            end 
            subgraph Parsers["Content Parsers"]
                direction TB
                ArticleParser["Article Parser"]
                CommentParser["Comment Parser"]
            end
        end
        
        subgraph DataLayer["Data Layer"]
            direction TB
            Article["Article
            - Title
            - URL
            - Comments
            - Total Comment Likes"]
        end
    end

    subgraph OutputSystem["Output System"]
        FileExport
        ConsoleDisplay
    end

    subgraph RankingEngine["Ranking"]
        direction TB
        subgraph Strategies["Ranking Methods"]
            LikeRanking["Total Comment Like Ranking"]
        end
    end

    %% Flow connections
    CLI --> Manager
    Manager --> CrawlerLayer
    CrawlerLayer --> NewsSpiders
    NewsSpiders --> Parsers
    Parsers --> Article
    Article --> RankingEngine
    RankingEngine --> OutputSystem
    
    UserInterface --> OutputSystem

    %% Styling
    classDef system fill:#f9f,stroke:#333,stroke-width:2px
    classDef component fill:#bfb,stroke:#333,stroke-width:2px
    classDef interface fill:#fbb,stroke:#333,stroke-width:2px
    
    class CoreSystem system
    class RankingEngine component
    class UserInterface,OutputSystem interface
```
