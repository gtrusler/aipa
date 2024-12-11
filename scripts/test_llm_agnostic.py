import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.lib.ai.llm import LLMService
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.local')

def test_different_models():
    # Test system prompt
    system_prompt = """You are an independent AI designed to provide clear, direct insights 
    in a conversational manner. Keep your responses concise and friendly."""
    
    # Test with Claude
    print("\nTesting Claude 3:")
    print("-" * 50)
    claude_service = LLMService(
        model_name="claude-3-5-sonnet-20241022",
        system_prompt=system_prompt,
        temperature=0.7
    )
    claude_response = claude_service.chat(
        "What are three key principles of good API design?"
    )
    print(f"Claude's response:\n{claude_response}")
    
    # Test with GPT
    print("\nTesting GPT:")
    print("-" * 50)
    gpt_service = LLMService(
        model_name="gpt-3.5-turbo",
        system_prompt=system_prompt,
        temperature=0.7
    )
    gpt_response = gpt_service.chat(
        "What are three key principles of good API design?"
    )
    print(f"GPT's response:\n{gpt_response}")

if __name__ == "__main__":
    test_different_models()
