# pip install google-genai requests

import os
from google import genai
from google.genai import types

class WeatherAgent:
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = genai.Client(api_key=self.api_key)
        self.model = "gemini-2.0-flash"  # Updated to Gemini 2.0 Flash

    def get_weather(self, location_name):
        """
        Get weather for a location using Gemini 2.0 Flash with Google Search tool.
        """
        # Create the user prompt
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(
                        text=f"What is the current weather condition in {location_name}? Provide only the temperature and weather condition. Be concise."
                    ),
                ],
            ),
        ]

        # Configure Google Search tool
        tools = [
            types.Tool(google_search=types.GoogleSearch()),
        ]

        # Set configuration
        generate_content_config = types.GenerateContentConfig(
            tools=tools,
            response_mime_type="text/plain",
        )

        # Generate content with Google Search capability
        response = self.client.models.generate_content(
            model=self.model,
            contents=contents,
            config=generate_content_config,
        )

        return response.text.strip()

    def reverse_geocode(self, lat, lon):
        """Convert GPS coordinates to a location name using OpenStreetMap."""
        import requests
        
        url = "https://nominatim.openstreetmap.org/reverse"
        params = {
            "lat": lat,
            "lon": lon,
            "format": "json"
        }
        headers = {
            "User-Agent": "WeatherAgent-Example"
        }
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            address = data.get("address", {})
            return (
                address.get("city") or
                address.get("town") or
                address.get("village") or
                data.get("display_name")
            )
        else:
            raise Exception(f"Reverse geocoding failed: {response.status_code}")


if __name__ == "__main__":
    # Replace these with actual GPS coordinates from your simulated IoT device
    latitude = 36.8065
    longitude = 10.1815

    # Set your Gemini API key in an environment variable or directly here
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
    if not GEMINI_API_KEY:
        raise Exception("Missing GEMINI_API_KEY environment variable")

    agent = WeatherAgent(api_key=GEMINI_API_KEY)

    print("🔁 Reverse geocoding coordinates...")
    try:
        location_name = agent.reverse_geocode(latitude, longitude)
        print(f"📍 Location: {location_name}")

        print("🌤️ Fetching weather with Google Search...")
        weather = agent.get_weather(location_name)
        print(f"🌡️ Weather in {location_name}: {weather}")
    except Exception as e:
        print(f"Error: {e}")

# Optional - Stream the response instead of waiting for complete response
def get_weather_stream(agent, location_name):
    """Get weather for a location using Gemini 2.0 Flash with streaming."""
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(
                    text=f"What is the current weather condition in {location_name}? Provide only the temperature and weather condition. Be concise."
                ),
            ],
        ),
    ]

    tools = [
        types.Tool(google_search=types.GoogleSearch()),
    ]

    generate_content_config = types.GenerateContentConfig(
        tools=tools,
        response_mime_type="text/plain",
    )

    print(f"Streaming weather for {location_name}:")
    for chunk in agent.client.models.generate_content_stream(
        model=agent.model,
        contents=contents,
        config=generate_content_config,
    ):
        print(chunk.text, end="")
    print()  # End with a newline
