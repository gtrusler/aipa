"""
Perplexity AI client for enhanced search and question answering.
"""
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
import os
import httpx
from ..utils.cache import cached

@dataclass
class PerplexityConfig:
    """Configuration for Perplexity API calls."""
    model: str = "llama-3.1-sonar-small-128k-online"
    temperature: float = 0.2
    top_p: float = 0.9
    max_tokens: Optional[int] = None
    search_domain_filter: Optional[List[str]] = None
    return_images: bool = False
    return_related_questions: bool = False
    search_recency_filter: Optional[str] = "month"
    top_k: int = 0
    stream: bool = False
    presence_penalty: float = 0
    frequency_penalty: float = 1

class PerplexityClient:
    """Client for interacting with Perplexity AI API."""
    
    API_URL = "https://api.perplexity.ai/chat/completions"
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the Perplexity client.
        
        Args:
            api_key: Optional API key. If not provided, will look for PERPLEXITY_API_KEY in environment.
        """
        self.api_key = api_key or os.getenv("PERPLEXITY_API_KEY")
        if not self.api_key:
            raise ValueError("Perplexity API key not found. Please set PERPLEXITY_API_KEY environment variable.")
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests."""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def _prepare_messages(self, query: str, system_prompt: Optional[str] = None) -> List[Dict[str, str]]:
        """Prepare messages for the API request."""
        messages = []
        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })
        messages.append({
            "role": "user",
            "content": query
        })
        return messages
    
    @cached(ttl_seconds=300)  # Cache responses for 5 minutes
    async def search(
        self,
        query: str,
        *,
        system_prompt: Optional[str] = "Be precise and concise.",
        config: Optional[PerplexityConfig] = None
    ) -> Dict[str, Any]:
        """
        Search using Perplexity AI.
        
        Args:
            query: The search query or question
            system_prompt: Optional system prompt to guide the response
            config: Optional configuration overrides
            
        Returns:
            Dict containing the API response
            
        Raises:
            httpx.HTTPError: If the API request fails
        """
        config = config or PerplexityConfig()
        
        payload = {
            "model": config.model,
            "messages": self._prepare_messages(query, system_prompt),
            "temperature": config.temperature,
            "top_p": config.top_p,
            "search_domain_filter": config.search_domain_filter,
            "return_images": config.return_images,
            "return_related_questions": config.return_related_questions,
            "search_recency_filter": config.search_recency_filter,
            "top_k": config.top_k,
            "stream": config.stream,
            "presence_penalty": config.presence_penalty,
            "frequency_penalty": config.frequency_penalty
        }
        
        if config.max_tokens:
            payload["max_tokens"] = config.max_tokens
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.API_URL,
                json=payload,
                headers=self._get_headers()
            )
            response.raise_for_status()
            return response.json()

    async def ask(
        self,
        question: str,
        *,
        system_prompt: Optional[str] = "Be precise and concise."
    ) -> str:
        """
        Simplified method to ask a question and get just the answer text.
        
        Args:
            question: The question to ask
            system_prompt: Optional system prompt to guide the response
            
        Returns:
            str: The answer text
        """
        response = await self.search(question, system_prompt=system_prompt)
        return response["choices"][0]["message"]["content"]
