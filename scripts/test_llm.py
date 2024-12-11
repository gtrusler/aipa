import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser

# Load environment variables from .env.local
load_dotenv('.env.local')

def test_llm_interaction():
    # Initialize the LLM
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7,
        openai_api_key=os.getenv('OPENAI_API_KEY')
    )
    
    # Create a simple chain with the system prompt
    system_prompt = """You are an independent AI designed to provide clear, direct insights in a conversational manner.
    Keep your responses concise and friendly."""
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content="Hello! Can you tell me what capabilities you have?")
    ]
    
    # Get the response
    response = llm.invoke(messages)
    
    print("\nTest Results:")
    print("-" * 50)
    print(f"Response:\n{response.content}")
    print("-" * 50)

if __name__ == "__main__":
    test_llm_interaction()
