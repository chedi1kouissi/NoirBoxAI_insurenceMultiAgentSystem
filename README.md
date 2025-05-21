# Multi-Agent Driving Analysis System

A coordinated multi-agent system that uses Google's Gemini 2.0 Flash to analyze driving conditions, road types, weather, and provide speed recommendations.

## Overview

This system combines three specialized AI agents:

1. **Road Type Agent**: Determines the type of road at specific GPS coordinates (highway, rural, or city)
2. **Weather Agent**: Identifies the location name and current weather conditions
3. **Decision Agent**: Evaluates if the current speed is appropriate for the road type and weather conditions

The system coordinates these agents to provide a comprehensive driving analysis, including speed recommendations and safety assessments.

## Requirements

- Python 3.7+
- Google Gemini API key
- Required packages:
  - `google-genai`
  - `requests`

## Installation

1. Clone this repository
2. Install required packages:
   ```
   pip install -r requirements.txt
   ```
3. Set up your Gemini API key using one of these methods:
   
   **Option 1:** Set as an environment variable:
   ```
   # On Windows
   set GEMINI_API_KEY=your-api-key-here
   
   # On macOS/Linux
   export GEMINI_API_KEY=your-api-key-here
   ```
   
   **Option 2:** Pass directly to the CLI:
   ```
   python cli.py --api-key="your-api-key-here" --lat 36.7374 --lon 10.3823
   ```

## Usage

### Command Line Interface

The system includes a CLI for easy interaction:

```
python cli.py --lat 36.7374 --lon 10.3823 --speed 85 --width 15
```

Options:
- `--lat`: Latitude coordinate (default: 36.7374)
- `--lon`: Longitude coordinate (default: 10.3823)
- `--speed`: Current speed in km/h (default: 80)
- `--width`: Road width in meters (optional, default: 15)
- `--api-key`: Gemini API key (defaults to GEMINI_API_KEY environment variable)
- `--json`: Output results in JSON format

### Python API

You can also use the system programmatically:

```python
from multi_agent_system import MultiAgentSystem

# Initialize the system
system = MultiAgentSystem(api_key="your-api-key")

# Analyze driving conditions
analysis = system.analyze_driving_conditions(
    lat=36.7374,
    lon=10.3823,
    speed=85,
    road_width=15
)

# Print formatted results
system.print_analysis(analysis)
```

## Configuration

System parameters can be customized in `config.py`, including:
- Default coordinates and driving parameters
- Speed limits for different road types
- Weather penalty factors
- Road width classification thresholds

## Components

### 1. Road Type Agent (`road_type_agent.py`)

Uses Gemini 2.0 Flash with Google Search to classify roads at specific GPS coordinates as:
- Highway (wide roads, typically 20+ meters)
- Rural (medium width roads, typically 8-20 meters)
- City (narrow roads, typically less than 8 meters)

Can also estimate road type based on width when provided.

### 2. Weather Agent (`weather_agent.py`)

Performs reverse geocoding to convert GPS coordinates to location names, then fetches current weather conditions for that location.

### 3. Decision Agent (`decision_making_agent.py`)

Evaluates if the current speed is safe based on:
- Road type (city, rural, highway)
- Weather conditions (applies penalties for adverse weather)
- Current speed

Provides safety assessments and recommendations.

## License

This project is MIT licensed. See LICENSE file for details.

## Acknowledgments

- Uses Google's Gemini 2.0 Flash AI models
- Weather data via Google Search
- Reverse geocoding via OpenStreetMap Nominatim 