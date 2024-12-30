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
- Mermaid Diagram - Supported by Claude
```mermaid
flowchart TB
    subgraph UserInterface["User Interface"]
        CLI["Command Line Interface"]
        Config["Input Arguments
        - News Sources
        - Date Range
        - Top N Articles"]
    end

    subgraph CoreSystem["Crawl System"]
        Manager["Crawler Manager"]
        
        subgraph CrawlerLayer["Crawler Layer"]
            direction BT
            VECrawler["VnExpress Crawler"]
            TTCrawler["TuoiTre Crawler"]
        end
        
        subgraph SpiderLayer["Spider Layer"]
            subgraph NewsSpiders["News Spiders"]
                direction RL
                VESpider["VnExpress Spider"]
                TTSpider["TuoiTre Spider"]
            end 
            subgraph Parsers["Content Parsers"]
                direction RL
                ArticleParser["Article Parser"]
                CommentParser["Comment Parser"]
            end
        end
    end

    subgraph OutputSystem["Output System"]
        FileExport
        ConsoleDisplay
    end

    subgraph Model["Model"]
        subgraph RankingEngine["Arregate"]
            direction RL
            subgraph Strategies["Ranking Methods"]
                LikeRanking["Total Comment Like Ranking"]
            end
        end
        subgraph DataLayer["Data"]
                direction RL
                Article["Article
                - Title
                - URL
                - Comments
                - Total Comment Likes"]
        end
    end 

    %% Flow connections
    CLI --> Manager
    Manager --> CrawlerLayer
    CrawlerLayer --> SpiderLayer
    NewsSpiders --> Parsers
    SpiderLayer --> Model
    
    DataLayer --> RankingEngine

    RankingEngine --> OutputSystem
    UserInterface --> OutputSystem

    %% Styling
    classDef system fill:#f9f,stroke:#333,stroke-width:2px
    classDef component fill:#bfb,stroke:#333,stroke-width:2px
    classDef interface fill:#fbb,stroke:#333,stroke-width:2px
    
    class CoreSystem,Model system
    class RankingEngine,CrawlerLayer,SpiderLayer,DataLayer component
    class UserInterface,OutputSystem interface
```
