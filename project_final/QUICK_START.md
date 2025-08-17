# 🚀 Quick Start Guide - News Fetcher

## 📁 Available Scripts

### 1. **`news_fetcher.py`** - Main Library
- **Purpose**: Core news fetching functionality
- **Usage**: Import as a module in your Python code
- **Features**: RSS feed parsing, date filtering, NewsAPI integration

### 2. **`cli_news_fetcher.py`** - Command Line Interface
- **Purpose**: Easy-to-use command line tool
- **Usage**: Run directly from terminal with various options
- **Features**: Date filtering, source filtering, JSON output, verbose logging

### 3. **`example_usage.py`** - Comprehensive Examples
- **Purpose**: Shows all features with practical examples
- **Usage**: Run to see different ways to use the news fetcher
- **Features**: Multiple date examples, source filtering, NewsAPI examples

### 4. **`test_news_fetcher.py`** - Basic Testing
- **Purpose**: Test basic functionality without making requests
- **Usage**: Verify the installation works correctly
- **Features**: Import testing, configuration validation

## 🎯 Quick Examples

### Get Today's Top 5 News
```bash
python cli_news_fetcher.py
```

### Get Yesterday's Top 5 News
```bash
python cli_news_fetcher.py --date yesterday
```

### Get News for Specific Date
```bash
python cli_news_fetcher.py --date 2024-01-15
```

### Get Top 3 News from BBC
```bash
python cli_news_fetcher.py --limit 3 --source BBC
```

### Get News from Last Week
```bash
python cli_news_fetcher.py --date last-week
```

### Output in JSON Format
```bash
python cli_news_fetcher.py --json
```

## 🔧 Installation

1. **Install Dependencies**:
   ```bash
   pip install -r requirements_news.txt
   ```

2. **Test Installation**:
   ```bash
   python test_news_fetcher.py
   ```

3. **Start Using**:
   ```bash
   python cli_news_fetcher.py
   ```

## 📊 News Sources

The script fetches from 10+ free RSS feeds:
- BBC News, Reuters, NPR, Al Jazeera
- The Guardian, AP News, NBC News
- ABC News, CBS News, PBS News

## 🆓 Free to Use

- **No API keys required** for basic functionality
- **RSS feeds** are completely free
- **Optional NewsAPI integration** for enhanced features

## 🚨 Important Notes

- **Rate Limiting**: 0.5-second delay between requests
- **Date Format**: Use YYYY-MM-DD format
- **Internet Required**: Needs internet connection to fetch feeds
- **Respectful Usage**: Be mindful of the news sources' servers

## 📖 Full Documentation

See `README_news_fetcher.md` for complete documentation and advanced usage examples.

## 🆘 Need Help?

1. Check the error logs first
2. Verify your internet connection
3. Try with `--verbose` flag for detailed logging
4. Check the example scripts for usage patterns

---

**Happy News Fetching! 📰✨**
