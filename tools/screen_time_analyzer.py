"""
Screen Time Analyzer Tool
Provides detailed analysis of device usage patterns
"""

import json
from datetime import datetime
from typing import Dict, List

class ScreenTimeAnalyzer:
    """Tool for analyzing screen time data"""
    
    def __init__(self):
        self.name = "Screen Time Analyzer"
        self.description = "Analyzes device usage patterns and provides insights"
    
    def run(self, device_data: str) -> str:
        """Analyze screen time data"""
        try:
            data = json.loads(device_data)
            
            analysis = {
                "total_screen_time": self._calculate_total_time(data),
                "app_breakdown": self._analyze_app_usage(data),
                "peak_usage_times": self._find_peak_times(data),
                "usage_trends": self._analyze_trends(data),
                "wellness_score": self._calculate_wellness_score(data),
                "recommendations": self._generate_recommendations(data)
            }
            
            return json.dumps(analysis, indent=2)
            
        except Exception as e:
            return json.dumps({"error": str(e)})
    
    def _calculate_total_time(self, data: Dict) -> Dict:
        """Calculate total screen time"""
        total_minutes = sum(app.get("duration", 0) for app in data.get("apps", []))
        hours = total_minutes // 60
        minutes = total_minutes % 60
        
        return {
            "hours": hours,
            "minutes": minutes,
            "total_minutes": total_minutes,
            "formatted": f"{hours}h {minutes}m"
        }
    
    def _analyze_app_usage(self, data: Dict) -> Dict:
        """Break down usage by app category"""
        categories = {}
        app_details = []
        
        for app in data.get("apps", []):
            category = app.get("category", "Other")
            duration = app.get("duration", 0)
            
            categories[category] = categories.get(category, 0) + duration
            app_details.append({
                "name": app.get("name"),
                "category": category,
                "duration": duration,
                "percentage": 0  # Will calculate after
            })
        
        # Calculate percentages
        total = sum(categories.values())
        if total > 0:
            for app in app_details:
                app["percentage"] = round((app["duration"] / total) * 100, 1)
        
        return {
            "by_category": categories,
            "by_app": sorted(app_details, key=lambda x: x["duration"], reverse=True)
        }
    
    def _find_peak_times(self, data: Dict) -> List[Dict]:
        """Identify peak usage times"""
        hourly_usage = {}
        
        for session in data.get("sessions", []):
            hour = session.get("hour", 0)
            duration = session.get("duration", 0)
            hourly_usage[hour] = hourly_usage.get(hour, 0) + duration
        
        # Sort by usage and get top 3
        peak_hours = sorted(hourly_usage.items(), key=lambda x: x[1], reverse=True)[:3]
        
        return [
            {
                "hour": hour,
                "duration": duration,
                "period": self._get_time_period(hour)
            }
            for hour, duration in peak_hours
        ]
    
    def _get_time_period(self, hour: int) -> str:
        """Convert hour to time period"""
        if 5 <= hour < 12:
            return "Morning"
        elif 12 <= hour < 17:
            return "Afternoon"
        elif 17 <= hour < 21:
            return "Evening"
        else:
            return "Night"
    
    def _analyze_trends(self, data: Dict) -> Dict:
        """Analyze usage trends"""
        daily_usage = data.get("daily_usage", [])
        
        if len(daily_usage) < 2:
            trend = "Insufficient data"
        else:
            recent_avg = sum(daily_usage[-3:]) / min(3, len(daily_usage))
            older_avg = sum(daily_usage[:-3]) / max(1, len(daily_usage) - 3)
            
            if recent_avg > older_avg * 1.1:
                trend = "Increasing"
            elif recent_avg < older_avg * 0.9:
                trend = "Decreasing"
            else:
                trend = "Stable"
        
        return {
            "overall_trend": trend,
            "daily_average": sum(daily_usage) / len(daily_usage) if daily_usage else 0,
            "most_used_app": self._find_most_used_app(data)
        }
    
    def _find_most_used_app(self, data: Dict) -> str:
        """Find the most frequently used app"""
        apps = data.get("apps", [])
        if not apps:
            return "No data"
        return max(apps, key=lambda x: x.get("duration", 0)).get("name", "Unknown")
    
    def _calculate_wellness_score(self, data: Dict) -> Dict:
        """Calculate digital wellness score (0-100)"""
        score = 100
        penalties = []
        
        # Check total time
        total_minutes = sum(app.get("duration", 0) for app in data.get("apps", []))
        if total_minutes > 360:  # 6 hours
            penalty = min(20, (total_minutes - 360) / 10)
            score -= penalty
            penalties.append(f"Excessive screen time: -{penalty:.0f}")
        
        # Check social media time
        social_time = sum(
            app.get("duration", 0) for app in data.get("apps", [])
            if app.get("category") == "Social Media"
        )
        if social_time > 120:  # 2 hours
            penalty = min(15, (social_time - 120) / 8)
            score -= penalty
            penalties.append(f"High social media use: -{penalty:.0f}")
        
        # Check late night usage
        late_sessions = [
            s for s in data.get("sessions", [])
            if s.get("hour", 0) >= 22 or s.get("hour", 0) <= 5
        ]
        if late_sessions:
            penalty = min(15, len(late_sessions) * 5)
            score -= penalty
            penalties.append(f"Late night usage: -{penalty:.0f}")
        
        return {
            "score": max(0, round(score)),
            "rating": self._get_rating(score),
            "penalties": penalties
        }
    
    def _get_rating(self, score: float) -> str:
        """Get rating based on score"""
        if score >= 80:
            return "Excellent"
        elif score >= 60:
            return "Good"
        elif score >= 40:
            return "Fair"
        else:
            return "Poor"
    
    def _generate_recommendations(self, data: Dict) -> List[str]:
        """Generate personalized recommendations"""
        recommendations = []
        
        total_minutes = sum(app.get("duration", 0) for app in data.get("apps", []))
        if total_minutes > 360:
            recommendations.append("Set daily screen time limits to under 6 hours")
        
        social_time = sum(
            app.get("duration", 0) for app in data.get("apps", [])
            if app.get("category") == "Social Media"
        )
        if social_time > 120:
            recommendations.append("Reduce social media usage to under 2 hours daily")
        
        late_sessions = [
            s for s in data.get("sessions", [])
            if s.get("hour", 0) >= 22
        ]
        if late_sessions:
            recommendations.append("Avoid screens 1 hour before bedtime for better sleep")
        
        if not recommendations:
            recommendations.append("Great job! Maintain your healthy digital habits")
        
        return recommendations

# Create instance for easy import
screen_time_analyzer = ScreenTimeAnalyzer()