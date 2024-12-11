from src.app import app
import asyncio

async def main():
    print("Testing application with context-aware LLM...")
    
    # Print current context
    print("\nCurrent Context:")
    await app.context_manager.update_llm_context(app.llm_service)
    
    # Test some context-aware questions
    questions = [
        "What's the current temperature in my location?",
        "Given the current time and weather, what would you recommend wearing today?",
        "Is it a good time for outdoor activities?"
    ]
    
    for question in questions:
        print(f"\nQuestion: {question}")
        await app.context_manager.update_llm_context(app.llm_service)
        response = app.llm_service.chat(question)
        print(f"Response: {response}")

if __name__ == "__main__":
    asyncio.run(main())
