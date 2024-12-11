import os
from typing import Dict, List, Optional, Tuple, Any
import httpx
from datetime import datetime, timedelta
from dotenv import load_dotenv
from ..utils.cache import cached
from ..utils.rate_limit import rate_limited

# Load environment variables
load_dotenv('.env.local')

class WeatherClient:
    BASE_URL = "https://api.tomorrow.io/v4"
    
    def __init__(self):
        self.api_key = os.getenv('TOMORROW_IO_API_KEY')
        if not self.api_key:
            raise ValueError("TOMORROW_IO_API_KEY environment variable is required")
        
        self.base_url = "https://api.tomorrow.io/v4/weather"

    @cached(ttl_seconds=300)  # Cache for 5 minutes
    @rate_limited(max_requests=25, time_window=300)  # 25 requests per 5 minutes
    async def get_realtime(
        self,
        location: Tuple[float, float],
        fields: Optional[List[str]] = None,
        units: str = "imperial"
    ) -> Dict[str, Any]:
        """
        Get current weather conditions for a location.
        
        Args:
            location: Tuple of (latitude, longitude)
            fields: List of fields to include in the response
            units: Unit system to use ('imperial' or 'metric')
        
        Returns:
            Dict containing current weather data
        """
        if fields is None:
            fields = [
                "temperature",
                "humidity",
                "windSpeed",
                "windDirection",
                "precipitationProbability",
                "precipitationType",
                "weatherCode"
            ]

        try:
            lat, lon = location
            params = {
                'apikey': self.api_key,
                'location': f"{lat},{lon}",
                'fields': fields,
                'units': units
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/realtime", params=params)
                response.raise_for_status()
                return response.json()
                
        except Exception as e:
            print(f"Error fetching current weather: {e}")
            raise

    @cached(ttl_seconds=300)  # Cache for 5 minutes
    @rate_limited(max_requests=25, time_window=300)  # 25 requests per 5 minutes
    async def get_forecast(
        self,
        location: Tuple[float, float],
        timesteps: str = "1h",
        fields: Optional[List[str]] = None,
        units: str = "imperial"
    ) -> Dict[str, Any]:
        """
        Get weather forecast for a location.
        
        Args:
            location: Tuple of (latitude, longitude)
            timesteps: Time step for forecast data ('1h', '1d', etc.)
            fields: List of fields to include in the forecast
            units: Unit system to use ('imperial' or 'metric')
        
        Returns:
            Dict containing forecast data
        """
        if fields is None:
            fields = [
                "temperature",
                "humidity",
                "windSpeed",
                "windDirection",
                "precipitationProbability",
                "precipitationType",
                "weatherCode"
            ]

        try:
            lat, lon = location
            params = {
                'apikey': self.api_key,
                'location': f"{lat},{lon}",
                'fields': fields,
                'timesteps': timesteps,
                'units': units
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/timelines", params=params)
                response.raise_for_status()
                return response.json()
                
        except Exception as e:
            print(f"Error fetching forecast: {e}")
            raise

    async def __del__(self):
        if hasattr(self, 'client'):
            await self.client.aclose()
