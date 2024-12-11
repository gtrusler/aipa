import asyncio
from datetime import datetime
from zoneinfo import ZoneInfo
from src.lib.news import NewsClient

async def main():
    client = NewsClient()
    current_time = datetime.fromisoformat('2024-12-11T04:16:54-06:00')
    
    print("Top Stories from Each Category:")
    news_data = await client.get_multiple_categories(
        categories=['austin', 'latest', 'us', 'world'],
        limit_per_category=3
    )
    
    for category, articles in news_data.items():
        print(f"\n{category.upper()} NEWS (Top 3):")
        for i, article in enumerate(articles, 1):
            # Calculate relative time
            time_diff = current_time - article.published
            if time_diff.days > 0:
                time_str = f"{time_diff.days}d ago"
            else:
                hours = time_diff.seconds // 3600
                if hours > 0:
                    time_str = f"{hours}h ago"
                else:
                    minutes = (time_diff.seconds % 3600) // 60
                    time_str = f"{minutes}m ago"
            
            print(f"\n{i}. {article.title}")
            print(f"   Time: {time_str}")
            summary = article.summary.replace('\n', ' ').strip()
            if len(summary) > 200:
                summary = summary[:197] + "..."
            print(f"   Summary: {summary}")
        print("-" * 80)

if __name__ == "__main__":
    asyncio.run(main())
