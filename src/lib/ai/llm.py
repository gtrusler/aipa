from typing import Optional, List, Union
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.language_models import BaseChatModel
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.local')

class LLMFactory:
    @staticmethod
    def create_llm(model_name: str, **kwargs) -> BaseChatModel:
        """Create an LLM instance based on the model name."""
        if model_name.startswith('gpt'):
            return ChatOpenAI(
                model=model_name,
                openai_api_key=os.getenv('OPENAI_API_KEY'),
                **kwargs
            )
        elif model_name.startswith('claude'):
            return ChatAnthropic(
                model=model_name,
                anthropic_api_key=os.getenv('ANTHROPIC_API_KEY'),
                **kwargs
            )
        else:
            raise ValueError(f"Unsupported model: {model_name}")

class LLMService:
    def __init__(
        self,
        model_name: str = "gpt-3.5-turbo",
        system_prompt: Optional[str] = None,
        **kwargs
    ):
        self.llm = LLMFactory.create_llm(model_name, **kwargs)
        self.system_prompt = system_prompt
        self.conversation_history: List[Union[SystemMessage, HumanMessage, AIMessage]] = []
        if system_prompt:
            self.conversation_history.append(SystemMessage(content=system_prompt))

    def add_context_message(self, context: str) -> None:
        """Add a context message to the conversation history."""
        # Remove any previous context messages
        self.conversation_history = [
            msg for msg in self.conversation_history 
            if not (isinstance(msg, SystemMessage) and msg.content.startswith("Here is the current context"))
        ]
        # Add the new context message
        self.conversation_history.append(SystemMessage(content=context))

    def chat(self, message: str) -> str:
        """Send a message and get a response."""
        self.conversation_history.append(HumanMessage(content=message))
        response = self.llm.invoke(self.conversation_history)
        self.conversation_history.append(response)
        return response.content

    def reset_conversation(self):
        """Reset the conversation history, keeping the system prompt if it exists."""
        self.conversation_history = []
        if self.system_prompt:
            self.conversation_history.append(SystemMessage(content=self.system_prompt))
