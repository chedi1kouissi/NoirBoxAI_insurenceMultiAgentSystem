# Configuration settings for the Multi-Agent System

# API Settings
API_KEY_ENV_VAR = "GEMINI_API_KEY"  # Name of environment variable for API key

# Default coordinates (Tunis, Tunisia)
DEFAULT_LATITUDE = 36.7374
DEFAULT_LONGITUDE = 10.3823

# Default driving parameters
DEFAULT_SPEED = 80  # km/h
DEFAULT_ROAD_WIDTH = 15  # meters

# Agent models
GEMINI_MODEL = "gemini-2.0-flash"  # Model used by all agents

# Decision Agent settings
SPEED_LIMITS = {
    "city": 50,     # km/h
    "rural": 80,    # km/h
    "highway": 110  # km/h
}

WEATHER_PENALTIES = {
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

# Weather keywords that trigger penalties
BAD_WEATHER_TYPES = ["rainy", "foggy", "snowy", "stormy", "icy", "hail", "thunderstorm", "sleet"]

# Road width thresholds for classification (meters)
ROAD_WIDTH_THRESHOLDS = {
    "highway": 20,  # >= 20 meters
    "rural": 8,     # >= 8 and < 20 meters
    "city": 0       # < 8 meters
} 