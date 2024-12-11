from .lib.context.manager import ContextManager
from .lib.ai.llm import LLMService
from .config.location import DEFAULT_LOCATION

class Application:
    def __init__(self):
        # Initialize the context manager with default location
        self.context_manager = ContextManager()
        self.context_manager.location = DEFAULT_LOCATION
        
        # Initialize the LLM service
        self.llm_service = LLMService()
    
    def process_message(self, message: str) -> str:
        """
        Process a user message, updating context before each interaction.
        """
        # Update context before processing the message
        self.context_manager.update_llm_context(self.llm_service)
        
        # Get response from LLM
        return self.llm_service.chat(message)
    
    def reset_conversation(self):
        """Reset the conversation history."""
        self.llm_service.reset_conversation()

# Create a singleton instance
app = Application()
