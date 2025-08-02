"""
Configuration file for Digital Wellness Coach
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Please set OPENAI_API_KEY in your .env file")

# Agent Configurations
AGENT_CONFIG = {
    "model": "gpt-3.5-turbo",  # or "gpt-4" for better results
    "temperature": 0.7,
    "max_iterations": 3
}

# Wellness Thresholds
WELLNESS_THRESHOLDS = {
    "screen_time_daily_limit": 6,  # hours
    "social_media_daily_limit": 2,  # hours
    "continuous_usage_limit": 1,  # hours without break
    "doom_scroll_threshold": 30,  # rapid swipes per minute
    "app_switch_frequency": 10,  # switches per 5 minutes
    "late_night_usage": 22,  # 10 PM
    "early_morning_usage": 6  # 6 AM
}

# Intervention Strategies
INTERVENTION_LEVELS = {
    "LOW": "Gentle reminder",
    "MEDIUM": "Suggested break activity",
    "HIGH": "Urgent intervention needed",
    "CRITICAL": "Digital detox required"
}

print("✅ Configuration loaded successfully!")