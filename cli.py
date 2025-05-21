#!/usr/bin/env python3
# Command-line interface for the Multi-Agent System

import os
import sys
import argparse
from multi_agent_system import MultiAgentSystem
import config

def parse_arguments():
    """Parse command line arguments for the multi-agent system."""
    parser = argparse.ArgumentParser(
        description="Multi-Agent System for Road Condition and Speed Analysis",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument("--lat", type=float, default=config.DEFAULT_LATITUDE,
                        help="Latitude coordinate")
    parser.add_argument("--lon", type=float, default=config.DEFAULT_LONGITUDE,
                        help="Longitude coordinate")
    parser.add_argument("--speed", type=float, default=config.DEFAULT_SPEED,
                        help="Current speed in km/h")
    parser.add_argument("--width", type=float, default=config.DEFAULT_ROAD_WIDTH,
                        help="Road width in meters (optional)")
    parser.add_argument("--api-key", type=str, default=None,
                        help=f"Gemini API key (defaults to {config.API_KEY_ENV_VAR} environment variable). Example: --api-key='YOUR_API_KEY_HERE'")
    parser.add_argument("--json", action="store_true",
                        help="Output results in JSON format")
    
    return parser.parse_args()

def check_api_key(api_key):
    """Check if API key is available, either as argument or environment variable."""
    if api_key:
        return api_key
    
    env_key = os.environ.get(config.API_KEY_ENV_VAR)
    if env_key:
        return env_key
    
    print(f"Error: No API key provided. Please set the {config.API_KEY_ENV_VAR} environment variable or use --api-key.")
    sys.exit(1)

def output_json(analysis):
    """Output analysis as JSON."""
    import json
    print(json.dumps(analysis, indent=2))

def main():
    """Main CLI function."""
    args = parse_arguments()
    
    # Validate API key
    api_key = check_api_key(args.api_key)
    
    # Initialize the multi-agent system
    system = MultiAgentSystem(api_key=api_key)
    
    try:
        print(f"\n🚀 Starting analysis for coordinates ({args.lat}, {args.lon}) at {args.speed} km/h...")
        
        # Run analysis
        analysis = system.analyze_driving_conditions(
            lat=args.lat,
            lon=args.lon,
            speed=args.speed,
            road_width=args.width
        )
        
        # Output results
        if args.json:
            output_json(analysis)
        else:
            system.print_analysis(analysis)
            
    except Exception as e:
        print(f"Error in multi-agent system: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 