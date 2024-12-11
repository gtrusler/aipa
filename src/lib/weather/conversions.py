from typing import Dict, Any

def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert Celsius to Fahrenheit."""
    return (celsius * 9/5) + 32

def meters_per_second_to_mph(mps: float) -> float:
    """Convert meters per second to miles per hour."""
    return mps * 2.237

def millimeters_to_inches(mm: float) -> float:
    """Convert millimeters to inches."""
    return mm / 25.4

def convert_to_imperial(data: Dict[str, Any]) -> Dict[str, Any]:
    """Convert weather data from metric to imperial units."""
    if 'temperature' in data:
        data['temperature'] = round(celsius_to_fahrenheit(data['temperature']), 1)
    
    if 'windSpeed' in data:
        data['windSpeed'] = round(meters_per_second_to_mph(data['windSpeed']), 1)
    
    if 'precipitation' in data:
        data['precipitation'] = round(millimeters_to_inches(data['precipitation']), 2)
    
    # Add unit labels
    if 'temperature' in data:
        data['temperatureUnit'] = '°F'
    if 'windSpeed' in data:
        data['windSpeedUnit'] = 'mph'
    if 'precipitation' in data:
        data['precipitationUnit'] = 'in'
    
    return data
