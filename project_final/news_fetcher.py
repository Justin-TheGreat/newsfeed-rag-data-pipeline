#!/usr/bin/env python3
"""
News Fetcher - A Python script to fetch free news feeds and filter by date
Returns the top 5 news items for a specified date
"""

import requests
import feedparser
from datetime import datetime, timedelta
import json
from typing import List, Dict, Optional
import time
from dataclasses import dataclass
from urllib.parse import urlparse
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class NewsItem:
    """Data class to represent a news item"""
    title: str
    description: str
    link: str
    published_date: str
    source: str
    category: Optional[str] = None
    image_url: Optional[str] = None

class NewsFetcher:
    """Class to fetch news from various free sources"""
    
    def __init__(self):
        self.rss_feeds = {
            'BBC': 'http://feeds.bbci.co.uk/news/rss.xml',
            'Reuters': 'http://feeds.reuters.com/reuters/topNews',
            'NBC News': 'https://feeds.nbcnews.com/nbcnews/public/world',
            'ABC News': 'https://abcnews.go.com/abcnews/usheadlines',
            'CBS News': 'https://www.cbsnews.com/latest/rss/main',
            'PBS News': 'https://www.pbs.org/newshour/feed/politics-headlines',
            'CNN': 'http://rss.cnn.com/rss/cnn_topstories.rss',
            'Fox News': 'https://www.foxnews.com/rss',
            'The New York Times': 'https://rss.nytimes.com/services/xml/rss/nyt/World.xml',
            'The Washington Post': 'https://feeds.washingtonpost.com/rss/world'
        }
        
        # Alternative: NewsAPI (requires free API key)
        self.news_api_key = None
        self.news_api_base_url = "https://newsapi.org/v2"
    
    def set_news_api_key(self, api_key: str):
        """Set NewsAPI key for additional news sources"""
        self.news_api_key = api_key
    
    def fetch_rss_news(self, target_date: str = None) -> List[NewsItem]:
        """
        Fetch news from RSS feeds
        
        Args:
            target_date: Date string in YYYY-MM-DD format. If None, fetches today's news.
            
        Returns:
            List of NewsItem objects
        """
        all_news = []
        
        if target_date:
            try:
                target_datetime = datetime.strptime(target_date, "%Y-%m-%d")
                logger.info(f"Fetching news for date: {target_date}")
            except ValueError:
                logger.error(f"Invalid date format: {target_date}. Use YYYY-MM-DD format.")
                return []
        else:
            target_datetime = datetime.now()
            target_date = target_datetime.strftime("%Y-%m-%d")
            logger.info(f"Fetching news for today: {target_date}")
        
        for source_name, feed_url in self.rss_feeds.items():
            try:
                logger.info(f"Fetching from {source_name}...")
                feed = feedparser.parse(feed_url)
                
                for entry in feed.entries:
                    try:
                        # Parse publication date
                        pub_date = self._parse_date(entry.get('published', ''))
                        
                        if pub_date and self._is_same_date(pub_date, target_datetime):
                            news_item = NewsItem(
                                title=entry.get('title', 'No title'),
                                description=entry.get('summary', 'No description'),
                                link=entry.get('link', ''),
                                published_date=pub_date.strftime("%Y-%m-%d %H:%M:%S"),
                                source=source_name,
                                category=self._extract_category(entry),
                                image_url=self._extract_image(entry)
                            )
                            all_news.append(news_item)
                    
                    except Exception as e:
                        logger.warning(f"Error parsing entry from {source_name}: {e}")
                        continue
                
                # Add delay to be respectful to RSS feeds
                time.sleep(0.5)
                
            except Exception as e:
                logger.error(f"Error fetching from {source_name}: {e}")
                continue
        
        logger.info(f"Fetched {len(all_news)} news items for {target_date}")
        return all_news
    
    def fetch_news_api_news(self, target_date: str = None, query: str = "general") -> List[NewsItem]:
        """
        Fetch news from NewsAPI (requires API key)
        
        Args:
            target_date: Date string in YYYY-MM-DD format
            query: Search query for news
            
        Returns:
            List of NewsItem objects
        """
        if not self.news_api_key:
            logger.warning("NewsAPI key not set. Skipping NewsAPI fetch.")
            return []
        
        if target_date:
            try:
                target_datetime = datetime.strptime(target_date, "%Y-%m-%d")
                from_date = target_datetime.strftime("%Y-%m-%d")
                to_date = target_datetime.strftime("%Y-%m-%d")
            except ValueError:
                logger.error(f"Invalid date format: {target_date}")
                return []
        else:
            from_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
            to_date = datetime.now().strftime("%Y-%m-%d")
        
        url = f"{self.news_api_base_url}/everything"
        params = {
            'q': query,
            'from': from_date,
            'to': to_date,
            'sortBy': 'relevancy',
            'apiKey': self.news_api_key,
            'language': 'en',
            'pageSize': 100
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            news_items = []
            
            for article in data.get('articles', []):
                news_item = NewsItem(
                    title=article.get('title', 'No title'),
                    description=article.get('description', 'No description'),
                    link=article.get('url', ''),
                    published_date=article.get('publishedAt', ''),
                    source=article.get('source', {}).get('name', 'Unknown'),
                    category=query,
                    image_url=article.get('urlToImage')
                )
                news_items.append(news_item)
            
            logger.info(f"Fetched {len(news_items)} news items from NewsAPI for {target_date}")
            return news_items
            
        except Exception as e:
            logger.error(f"Error fetching from NewsAPI: {e}")
            return []
    
    def get_top_news(self, target_date: str = None, limit: int = 5, 
                     use_news_api: bool = False, query: str = "general") -> List[NewsItem]:
        """
        Get top news items for a specific date
        
        Args:
            target_date: Date string in YYYY-MM-DD format
            limit: Number of top news items to return
            use_news_api: Whether to also use NewsAPI
            query: Search query for NewsAPI
            
        Returns:
            List of top NewsItem objects
        """
        all_news = []
        
        # Fetch from RSS feeds
        rss_news = self.fetch_rss_news(target_date)
        all_news.extend(rss_news)
        
        # Fetch from NewsAPI if requested
        if use_news_api:
            api_news = self.fetch_news_api_news(target_date, query)
            all_news.extend(api_news)
        
        # Sort by relevance (you can implement custom ranking logic here)
        # For now, we'll sort by source reliability and date
        source_priority = {
            'BBC': 1, 'Reuters': 2, 'AP News': 3, 'NPR': 4, 'The Guardian': 5
        }
        
        def sort_key(news_item):
            priority = source_priority.get(news_item.source, 999)
            return (priority, news_item.published_date)
        
        all_news.sort(key=sort_key)
        
        # Return top N items
        top_news = all_news[:limit]
        
        logger.info(f"Returning top {len(top_news)} news items for {target_date}")
        return top_news
    
    def _parse_date(self, date_string: str) -> Optional[datetime]:
        """Parse various date formats from RSS feeds"""
        date_formats = [
            "%a, %d %b %Y %H:%M:%S %z",
            "%a, %d %b %Y %H:%M:%S %Z",
            "%Y-%m-%dT%H:%M:%SZ",
            "%Y-%m-%dT%H:%M:%S%z",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d"
        ]
        
        for fmt in date_formats:
            try:
                return datetime.strptime(date_string, fmt)
            except ValueError:
                continue
        
        return None
    
    def _is_same_date(self, date1: datetime, date2: datetime) -> bool:
        """Check if two dates are the same day"""
        return date1.date() == date2.date()
    
    def _extract_category(self, entry) -> Optional[str]:
        """Extract category from RSS entry"""
        # Try different possible category fields
        category_fields = ['category', 'tags', 'section']
        for field in category_fields:
            if hasattr(entry, field) and entry[field]:
                return entry[field]
        return None
    
    def _extract_image(self, entry) -> Optional[str]:
        """Extract image URL from RSS entry"""
        # Try different possible image fields
        if hasattr(entry, 'media_content') and entry.media_content:
            return entry.media_content[0].get('url')
        elif hasattr(entry, 'media_thumbnail') and entry.media_thumbnail:
            return entry.media_thumbnail[0].get('url')
        elif hasattr(entry, 'enclosures') and entry.enclosures:
            for enclosure in entry.enclosures:
                if enclosure.get('type', '').startswith('image/'):
                    return enclosure.get('href')
        return None

def print_news_summary(news_items: List[NewsItem]):
    """Print a formatted summary of news items"""
    if not news_items:
        print("No news items found for the specified date.")
        return
    
    print(f"\n{'='*80}")
    print(f"TOP {len(news_items)} NEWS ITEMS")
    print(f"{'='*80}\n")
    
    for i, item in enumerate(news_items, 1):
        print(f"{i}. {item.title}")
        print(f"   Source: {item.source}")
        print(f"   Date: {item.published_date}")
        if item.category:
            print(f"   Category: {item.category}")
        print(f"   Description: {item.description[:150]}{'...' if len(item.description) > 150 else ''}")
        print(f"   Link: {item.link}")
        if item.image_url:
            print(f"   Image: {item.image_url}")
        print("-" * 80)

def main():
    """Main function to demonstrate usage"""
    print("News Fetcher - Free News Feed with Date Filtering")
    print("=" * 50)
    
    # Initialize news fetcher
    fetcher = NewsFetcher()
    
    # Option 1: Set NewsAPI key if you have one (optional)
    # fetcher.set_news_api_key("your_api_key_here")
    
    # Get today's top 5 news
    print("\nFetching today's top 5 news...")
    today_news = fetcher.get_top_news(limit=5)
    print_news_summary(today_news)
    
    # Get news for a specific date (example: yesterday)
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    print(f"\nFetching top 5 news for {yesterday}...")
    yesterday_news = fetcher.get_top_news(target_date=yesterday, limit=5)
    print_news_summary(yesterday_news)
    
    # Example with NewsAPI (if you have an API key)
    # print("\nFetching technology news from NewsAPI...")
    # tech_news = fetcher.get_top_news(
    #     target_date=datetime.now().strftime("%Y-%m-%d"),
    #     limit=5,
    #     use_news_api=True,
    #     query="technology"
    # )
    # print_news_summary(tech_news)

if __name__ == "__main__":
    main()
