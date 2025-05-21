# pip install google-genai

import os
from google import genai
from google.genai import types

class DecisionAgent:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise Exception("Missing GEMINI_API_KEY environment variable or parameter")
        
        self.client = genai.Client(api_key=self.api_key)
        self.model = "gemini-2.0-flash"
        
        # Define speed limits and weather penalties
        self.speed_limits = {
            "city": 50,     # km/h
            "rural": 80,    # km/h
            "highway": 110  # km/h
        }
        
        self.weather_penalties = {
            "rainy": {
                "city": 10,
                "rural": 10,
                "highway": 20
            },
            "foggy": {
                "city": 10,
                "rural": 10,
                "highway": 20
            },
            "snowy": {
                "city": 15,
                "rural": 20,
                "highway": 30
            }
        }
        
        # Default weather types that need penalty
        self.bad_weather_types = ["rainy", "foggy", "snowy", "stormy", "icy", "hail"]
    
    def get_adjusted_speed_limit(self, road_type, weather):
        """Calculate the adjusted speed limit based on road type and weather conditions."""
        # Get base speed limit for the road type
        base_limit = self.speed_limits.get(road_type.lower(), 50)
        
        # Check if the weather requires a penalty
        weather_lower = weather.lower()
        penalty = 0
        
        # Check for exact weather match in penalties
        if weather_lower in self.weather_penalties:
            penalty = self.weather_penalties[weather_lower].get(road_type.lower(), 0)
        # Check for partial matches in bad weather types
        else:
            for bad_weather in self.bad_weather_types:
                if bad_weather in weather_lower:
                    # Apply default penalty for this road type based on rainy condition
                    penalty = self.weather_penalties["rainy"].get(road_type.lower(), 0)
                    break
        
        # Calculate adjusted limit
        adjusted_limit = base_limit - penalty
        
        return {
            "base_limit": base_limit,
            "weather_penalty": penalty,
            "adjusted_limit": adjusted_limit
        }
    
    def evaluate_speed(self, road_type, weather, speed):
        """Evaluate if the current speed violates the adjusted speed limit."""
        # Ensure road_type is valid, default to city if not
        if road_type.lower() not in self.speed_limits:
            road_type = "city"
        
        # Get adjusted speed limit
        limit_info = self.get_adjusted_speed_limit(road_type, weather)
        
        # Check for violation
        violation = speed > limit_info["adjusted_limit"]
        over_by = speed - limit_info["adjusted_limit"] if violation else 0
        
        # Calculate penalty score (example: reduce score by 1 point per 5km/h over the limit)
        penalty = 0
        if violation:
            # Basic penalty calculation
            penalty = min(100, round(over_by / 5) * 5)  # Cap at 100 points penalty
        
        return {
            "violation": violation,
            "base_limit": limit_info["base_limit"],
            "adjusted_limit": limit_info["adjusted_limit"],
            "weather_penalty": limit_info["weather_penalty"],
            "current_speed": speed,
            "over_by": over_by,
            "penalty_points": penalty
        }
    
    def analyze_with_ai(self, road_type, weather, speed):
        """Use Gemini AI to analyze driving behavior and provide insights."""
        # Create the user prompt
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(
                        text=(
                            f"Analyze this driving scenario:\n"
                            f"- Road type: {road_type}\n"
                            f"- Weather condition: {weather}\n"
                            f"- Current speed: {speed} km/h\n\n"
                            f"Based on these conditions, is the driver speeding? "
                            f"For city roads the speed limit is 50 km/h, for rural roads 80 km/h, and for highways 110 km/h. "
                            f"In rainy or foggy conditions, the speed limit is reduced by 10 km/h on city and rural roads, and by 20 km/h on highways. "
                            f"Respond with ONLY ONE WORD: either 'safe' or 'speeding'."
                        )
                    ),
                ],
            ),
        ]

        generate_content_config = types.GenerateContentConfig(
            response_mime_type="text/plain",
        )

        # Generate content
        response = self.client.models.generate_content(
            model=self.model,
            contents=contents,
            config=generate_content_config,
        )

        # Get the one-word response
        ai_assessment = response.text.strip().lower()
        
        return "speeding" if "speed" in ai_assessment else "safe"


if __name__ == "__main__":
    # Set your Gemini API key in an environment variable or directly here
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
    
    agent = DecisionAgent(api_key=GEMINI_API_KEY)
    
    # Test scenarios
    test_scenarios = [
        {"road_type": "city", "weather": "sunny", "speed": 45},
        {"road_type": "city", "weather": "sunny", "speed": 55},
        {"road_type": "city", "weather": "rainy", "speed": 45},
        {"road_type": "highway", "weather": "foggy", "speed": 100},
        {"road_type": "highway", "weather": "foggy", "speed": 95},
        {"road_type": "rural", "weather": "snowy", "speed": 75},
    ]
    
    # Test each scenario
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n--- Scenario {i} ---")
        road_type = scenario["road_type"]
        weather = scenario["weather"]
        speed = scenario["speed"]
        
        print(f"🛣️  Road type: {road_type}")
        print(f"🌤️  Weather: {weather}")
        print(f"🚗  Speed: {speed} km/h")
        
        # Evaluate with rules engine
        result = agent.evaluate_speed(road_type, weather, speed)
        
        # AI-based analysis (optional)
        ai_result = agent.analyze_with_ai(road_type, weather, speed)
        
        # Display results
        print(f"⚙️  Base speed limit: {result['base_limit']} km/h")
        if result['weather_penalty'] > 0:
            print(f"⚠️  Weather penalty: -{result['weather_penalty']} km/h")
        print(f"🚸  Adjusted speed limit: {result['adjusted_limit']} km/h")
        
        if result['violation']:
            print(f"❌  VIOLATION: {result['over_by']} km/h over limit")
            print(f"📉  Penalty: -{result['penalty_points']} points")
        else:
            print(f"✅  COMPLIANT: Within speed limit")
            
        # Compare with AI assessment
        print(f"🤖  AI assessment: {ai_result.upper()}")


# Function to integrate with other agents
def process_driving_data(road_type, weather, speed, api_key=None):
    """
    Process driving data and return decision results.
    This function can be imported and used in other scripts.
    """
    agent = DecisionAgent(api_key=api_key)
    result = agent.evaluate_speed(road_type, weather, speed)
    
    return {
        "road_type": road_type,
        "weather": weather,
        "speed": speed,
        "base_limit": result["base_limit"],
        "adjusted_limit": result["adjusted_limit"],
        "violation": result["violation"],
        "penalty_points": result["penalty_points"] if result["violation"] else 0
    }