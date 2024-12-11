from src.lib.context.manager import ContextManager, Location
from src.lib.ai.llm import LLMService

def main():
    # Initialize the context manager
    context_manager = ContextManager()
    
    # Set a sample location (Austin, TX)
    context_manager.location = Location(
        latitude=30.2672,
        longitude=-97.7431,
        city="Austin",
        state="Texas",
        country="United States",
        timezone="America/Chicago"
    )
    
    # Initialize the LLM service
    llm_service = LLMService()
    
    # Update the LLM context with current information
    context_manager.update_llm_context(llm_service)
    
    # Print the current context
    print("Current Context:")
    print(context_manager.get_context_for_llm())
    print("\nTesting LLM with context...")
    
    # Test the LLM with a weather-related question
    response = llm_service.chat("What's the current temperature and weather like?")
    print("\nLLM Response:")
    print(response)

if __name__ == "__main__":
    main()
