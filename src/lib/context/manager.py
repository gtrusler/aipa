from datetime import datetime
from typing import Optional, Dict, Any, Tuple, List
from dataclasses import dataclass
from zoneinfo import ZoneInfo
import json
from ..weather.client import WeatherClient
from ..weather.allergy import AllergyClient
from ..news import NewsClient
from ..ai.perplexity import PerplexityClient, PerplexityConfig

@dataclass
class Location:
    latitude: float
    longitude: float
    city: str
    state: str
    country: str
    timezone: str

class ContextManager:
    def __init__(self, location: Location):
        """Initialize the context manager with a location."""
        self._location = location
        self._weather_client = WeatherClient()
        self._allergy_client = AllergyClient()
        self._news_client = NewsClient()
        self._perplexity_client = PerplexityClient()
        
    @property
    def location(self) -> Optional[Location]:
        return self._location
    
    @location.setter
    def location(self, value: Location):
        self._location = value
    
    def get_current_time(self) -> datetime:
        """Get the current time in the user's timezone."""
        if self._location and self._location.timezone:
            return datetime.now(ZoneInfo(self._location.timezone))
        return datetime.now()
    
    async def get_current_weather(self) -> Optional[Dict[str, Any]]:
        """Get the current weather for the user's location."""
        if not self._location:
            return None
            
        try:
            return await self._weather_client.get_realtime(
                (self._location.latitude, self._location.longitude)
            )
        except Exception as e:
            print(f"Error fetching weather: {e}")
            return None
    
    async def _get_air_quality_context(self, location: Tuple[float, float]) -> str:
        """Get air quality context for the given location."""
        data = await self._allergy_client.get_air_quality(location[0], location[1])
        if not data:
            return "Air quality data is currently unavailable."

        context_parts = []
        
        # Add AQI information
        for index in data.get('indexes', []):
            name = 'Universal AQI' if index['code'] == 'uaqi' else f"AQI ({index['code'].upper()})"
            context_parts.append(
                f"{name}: {index['aqi']} - {index['category']}. "
                f"Dominant pollutant: {index['dominantPollutant'].upper()}"
            )

        # Add pollutant concentrations
        if data.get('pollutants'):
            context_parts.append("\nPollutant levels:")
            for pollutant in data['pollutants']:
                conc = pollutant.get('concentration', {})
                context_parts.append(
                    f"- {pollutant['fullName']}: {conc.get('value', 'N/A')} {conc.get('units', '')}"
                )

        # Add health recommendations
        if data.get('healthRecommendations'):
            recs = data['healthRecommendations']
            if recs.get('generalPopulation'):
                context_parts.append(f"\nHealth advice: {recs['generalPopulation']}")

        return "\n".join(context_parts)

    async def _get_pollen_context(self, location: Tuple[float, float]) -> str:
        """Get pollen forecast context for the given location."""
        data = await self._allergy_client.get_pollen_forecast(location[0], location[1], days=1)
        if not data or not data.get('dailyInfo'):
            return "Pollen forecast is currently unavailable."

        context_parts = []
        today = data['dailyInfo'][0]
        
        # Add date
        date = today.get('date', {})
        if date:
            date_str = f"{date.get('year')}-{date.get('month'):02d}-{date.get('day'):02d}"
            context_parts.append(f"Pollen forecast for {date_str}:")
        
        # Add pollen type information
        for pollen_type in today.get('pollenTypeInfo', []):
            name = pollen_type['displayName']
            season_status = "In season" if pollen_type.get('inSeason') else "Out of season"
            
            index_info = pollen_type.get('indexInfo', {})
            if index_info:
                level = f"{index_info.get('value', 'N/A')} - {index_info.get('category', 'Unknown')}"
                context_parts.append(f"\n{name} Pollen ({season_status}):")
                context_parts.append(f"Level: {level}")
                
                # Add health recommendations if available
                if pollen_type.get('healthRecommendations'):
                    context_parts.append("Advice: " + pollen_type['healthRecommendations'][0])
        
        # Add significant plant information
        plants = [p for p in today.get('plantInfo', []) if p.get('inSeason') and p.get('indexInfo', {}).get('value', 0) > 1]
        if plants:
            context_parts.append("\nSignificant plants in season:")
            for plant in plants:
                index_info = plant.get('indexInfo', {})
                context_parts.append(f"- {plant['displayName']}: {index_info.get('category', 'Unknown')}")

        return "\n".join(context_parts)

    async def _get_news_context(self, categories: List[str] = None, include_summaries: bool = True, stories_per_category: int = 3) -> str:
        """
        Get news context for specified categories.
        
        Args:
            categories: List of news categories to fetch
            include_summaries: Whether to include article summaries
            stories_per_category: Number of stories to show per category
        """
        if categories is None:
            categories = ['latest', 'us', 'world']  # Default categories
        
        try:
            news_data = await self._news_client.get_multiple_categories(
                categories=categories,
                limit_per_category=stories_per_category
            )
            if not news_data:
                return "News data is currently unavailable."

            context_parts = []
            
            for category, articles in news_data.items():
                if articles:
                    context_parts.append(f"\n{category.title()} News (Top {stories_per_category}):")
                    for i, article in enumerate(articles, 1):
                        # Format publish time
                        time_str = article.published.strftime('%I:%M %p').lstrip('0')
                        
                        # Add numbered title and timestamp
                        context_parts.append(f"{i}. [{time_str}] {article.title}")
                        
                        # Add summary if requested
                        if include_summaries and article.summary:
                            # Clean and truncate summary
                            summary = article.summary.replace('\n', ' ').strip()
                            if len(summary) > 200:
                                summary = summary[:197] + "..."
                            context_parts.append(f"   Summary: {summary}")
            
            return "\n".join(context_parts)
            
        except Exception as e:
            print(f"Error getting news context: {e}")
            return "News data is currently unavailable."

    async def _get_web_search_context(self, query: str) -> str:
        """Get relevant web search results for the query."""
        try:
            config = PerplexityConfig(
                temperature=0.1,  # More focused results
                search_recency_filter="day",  # Recent information
                return_related_questions=False
            )
            
            result = await self._perplexity_client.search(
                query,
                system_prompt="Provide a concise summary of the most relevant and recent information. Focus on factual data.",
                config=config
            )
            
            if result and result.get('choices'):
                return f"\nWeb Search Results:\n{result['choices'][0]['message']['content']}"
            return ""
            
        except Exception as e:
            print(f"Error fetching web search results: {e}")
            return ""

    async def get_context_for_llm(self, query: str = "", include_news_summaries: bool = True, include_web_search: bool = True) -> str:
        """
        Generate a context string for the LLM that includes current time,
        weather, air quality, pollen, news, and relevant web search results.
        
        Args:
            query: The user's query to get relevant web search results
            include_news_summaries: Whether to include article summaries in news context
            include_web_search: Whether to include web search results
        """
        context_parts = []
        
        # Add current time
        current_time = datetime.now(ZoneInfo(self._location.timezone))
        context_parts.append(f"Current time: {current_time.strftime('%I:%M %p').lstrip('0')}")
        
        # Add current weather conditions if available
        if self._location:
            weather = await self.get_current_weather()
            if weather:
                values = weather['data']['values']
                context_parts.extend([
                    "\nCurrent weather conditions:",
                    f"  Temperature: {round(values['temperature'])}°F",
                    f"  Conditions: {values.get('weatherCode', 'Unknown')}",
                    f"  Wind Speed: {round(values['windSpeed'])} mph"
                ])
            
            # Add current air quality
            air_quality_context = await self._get_air_quality_context((self._location.latitude, self._location.longitude))
            if air_quality_context:
                context_parts.append("\nCurrent air quality:")
                context_parts.append(air_quality_context)
            
            # Add pollen information
            pollen_context = await self._get_pollen_context((self._location.latitude, self._location.longitude))
            if pollen_context:
                context_parts.append("\nPollen information:")
                context_parts.append(pollen_context)
        
        # Add news information
        news_context = await self._get_news_context(
            categories=['austin', 'latest', 'us', 'world'],
            include_summaries=include_news_summaries,
            stories_per_category=3
        )
        if news_context:
            context_parts.append("\nTop Stories:")
            context_parts.append(news_context)
        
        # Add web search results if query is provided
        if include_web_search and query:
            web_context = await self._get_web_search_context(query)
            if web_context:
                context_parts.append(web_context)
        
        return "\n".join(context_parts)

    async def update_llm_context(self, llm_service) -> None:
        """
        Update the LLM's context with current information.
        This should be called before each LLM interaction.
        """
        context = await self.get_context_for_llm()
        # Add the context as a system message
        llm_service.add_context_message(
            f"Here is the current context for this interaction:\n{context}\n\n"
            "Use this information when it's relevant to the user's questions or when "
            "providing time-sensitive or location-aware responses."
        )
