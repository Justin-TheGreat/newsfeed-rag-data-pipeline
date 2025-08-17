#!/usr/bin/env python3
"""
Example usage of the News Fetcher
Demonstrates how to fetch news for different dates and get top 5 results
"""

from news_fetcher import NewsFetcher, print_news_summary
from datetime import datetime, timedelta

def main():
    """Example usage of the NewsFetcher class"""
    
    # Initialize the news fetcher
    fetcher = NewsFetcher()
    
    print("🚀 News Fetcher Example Usage")
    print("=" * 50)
    
    # Example 1: Get today's top 5 news
    print("\n📅 Example 1: Today's Top 5 News")
    print("-" * 40)
    today_news = fetcher.get_top_news(limit=5)
    print_news_summary(today_news)
    
    # Example 2: Get yesterday's top 5 news
    print("\n📅 Example 2: Yesterday's Top 5 News")
    print("-" * 40)
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    yesterday_news = fetcher.get_top_news(target_date=yesterday, limit=5)
    print_news_summary(yesterday_news)
    
    # Example 3: Get news for a specific date (last week)
    print("\n📅 Example 3: Last Week's Top 5 News")
    print("-" * 40)
    last_week = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    last_week_news = fetcher.get_top_news(target_date=last_week, limit=5)
    print_news_summary(last_week_news)
    
    # Example 4: Get news for a specific date (custom date)
    print("\n📅 Example 4: Custom Date News (2024-01-15)")
    print("-" * 40)
    custom_date = "2024-01-15"
    custom_news = fetcher.get_top_news(target_date=custom_date, limit=5)
    print_news_summary(custom_news)
    
    # Example 5: Get top 3 news instead of 5
    print("\n📅 Example 5: Today's Top 3 News")
    print("-" * 40)
    top_3_news = fetcher.get_top_news(limit=3)
    print_news_summary(top_3_news)
    
    # Example 6: Using NewsAPI (if you have an API key)
    print("\n📅 Example 6: NewsAPI Integration (Optional)")
    print("-" * 40)
    print("To use NewsAPI, uncomment the following lines and add your API key:")
    print("fetcher.set_news_api_key('your_api_key_here')")
    print("tech_news = fetcher.get_top_news(")
    print("    target_date=datetime.now().strftime('%Y-%m-%d'),")
    print("    limit=5,")
    print("    use_news_api=True,")
    print("    query='technology'")
    print(")")
    
    # Example 7: Filter news by source
    print("\n📅 Example 7: Filter by Source")
    print("-" * 40)
    all_news = fetcher.fetch_rss_news()
    bbc_news = [item for item in all_news if item.source == 'BBC'][:3]
    print(f"Top 3 BBC news items:")
    print_news_summary(bbc_news)

if __name__ == "__main__":
    main()
