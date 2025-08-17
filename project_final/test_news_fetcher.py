#!/usr/bin/env python3
"""
Simple test script for the News Fetcher
Tests basic functionality without making too many requests
"""

from news_fetcher import NewsFetcher, print_news_summary
from datetime import datetime

def test_basic_functionality():
    """Test basic news fetcher functionality"""
    print("🧪 Testing News Fetcher Basic Functionality")
    print("=" * 50)
    
    # Initialize fetcher
    fetcher = NewsFetcher()
    print("✅ NewsFetcher initialized successfully")
    
    # Test RSS feeds configuration
    print(f"✅ Available RSS sources: {len(fetcher.rss_feeds)}")
    for source in list(fetcher.rss_feeds.keys())[:3]:  # Show first 3
        print(f"   - {source}")
    
    # Test date parsing
    test_date = "2024-01-15"
    try:
        parsed_date = datetime.strptime(test_date, "%Y-%m-%d")
        print(f"✅ Date parsing works: {test_date} -> {parsed_date}")
    except ValueError as e:
        print(f"❌ Date parsing failed: {e}")
    
    # Test NewsItem creation
    from news_fetcher import NewsItem
    test_item = NewsItem(
        title="Test News",
        description="This is a test news item",
        link="https://example.com",
        published_date="2024-01-15 10:00:00",
        source="Test Source"
    )
    print(f"✅ NewsItem creation works: {test_item.title}")
    
    print("\n🎯 Basic functionality tests completed successfully!")
    print("💡 Run 'python news_fetcher.py' to fetch actual news")
    print("💡 Run 'python example_usage.py' to see comprehensive examples")

if __name__ == "__main__":
    test_basic_functionality()
