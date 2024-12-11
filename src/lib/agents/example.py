import os
from dotenv import load_dotenv
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.tools.wikipedia.tool import WikipediaQueryRun
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper

from base_agent import BaseAgent

def main():
    # Load environment variables
    load_dotenv()

    # Initialize tools
    search = DuckDuckGoSearchRun()
    wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
    tools = [search, wikipedia]

    # Create the agent
    agent = BaseAgent(
        tools=tools,
        model_name="claude-3-sonnet-20240229"
    )

    # Test direct queries
    queries = [
        "Compare and contrast the approaches of LangChain and LangGraph for building AI applications. Use both search and Wikipedia to gather comprehensive information.",
        "What are the key features and capabilities of Claude 3.5 Sonnet? How does it compare to previous versions?",
        "Analyze the current state of AI agent architectures. What are the emerging trends and best practices?"
    ]

    # Run direct queries
    for query in queries:
        print(f"\nQuery: {query}")
        print("-" * 80)
        response = agent.process({
            "input": query,
            "chat_history": [],
            "output": None
        })
        print(f"Response: {response['output']}")
        print("-" * 80)

if __name__ == "__main__":
    main()
