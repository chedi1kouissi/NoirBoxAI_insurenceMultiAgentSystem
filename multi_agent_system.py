# pip install google-genai requests

import os
import time
from google import genai
import config

# Import agents from their respective modules
from road_type_agent import RoadTypeAgent
from weather_agent import WeatherAgent
from decision_making_agent import DecisionAgent

class MultiAgentSystem:
    def __init__(self, api_key=None):
        """Initialize the multi-agent system with a shared API key."""
        self.api_key = api_key or os.environ.get(config.API_KEY_ENV_VAR)
        if not self.api_key:
            raise Exception(f"Missing {config.API_KEY_ENV_VAR} environment variable or parameter")
        
        # Initialize all agents with the same API key
        self.road_agent = RoadTypeAgent(api_key=self.api_key)
        self.weather_agent = WeatherAgent(api_key=self.api_key)
        self.decision_agent = DecisionAgent(api_key=self.api_key)
    
    def analyze_driving_conditions(self, lat, lon, speed, road_width=None):
        """
        Analyze driving conditions by coordinating all agents.
        
        Args:
            lat (float): Latitude coordinate
            lon (float): Longitude coordinate
            speed (float): Current speed in km/h
            road_width (float, optional): Road width in meters if available
            
        Returns:
            dict: Complete analysis of driving conditions and recommendations
        """
        results = {
            "location": {
                "latitude": lat,
                "longitude": lon
            },
            "speed": speed,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Step 1: Determine road type using RoadTypeAgent
        print("🛣️ Analyzing road type...")
        road_type = self.road_agent.get_road_type(lat, lon, road_width)
        results["road_type"] = road_type
        
        if road_width:
            results["road_width"] = road_width
            results["road_type_estimate"] = self.road_agent.estimate_road_type_from_width(road_width)
        
        # Step 2: Get location name and weather using WeatherAgent
        try:
            print("📍 Determining location name...")
            location_name = self.weather_agent.reverse_geocode(lat, lon)
            results["location_name"] = location_name
            
            print(f"🌤️ Checking weather conditions in {location_name}...")
            weather = self.weather_agent.get_weather(location_name)
            results["weather"] = weather
        except Exception as e:
            print(f"Weather data unavailable: {e}")
            weather = "unknown"
            results["weather"] = "unknown"
            results["weather_error"] = str(e)
        
        # Step 3: Make driving decision using DecisionAgent
        print("🚦 Evaluating driving conditions...")
        decision = self.decision_agent.evaluate_speed(road_type, weather, speed)
        results["speed_analysis"] = decision
        
        # Step 4: Get AI assessment
        print("🤖 Getting AI assessment...")
        ai_assessment = self.decision_agent.analyze_with_ai(road_type, weather, speed)
        results["ai_assessment"] = ai_assessment
        
        return results
    
    def print_analysis(self, analysis):
        """Print a formatted analysis report."""
        print("\n" + "="*50)
        print(f"🌍 LOCATION: {analysis.get('location_name', 'Unknown')} ({analysis['location']['latitude']}, {analysis['location']['longitude']})")
        print(f"⏱️ TIME: {analysis['timestamp']}")
        print("-"*50)
        
        print(f"🛣️ ROAD TYPE: {analysis['road_type'].upper()}")
        if 'road_width' in analysis:
            print(f"📏 ROAD WIDTH: {analysis['road_width']} meters")
        
        print(f"🌤️ WEATHER: {analysis['weather']}")
        print(f"🚗 CURRENT SPEED: {analysis['speed']} km/h")
        print("-"*50)
        
        speed_analysis = analysis['speed_analysis']
        print(f"⚙️ BASE SPEED LIMIT: {speed_analysis['base_limit']} km/h")
        if speed_analysis['weather_penalty'] > 0:
            print(f"⚠️ WEATHER PENALTY: -{speed_analysis['weather_penalty']} km/h")
        print(f"🚸 ADJUSTED SPEED LIMIT: {speed_analysis['adjusted_limit']} km/h")
        
        if speed_analysis['violation']:
            print(f"❌ VIOLATION: {speed_analysis['over_by']} km/h over limit")
            print(f"📉 PENALTY: -{speed_analysis['penalty_points']} points")
        else:
            print(f"✅ COMPLIANT: Within speed limit")
            
        print(f"🤖 AI ASSESSMENT: {analysis['ai_assessment'].upper()}")
        print("="*50)


if __name__ == "__main__":
    # Set your Gemini API key in an environment variable
    GEMINI_API_KEY = os.environ.get(config.API_KEY_ENV_VAR)
    if not GEMINI_API_KEY:
        raise Exception(f"Missing {config.API_KEY_ENV_VAR} environment variable")
    
    # Initialize the multi-agent system
    system = MultiAgentSystem(api_key=GEMINI_API_KEY)
    
    # Test coordinates (Tunis, Tunisia)
    lat = 36.7374
    lon = 10.3823
    speed = 85  # km/h
    road_width = 15  # meters, optional
    
    try:
        print("\n🚀 Starting multi-agent analysis...")
        analysis = system.analyze_driving_conditions(lat, lon, speed, road_width)
        system.print_analysis(analysis)
    except Exception as e:
        print(f"Error in multi-agent system: {e}") 