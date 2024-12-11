from src.lib.weather.allergy import AllergyClient
import asyncio

async def main():
    print("Testing allergy data for Austin, TX...")
    
    try:
        client = AllergyClient()
        
        # Austin coordinates
        lat, lon = 30.2672, -97.7431
        
        pollen_data = await client.get_pollen_data(lat, lon)
        
        if pollen_data:
            print("\nPollen Data:")
            print(f"Overall Risk: {pollen_data.get('overall_risk', 'Unknown').replace('_', ' ').title()}")
            print("\nDetailed Levels:")
            if 'tree_pollen' in pollen_data:
                print(f"Tree Pollen: {pollen_data['tree_pollen']['level'].replace('_', ' ').title()}")
            if 'grass_pollen' in pollen_data:
                print(f"Grass Pollen: {pollen_data['grass_pollen']['level'].replace('_', ' ').title()}")
            if 'weed_pollen' in pollen_data:
                print(f"Weed Pollen: {pollen_data['weed_pollen']['level'].replace('_', ' ').title()}")
        else:
            print("No pollen data available")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
