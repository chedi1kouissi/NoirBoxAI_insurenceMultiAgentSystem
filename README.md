Multi-Agent Driving Analysis System
A coordinated multi-agent system powered by Google Gemini 2.0 Flash that analyzes real-time driving conditions—factoring in road type, weather, and road geometry—to provide intelligent speed recommendations and safety assessments.

🚗 Designed for in-vehicle IoT integration:
This system is intended to be deployed on IoT devices installed in vehicles. It enables insurance companies to evaluate driver behavior, promote responsible driving, and build accurate driver scoring models. Additional behavioral scoring features will be added in future versions.

🚦 Overview
This modular system integrates three intelligent agents working in coordination:

Road Type Agent
Identifies road categories—city, rural, or highway—based on GPS coordinates and road width.

Weather Agent
Converts coordinates to a location name and fetches current weather conditions using web search and APIs.

Decision Agent
Assesses whether the current speed is appropriate based on:

Detected road type

Weather status

Road geometry (optional width input)

Customizable safety thresholds

Together, they form a real-time assistant for driving safety analysis and speed compliance.

📦 Requirements
Python 3.7+

Google Gemini API key

Dependencies:

google-genai

requests

🚀 Installation
Clone the repository:

bash
Copier
Modifier
git clone https://github.com/yourusername/multi-agent-driving-analysis.git
cd multi-agent-driving-analysis
Install required packages:

bash
Copier
Modifier
pip install -r requirements.txt
Set up your Gemini API key:

Option 1: Environment variable

bash
Copier
Modifier
# Windows
set GEMINI_API_KEY=your-api-key

# macOS/Linux
export GEMINI_API_KEY=your-api-key
Option 2: CLI parameter

bash
Copier
Modifier
python cli.py --api-key="your-api-key" --lat 36.7374 --lon 10.3823
🧪 Usage
🔧 Command Line Interface
Run the system directly from the terminal:

bash
Copier
Modifier
python cli.py --lat 36.7374 --lon 10.3823 --speed 85 --width 15
Options:

--lat: Latitude (default: 36.7374)

--lon: Longitude (default: 10.3823)

--speed: Current speed in km/h (default: 80)

--width: Optional road width in meters (default: 15)

--api-key: Gemini API key (overrides environment variable)

--json: Output results in JSON format

🐍 Python API
Use the system within your own Python scripts:

python
Copier
Modifier
from multi_agent_system import MultiAgentSystem

system = MultiAgentSystem(api_key="your-api-key")

result = system.analyze_driving_conditions(
    lat=36.7374,
    lon=10.3823,
    speed=85,
    road_width=15
)

system.print_analysis(result)
⚙️ Configuration
Tune system logic in config.py:

Default coordinates and speed

Speed limits per road type

Weather impact penalties

Road width classification

🧠 System Architecture
road_type_agent.py
Uses Gemini 2.0 Flash + Google Search

Classifies roads as:

Highway: Typically ≥20m wide

Rural: ~8–20m wide

City: ≤8m wide

Falls back to road width if satellite classification is unavailable

weather_agent.py
Uses reverse geocoding (OpenStreetMap Nominatim)

Queries weather using location names

Extracts weather status (e.g., sunny, rainy) for safety evaluation

decision_making_agent.py
Integrates road type, speed, and weather to:

Determine safety of current speed

Apply penalties for adverse weather

Recommend safer speeds if necessary

🧭 Future Plans
Driver scoring system based on:

Speed compliance trends

Weather-aware risk behavior

Road-type adaptation

Integration with insurance dashboards

Real-time feedback to drivers via IoT interfaces

📄 License
This project is licensed under the MIT License. See the LICENSE file for details.

🙏 Acknowledgments
Built with Google Gemini 2.0 Flash

Weather and location data via Google Search + OpenStreetMap Nominatim

Inspired by smart mobility and insurtech innovation
