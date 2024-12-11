from datetime import datetime, timedelta
from typing import Dict, Optional
import asyncio

class RateLimiter:
    """Rate limiter with token bucket algorithm"""
    
    def __init__(self, max_requests: int, time_window: int):
        """
        Initialize rate limiter.
        
        Args:
            max_requests: Maximum number of requests allowed in time window
            time_window: Time window in seconds
        """
        self.max_requests = max_requests
        self.time_window = time_window
        self.tokens = max_requests
        self.last_update = datetime.now()
        self._lock = asyncio.Lock()
    
    async def acquire(self):
        """Acquire a token, waiting if necessary"""
        async with self._lock:
            while self.tokens <= 0:
                now = datetime.now()
                time_passed = (now - self.last_update).total_seconds()
                self.tokens = min(
                    self.max_requests,
                    self.tokens + (time_passed * self.max_requests / self.time_window)
                )
                self.last_update = now
                if self.tokens <= 0:
                    await asyncio.sleep(0.1)  # Wait a bit before checking again
            
            self.tokens -= 1
            return True


def rate_limited(max_requests: int, time_window: int):
    """Decorator to rate limit a function"""
    limiters: Dict[str, RateLimiter] = {}
    
    def decorator(func):
        # Create a unique key for this function
        key = f"{func.__module__}.{func.__qualname__}"
        
        async def wrapper(*args, **kwargs):
            # Get or create limiter for this function
            if key not in limiters:
                limiters[key] = RateLimiter(max_requests, time_window)
            
            # Wait for token
            await limiters[key].acquire()
            
            # Call function
            return await func(*args, **kwargs)
        
        return wrapper
    return decorator
