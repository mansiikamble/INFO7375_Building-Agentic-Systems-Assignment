"""
REST API for Digital Wellness Coach
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from main import DigitalWellnessCoach, generate_dynamic_sample_data, generate_mood_data
import json
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for web frontends
coach = DigitalWellnessCoach()

@app.route('/')
def home():
    """API documentation"""
    return jsonify({
        "service": "Digital Wellness Coach API",
        "version": "1.0",
        "endpoints": {
            "POST /analyze": "Analyze user's digital wellness",
            "GET /demo/<severity>": "Run demo analysis (light/moderate/heavy)",
            "GET /health": "API health check",
            "GET /sample/<severity>": "Get sample data for testing"
        }
    })

@app.route('/analyze', methods=['POST'])
def analyze_wellness():
    """Analyze user's digital wellness"""
    try:
        user_data = request.json
        
        # Validate required fields
        required_fields = ["apps", "sessions", "app_switches", "duration_minutes"]
        for field in required_fields:
            if field not in user_data:
                return jsonify({
                    "status": "error",
                    "message": f"Missing required field: {field}"
                }), 400
        
        # Run analysis
        result = coach.analyze_user(user_data)
        
        # Extract key metrics from result
        severity = "CRITICAL" if "critical" in str(result).lower() else "MODERATE"
        
        return jsonify({
            "status": "success",
            "severity": severity,
            "analysis": str(result),
            "metrics": {
                "app_switches": user_data["app_switches"],
                "total_minutes": user_data["duration_minutes"],
                "app_count": len(user_data["apps"])
            }
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/demo/<severity>', methods=['GET'])
def demo_analysis(severity):
    """Run demo analysis with different severity levels"""
    if severity not in ["light", "moderate", "heavy"]:
        return jsonify({
            "status": "error",
            "message": "Severity must be: light, moderate, or heavy"
        }), 400
    
    try:
        # Generate appropriate data
        data = generate_dynamic_sample_data(severity)
        mood_data = generate_mood_data(severity)
        
        # Run analysis
        result = coach.analyze_user(data, mood_data)
        
        return jsonify({
            "status": "success",
            "severity": severity,
            "user_data": {
                "app_switches": data["app_switches"],
                "total_minutes": data["duration_minutes"],
                "session_count": len(data["sessions"]),
                "app_count": len(data["apps"])
            },
            "analysis_summary": str(result)[:1000] + "..."  # First 1000 chars
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/sample/<severity>', methods=['GET'])
def get_sample_data(severity):
    """Get sample data for testing"""
    if severity not in ["light", "moderate", "heavy"]:
        return jsonify({
            "status": "error",
            "message": "Severity must be: light, moderate, or heavy"
        }), 400
    
    data = generate_dynamic_sample_data(severity)
    mood_data = generate_mood_data(severity)
    
    return jsonify({
        "usage_data": data,
        "mood_data": mood_data
    })

@app.route('/health', methods=['GET'])
def health_check():
    """API health check"""
    return jsonify({
        "status": "healthy",
        "agents": len(coach.agents),
        "custom_tools": 2,
        "built_in_tools": 3
    })

if __name__ == '__main__':
    print("🚀 Starting Digital Wellness Coach API...")
    print("📍 Access at: http://localhost:5000")
    app.run(debug=True, port=5000)