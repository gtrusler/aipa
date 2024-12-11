import asyncio
from src.lib.ai.perplexity import PerplexityClient, PerplexityConfig

async def main():
    # Initialize client
    client = PerplexityClient()
    
    # Basic usage with default settings
    print("Basic question:")
    answer = await client.ask("How many stars are there in our galaxy?")
    print(f"Answer: {answer}\n")
    
    # Advanced usage with custom configuration
    print("Advanced search with custom config:")
    config = PerplexityConfig(
        model="llama-3.1-sonar-small-128k-online",
        temperature=0.1,  # More focused responses
        search_recency_filter="week",  # More recent results
        return_related_questions=True  # Include related questions
    )
    
    result = await client.search(
        "What are the latest developments in quantum computing?",
        system_prompt="Focus on verified scientific sources and recent breakthroughs.",
        config=config
    )
    
    print("Full response:")
    print(f"Main answer: {result['choices'][0]['message']['content']}")
    if result.get('related_questions'):
        print("\nRelated questions:")
        for question in result['related_questions']:
            print(f"- {question}")

if __name__ == "__main__":
    asyncio.run(main())
