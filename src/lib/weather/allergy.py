import os
from typing import Dict, Any, Optional
import httpx
from datetime import datetime, timedelta
from ..utils.cache import cached

class AllergyClient:
    """Client for accessing Google Maps Pollen API"""
    
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_MAPS_API_KEY')
        if not self.api_key:
            raise ValueError("GOOGLE_MAPS_API_KEY environment variable is required")
        
        self.air_quality_url = "https://airquality.googleapis.com/v1/currentConditions:lookup"
        self.pollen_url = "https://pollen.googleapis.com/v1/forecast:lookup"

    @cached(ttl_seconds=300)  # Cache for 5 minutes
    async def get_air_quality(self, latitude: float, longitude: float) -> Optional[Dict[str, Any]]:
        """
        Get current air quality conditions for a location.
        """
        try:
            json_data = {
                "universalAqi": True,
                "location": {
                    "latitude": latitude,
                    "longitude": longitude
                },
                "extraComputations": [
                    "HEALTH_RECOMMENDATIONS",
                    "DOMINANT_POLLUTANT_CONCENTRATION",
                    "POLLUTANT_CONCENTRATION",
                    "LOCAL_AQI",
                    "POLLUTANT_ADDITIONAL_INFO"
                ],
                "languageCode": "en"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.air_quality_url}?key={self.api_key}",
                    json=json_data,
                    headers={'Content-Type': 'application/json'}
                )
                response.raise_for_status()
                return response.json()
                
        except httpx.HTTPError as e:
            print(f"Error fetching air quality data: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error fetching air quality data: {e}")
            return None

    @cached(ttl_seconds=300)  # Cache for 5 minutes
    async def get_pollen_forecast(self, latitude: float, longitude: float, days: int = 5) -> Optional[Dict[str, Any]]:
        """
        Get pollen forecast for a location.
        
        Args:
            latitude: Location latitude
            longitude: Location longitude
            days: Number of forecast days (max 5)
            
        Returns:
            Dictionary containing pollen forecast data including:
            - Daily pollen levels for grass, tree, and weed pollen
            - Plant-specific information and seasonality
            - Health recommendations
        """
        try:
            params = {
                "key": self.api_key,
                "location.latitude": latitude,
                "location.longitude": longitude,
                "days": min(days, 5),  # Ensure we don't exceed max days
                "languageCode": "en",
                "plantsDescription": "true"  # Include detailed plant information
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    self.pollen_url,
                    params=params
                )
                response.raise_for_status()
                return response.json()
                
        except httpx.HTTPError as e:
            print(f"Error fetching pollen forecast: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error fetching pollen forecast: {e}")
            return None
