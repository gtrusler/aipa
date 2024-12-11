import asyncio
from src.lib.context.manager import ContextManager, Location

async def main():
    # Initialize context manager with Austin location
    context_manager = ContextManager(
        Location(
            latitude=30.2672,
            longitude=-97.7431,
            timezone="America/Chicago"
        )
    )
    
    # Test queries
    queries = [
        "What's the latest news about AI regulation?",
        "Tell me about recent developments in Austin's tech scene",
        "What are the current market trends in real estate?"
    ]
    
    for query in queries:
        print(f"\nGetting context for query: {query}")
        print("-" * 80)
        
        # Get context with web search results
        context = await context_manager.get_context_for_llm(
            query=query,
            include_news_summaries=True,
            include_web_search=True
        )
        
        print(context)
        print("=" * 80)
        
        # Small delay to respect rate limits
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
