# News Fetcher - Free News Feed with Date Filtering

A Python script that fetches free news from various RSS feeds and filters them by date to return the top 5 news items.

## Features

- 🆓 **Free to use** - No API keys required for basic functionality
- 📅 **Date filtering** - Get news for specific dates
- 🔝 **Top N results** - Configurable number of top news items
- 📰 **Multiple sources** - BBC, Reuters, NPR, Al Jazeera, The Guardian, and more
- 🚀 **Easy to use** - Simple API with comprehensive examples
- 📊 **Structured data** - News items with title, description, link, source, and date

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements_news.txt
```

Or install manually:
```bash
pip install requests feedparser python-dateutil
```

## Quick Start

### Basic Usage

```python
from news_fetcher import NewsFetcher

# Initialize the fetcher
fetcher = NewsFetcher()

# Get today's top 5 news
today_news = fetcher.get_top_news(limit=5)

# Get news for a specific date
yesterday_news = fetcher.get_top_news(target_date="2024-01-15", limit=5)
```

### Get Today's Top 5 News

```python
from news_fetcher import NewsFetcher, print_news_summary

fetcher = NewsFetcher()
today_news = fetcher.get_top_news(limit=5)
print_news_summary(today_news)
```

### Get News for a Specific Date

```python
# Get news for January 15, 2024
custom_date = "2024-01-15"
news = fetcher.get_top_news(target_date=custom_date, limit=5)
print_news_summary(news)
```

### Get Yesterday's News

```python
from datetime import datetime, timedelta

yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
yesterday_news = fetcher.get_top_news(target_date=yesterday, limit=5)
print_news_summary(yesterday_news)
```

## News Sources

The script fetches news from the following free RSS feeds:

- **BBC News** - World news and current events
- **Reuters** - International news and business
- **NPR** - National Public Radio news
- **Al Jazeera** - International news coverage
- **The Guardian** - World news and analysis
- **AP News** - Associated Press news
- **NBC News** - National news coverage
- **ABC News** - US headlines
- **CBS News** - Latest news
- **PBS News** - Politics and current events

## Advanced Features

### NewsAPI Integration (Optional)

For additional news sources and better search capabilities, you can integrate with NewsAPI:

1. Get a free API key from [NewsAPI](https://newsapi.org/)
2. Set your API key:
```python
fetcher.set_news_api_key("your_api_key_here")
```

3. Use NewsAPI for specific queries:
```python
tech_news = fetcher.get_top_news(
    target_date="2024-01-15",
    limit=5,
    use_news_api=True,
    query="technology"
)
```

### Custom Ranking

The script includes basic ranking based on source reliability. You can customize the ranking logic by modifying the `source_priority` dictionary in the `get_top_news` method.

## Data Structure

Each news item contains:

```python
@dataclass
class NewsItem:
    title: str              # News headline
    description: str         # News summary/description
    link: str               # URL to full article
    published_date: str     # Publication date and time
    source: str             # News source name
    category: Optional[str] # News category (if available)
    image_url: Optional[str] # Image URL (if available)
```

## Examples

Run the example script to see all features in action:

```bash
python example_usage.py
```

Or run the main script:

```bash
python news_fetcher.py
```

## Error Handling

The script includes comprehensive error handling:

- Invalid date formats
- Network connection issues
- RSS feed parsing errors
- Missing or malformed data

All errors are logged and the script continues processing other sources.

## Rate Limiting

The script includes a 0.5-second delay between RSS feed requests to be respectful to the news sources.

## Requirements

- Python 3.7+
- `requests` - HTTP library
- `feedparser` - RSS/Atom feed parser
- `python-dateutil` - Date parsing utilities

## License

This script is free to use and modify. Please respect the terms of service of the news sources you're fetching from.

## Contributing

Feel free to:
- Add more RSS feeds
- Improve the ranking algorithm
- Add more filtering options
- Enhance error handling
- Add tests

## Troubleshooting

### Common Issues

1. **No news returned**: Check your internet connection and ensure the RSS feeds are accessible
2. **Date parsing errors**: Ensure dates are in YYYY-MM-DD format
3. **Empty results**: Some dates may not have news available from all sources

### Debug Mode

Enable debug logging to see detailed information:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Support

If you encounter issues or have questions, check the error logs first. The script provides detailed logging for troubleshooting.
