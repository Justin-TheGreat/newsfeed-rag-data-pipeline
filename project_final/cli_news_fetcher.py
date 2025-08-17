#!/usr/bin/env python3
"""
Command Line Interface for News Fetcher
Easy to use CLI for fetching news with date filtering
"""

import argparse
import sys
from datetime import datetime, timedelta
from news_fetcher import NewsFetcher, print_news_summary

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Fetch free news feeds with date filtering",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Get today's top 5 news
  python cli_news_fetcher.py

  # Get yesterday's top 5 news
  python cli_news_fetcher.py --date yesterday

  # Get news for a specific date
  python cli_news_fetcher.py --date 2024-01-15

  # Get top 3 news for today
  python cli_news_fetcher.py --limit 3

  # Get news from last week
  python cli_news_fetcher.py --date last-week

  # Get news from last month
  python cli_news_fetcher.py --date last-month
        """
    )
    
    parser.add_argument(
        '--date', '-d',
        type=str,
        help='Date to fetch news for (YYYY-MM-DD, yesterday, last-week, last-month)'
    )
    
    parser.add_argument(
        '--limit', '-l',
        type=int,
        default=5,
        help='Number of top news items to return (default: 5)'
    )
    
    parser.add_argument(
        '--source', '-s',
        type=str,
        help='Filter news by specific source (e.g., BBC, Reuters)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    parser.add_argument(
        '--json', '-j',
        action='store_true',
        help='Output results in JSON format'
    )
    
    return parser.parse_args()

def get_date_from_argument(date_arg):
    """Convert date argument to YYYY-MM-DD format"""
    if not date_arg:
        return datetime.now().strftime("%Y-%m-%d")
    
    if date_arg == 'yesterday':
        return (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    elif date_arg == 'last-week':
        return (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    elif date_arg == 'last-month':
        return (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    else:
        # Try to parse as YYYY-MM-DD
        try:
            datetime.strptime(date_arg, "%Y-%m-%d")
            return date_arg
        except ValueError:
            print(f"Error: Invalid date format '{date_arg}'. Use YYYY-MM-DD, yesterday, last-week, or last-month")
            sys.exit(1)

def filter_by_source(news_items, source_name):
    """Filter news items by source"""
    if not source_name:
        return news_items
    
    filtered = [item for item in news_items if source_name.lower() in item.source.lower()]
    if not filtered:
        print(f"Warning: No news found from source '{source_name}'")
        return []
    
    return filtered

def output_json(news_items):
    """Output news items in JSON format"""
    import json
    
    news_data = []
    for item in news_items:
        news_data.append({
            'title': item.title,
            'description': item.description,
            'link': item.link,
            'published_date': item.published_date,
            'source': item.source,
            'category': item.category,
            'image_url': item.image_url
        })
    
    print(json.dumps(news_data, indent=2, ensure_ascii=False))

def main():
    """Main CLI function"""
    args = parse_arguments()
    
    # Set up logging
    if args.verbose:
        import logging
        logging.basicConfig(level=logging.INFO)
    
    print("📰 News Fetcher CLI")
    print("=" * 40)
    
    # Get target date
    target_date = get_date_from_argument(args.date)
    print(f"📅 Fetching news for: {target_date}")
    print(f"🔝 Number of items: {args.limit}")
    
    if args.source:
        print(f"📡 Filtering by source: {args.source}")
    
    print("-" * 40)
    
    try:
        # Initialize fetcher and get news
        fetcher = NewsFetcher()
        news_items = fetcher.get_top_news(target_date=target_date, limit=args.limit * 2)  # Get more to filter
        
        # Filter by source if specified
        if args.source:
            news_items = filter_by_source(news_items, args.source)
            news_items = news_items[:args.limit]  # Limit after filtering
        
        # Limit results
        news_items = news_items[:args.limit]
        
        if not news_items:
            print(f"❌ No news found for {target_date}")
            if args.source:
                print(f"   Source filter: {args.source}")
            sys.exit(1)
        
        # Output results
        if args.json:
            output_json(news_items)
        else:
            print_news_summary(news_items)
        
        print(f"\n✅ Successfully fetched {len(news_items)} news items for {target_date}")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
