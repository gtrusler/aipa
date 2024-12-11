import feedparser
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
import asyncio
import httpx
from ..utils.cache import cached
from zoneinfo import ZoneInfo
import time

@dataclass
class NewsArticle:
    title: str
    summary: str
    link: str
    published: datetime
    category: str

class NewsClient:
    """Client for fetching news from Fox News RSS feeds."""
    
    FEED_URLS = {
        'latest': 'https://moxie.foxnews.com/google-publisher/latest.xml',
        'world': 'https://moxie.foxnews.com/google-publisher/world.xml',
        'us': 'https://moxie.foxnews.com/google-publisher/us.xml',
        'politics': 'https://moxie.foxnews.com/google-publisher/politics.xml',
        'science': 'https://moxie.foxnews.com/google-publisher/science.xml',
        'health': 'https://moxie.foxnews.com/google-publisher/health.xml',
        'sports': 'https://moxie.foxnews.com/google-publisher/sports.xml',
        'travel': 'https://moxie.foxnews.com/google-publisher/travel.xml',
        'tech': 'https://moxie.foxnews.com/google-publisher/tech.xml',
        'opinion': 'https://moxie.foxnews.com/google-publisher/opinion.xml',
        'austin': 'https://www.fox7austin.com/rss/category/local-news'
    }
    
    def __init__(self):
        """Initialize the news client."""
        pass
    
    async def _parse_feed(self, feed_data: feedparser.FeedParserDict, limit: int = None) -> List[NewsArticle]:
        """Parse feed data and return a list of NewsArticle objects."""
        articles = []
        entries = feed_data.entries[:limit] if limit else feed_data.entries
        
        for entry in entries:
            # Convert the published time to a datetime object with timezone
            published = datetime.fromtimestamp(
                time.mktime(entry.published_parsed)
            ).replace(tzinfo=ZoneInfo("America/Chicago"))
            
            article = NewsArticle(
                title=entry.title,
                link=entry.link,
                published=published,
                summary=entry.summary if hasattr(entry, 'summary') else entry.description,
                category='latest'
            )
            articles.append(article)
        
        return articles
    
    @cached(ttl_seconds=300)  # Cache for 5 minutes
    async def get_news(self, category: str = 'latest', limit: int = 5) -> List[NewsArticle]:
        """
        Fetch news articles from the specified category.
        
        Args:
            category: News category (latest, world, us, politics, etc.)
            limit: Maximum number of articles to return
            
        Returns:
            List of NewsArticle objects
        """
        if category not in self.FEED_URLS:
            raise ValueError(f"Invalid category. Choose from: {', '.join(self.FEED_URLS.keys())}")
        
        try:
            # Fetch RSS feed
            async with httpx.AsyncClient() as client:
                response = await client.get(self.FEED_URLS[category])
                response.raise_for_status()
                feed_content = response.text
            
            # Parse feed (feedparser is synchronous, so run in thread pool)
            feed = await asyncio.get_event_loop().run_in_executor(
                None, feedparser.parse, feed_content
            )
            
            return await self._parse_feed(feed, limit)
            
        except httpx.HTTPError as e:
            print(f"Error fetching news feed: {e}")
            return []
        except Exception as e:
            print(f"Unexpected error fetching news: {e}")
            return []
    
    async def get_multiple_categories(
        self, 
        categories: List[str] = None,
        limit_per_category: int = 3
    ) -> Dict[str, List[NewsArticle]]:
        """
        Fetch news from multiple categories concurrently.
        
        Args:
            categories: List of categories to fetch (defaults to ['latest', 'world', 'us'])
            limit_per_category: Maximum number of articles per category
            
        Returns:
            Dictionary mapping categories to lists of articles
        """
        if categories is None:
            categories = ['latest', 'world', 'us']
        
        # Validate categories
        invalid_categories = [cat for cat in categories if cat not in self.FEED_URLS]
        if invalid_categories:
            raise ValueError(f"Invalid categories: {', '.join(invalid_categories)}")
        
        # Fetch all categories concurrently
        tasks = [
            self.get_news(category, limit_per_category)
            for category in categories
        ]
        results = await asyncio.gather(*tasks)
        
        # Combine results
        return dict(zip(categories, results))
