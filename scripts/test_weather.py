import sys
import os
from datetime import datetime

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.lib.weather.client import WeatherClient

def test_weather_service():
    weather = WeatherClient()
    
    # Test with coordinates (New York City)
    print("\nTesting weather forecast for New York City:")
    print("-" * 50)
    
    try:
        # Get current weather
        current = weather.get_realtime((40.7128, -74.0060))
        print("\nCurrent weather in NYC:")
        print(f"Temperature: {current['data']['values']['temperature']}°F")
        print(f"Humidity: {current['data']['values']['humidity']}%")
        print(f"Wind Speed: {current['data']['values']['windSpeed']} mph")
        
        # Get hourly forecast
        forecast = weather.get_forecast(
            (40.7128, -74.0060),
            timesteps="1h",
            fields=["temperature", "humidity", "windSpeed", "precipitationProbability"]
        )
        
        print("\nHourly forecast:")
        for interval in forecast['data']['timelines'][0]['intervals'][:5]:  # Show next 5 hours
            time = datetime.fromisoformat(interval['startTime'].replace('Z', '+00:00'))
            values = interval['values']
            print(f"\nTime: {time.strftime('%I:%M %p')}")
            print(f"Temperature: {values['temperature']}°F")
            print(f"Humidity: {values['humidity']}%")
            print(f"Wind Speed: {values['windSpeed']} mph")
            print(f"Precipitation Probability: {values['precipitationProbability']}%")
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_weather_service()
