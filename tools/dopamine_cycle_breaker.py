"""
Custom Tool: Dopamine Cycle Breaker
Detects and interrupts addictive digital behavior patterns
"""

import json
from datetime import datetime
from typing import Dict

class DopamineCycleBreaker:
    """Tool for analyzing digital usage patterns"""
    
    def __init__(self):
        self.name = "Dopamine Cycle Breaker"
        self.description = "Analyzes app usage patterns to detect addictive behaviors"
    
    def run(self, usage_data: str) -> str:
        """Main method to analyze usage data"""
        try:
            data = json.loads(usage_data)
            
            # Analyze patterns
            patterns = self.analyze_patterns(data)
            
            # Generate interventions
            interventions = self.generate_interventions(patterns)
            
            # Calculate severity
            severity = self.calculate_severity(patterns)
            
            result = {
                "analysis": patterns,
                "interventions": interventions,
                "severity": severity,
                "timestamp": datetime.now().isoformat()
            }
            
            return json.dumps(result, indent=2)
            
        except Exception as e:
            return json.dumps({"error": str(e)})
    
    def analyze_patterns(self, data: Dict) -> Dict:
        """Analyze usage for addictive patterns"""
        patterns = {
            "rapid_app_switching": False,
            "doom_scrolling": False,
            "notification_loops": False,
            "late_night_usage": False,
            "continuous_usage": False
        }
        
        # Check for rapid app switching
        if "app_switches" in data:
            switches_per_hour = data["app_switches"] * (60 / data.get("duration_minutes", 60))
            patterns["rapid_app_switching"] = switches_per_hour > 30
        
        # Check for doom scrolling
        if "scroll_speed" in data:
            patterns["doom_scrolling"] = data["scroll_speed"] > 100
        
        # Check for notification response loops
        if "notification_response_time" in data:
            response_times = data["notification_response_time"]
            if response_times:
                avg_response = sum(response_times) / len(response_times)
                patterns["notification_loops"] = avg_response < 5
        
        # Check for late night usage
        if "usage_times" in data:
            late_night_sessions = [t for t in data["usage_times"] if t.get("hour", 0) >= 22 or t.get("hour", 0) <= 5]
            patterns["late_night_usage"] = len(late_night_sessions) > 0
        
        # Check for continuous usage
        if "session_duration" in data:
            patterns["continuous_usage"] = data["session_duration"] > 90
            
        return patterns
    
    def generate_interventions(self, analysis: Dict) -> list:
        """Generate interventions based on patterns"""
        interventions = []
        
        if analysis["rapid_app_switching"]:
            interventions.append({
                "type": "app_limit",
                "action": "Enable focus mode for 30 minutes",
                "reasoning": "Frequent app switching indicates lack of focus",
                "priority": "high"
            })
        
        if analysis["doom_scrolling"]:
            interventions.append({
                "type": "content_break",
                "action": "Suggest 5-minute breathing exercise",
                "reasoning": "Rapid scrolling often indicates anxiety or boredom",
                "priority": "medium"
            })
        
        if analysis["notification_loops"]:
            interventions.append({
                "type": "notification_management",
                "action": "Batch notifications to hourly summaries",
                "reasoning": "Instant responses create dopamine dependency",
                "priority": "high"
            })
        
        if analysis["late_night_usage"]:
            interventions.append({
                "type": "sleep_hygiene",
                "action": "Enable night mode and set device bedtime",
                "reasoning": "Screen usage affects sleep quality",
                "priority": "critical"
            })
        
        if analysis["continuous_usage"]:
            interventions.append({
                "type": "mandatory_break",
                "action": "Lock entertainment apps for 15 minutes",
                "reasoning": "Eyes and mind need regular breaks",
                "priority": "high"
            })
            
        return interventions
    
    def calculate_severity(self, analysis: Dict) -> str:
        """Calculate overall severity level"""
        active_patterns = sum(1 for v in analysis.values() if v)
        
        if active_patterns >= 4:
            return "CRITICAL"
        elif active_patterns >= 3:
            return "HIGH"
        elif active_patterns >= 2:
            return "MEDIUM"
        elif active_patterns >= 1:
            return "LOW"
        else:
            return "HEALTHY"

# Create instance for easy import
dopamine_cycle_breaker = DopamineCycleBreaker()