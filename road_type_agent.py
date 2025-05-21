# pip install google-genai

import os
from google import genai
from google.genai import types


class RoadTypeAgent:
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = genai.Client(api_key=self.api_key)
        self.model = "gemini-2.0-flash"  # Using Gemini 2.0 Flash
    
    def get_road_type(self, lat, lon, road_width=None):
        """
        Determine the road type at given coordinates using Gemini 2.0 Flash with Google Search.
        Optionally accepts road width to assist classification.
        Returns a single-word category: 'highway', 'rural', or 'city'.
        """
        # Include width information if provided
        width_info = ""
        if road_width is not None:
            width_info = f" The estimated road width is {road_width} meters."
            
        # Construct a strict prompt expecting a one-word response
        contents = [
            types.Content(
                role="user",
                parts=[types.Part.from_text(
                    text=(
                        f"Using ONLY Google Maps, determine the road type at coordinates ({lat}, {lon}).{width_info} "
                        f"Classify it as one of: 'highway' (typically 20+ meters wide), 'rural' (usually 8–20 meters wide), "
                        f"or 'city' (generally under 8 meters). "
                        f"IMPORTANT: Respond ONLY with a single word — 'highway', 'rural', or 'city'. No explanation."
                    )
                )]
            )
        ]

        # Enable Google Search tool
        tools = [types.Tool(google_search=types.GoogleSearch())]

        # Set generation config
        generate_content_config = types.GenerateContentConfig(
            tools=tools,
            response_mime_type="text/plain",
        )

        # Query Gemini
        response = self.client.models.generate_content(
            model=self.model,
            contents=contents,
            config=generate_content_config,
        )

        # Normalize and validate response
        road_type = response.text.strip().lower()
        if "highway" in road_type:
            return "highway"
        elif "rural" in road_type:
            return "rural"
        elif "city" in road_type:
            return "city"
        else:
            return "unknown"
        
    def estimate_road_type_from_width(self, width):
        """
        Estimate road type based solely on width in meters.
        Used as a fallback when geolocation classification is unclear.
        """
        if width is None:
            return "unknown"
        
        if width >= 20:
            return "highway"
        elif 8 <= width < 20:
            return "rural"
        else:
            return "city"


if __name__ == "__main__":
    # Get API key from environment
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
    if not GEMINI_API_KEY:
        raise Exception("Missing GEMINI_API_KEY environment variable")

    agent = RoadTypeAgent(api_key=GEMINI_API_KEY)

    # Test location: Tunis, Tunisia
    lat = 36.7374
    lon = 10.3823

    # Optional road width from sensors (in meters)
    road_width = 15

    try:
        print(f"🔍 Analyzing road at coordinates: ({lat}, {lon})")
        if road_width is not None:
            print(f"📏 Provided road width: {road_width} meters")
            print(f"💡 Width-based estimate: {agent.estimate_road_type_from_width(road_width)}")
        
        # Use Gemini to determine road type
        road_type = agent.get_road_type(lat, lon, road_width)
        print(f"🚦 Gemini 2.0 Flash Road Type: {road_type}")

    except Exception as e:
        print(f"Error: {e}")
