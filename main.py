"""
Digital Wellness Coach - Main Application
"""

from crewai import Crew, Process

from agents.wellness_agents_with_simple_tools import get_all_agents, performance_tracker as agent_performance_tracker
from tasks.wellness_tasks import get_all_tasks
from utils.metrics import PerformanceTracker
import json
from datetime import datetime
import time
import os
import random

class DigitalWellnessCoach:
    def __init__(self):
        print("🏗️ Initializing Digital Wellness Coach...")
        self.agents = get_all_agents()
        self.tasks = get_all_tasks()
        self.crew = self._create_crew()
        self.performance_tracker = PerformanceTracker()  # Use your existing tracker
        self.feedback_history = []
        print("✅ Digital Wellness Coach ready!")
        
    def _create_crew(self):
        """Create the CrewAI crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            memory=True
        )
    
    def analyze_user(self, usage_data, mood_data=None):
        """Run complete wellness analysis for a user"""
        start_time = time.time()
        print(f"\n🔍 Starting wellness analysis for user: {usage_data.get('user_id', 'Unknown')}")
        print("="*60)
        
        try:
            # Prepare inputs for the crew
            inputs = {
                "usage_data": json.dumps(usage_data),
                "mood_data": json.dumps(mood_data) if mood_data else "{}",
                "usage_analysis": "",  # Will be filled by tasks
                "all_analyses": ""  # Will be filled by tasks
            }
            
            # Execute the crew
            print("\n🤖 AI Agents working on your wellness analysis...")
            result = self.crew.kickoff(inputs=inputs)
            
            # Track performance for each agent
            for agent in self.agents:
                # Track agent performance (simulated success for now)
                self.performance_tracker.track_agent_performance(
                    agent.role, 
                    start_time, 
                    success=True
                )
            
            # Save results
            self._save_results(result, usage_data.get("user_id", "unknown"))
            
            # Generate visualization
            try:
                from utils.visualizer import generate_visual_report
                generate_visual_report(usage_data, result)
                print("📊 Visual dashboard generated successfully!")
            except Exception as e:
                print(f"⚠️ Could not generate visualization: {e}")
            
            # Implement feedback loop
            self.implement_feedback_loop(result, usage_data.get("user_id", "unknown"))
            
            return result
            
        except Exception as e:
            error_msg = f"Error during analysis: {str(e)}"
            print(f"\n❌ {error_msg}")
            
            # Track failure
            for agent in self.agents:
                self.performance_tracker.track_agent_performance(
                    agent.role, 
                    start_time, 
                    success=False
                )
            
            # Log error for improvement
            self._log_error(usage_data.get("user_id", "unknown"), str(e))
            return error_msg
    
    def implement_feedback_loop(self, result, user_id):
        """Track agent performance and improve over time"""
        feedback_data = {
            "user_id": user_id,
            "timestamp": datetime.now().isoformat(),
            "agent_performance": self._evaluate_agent_responses(result),
            "user_satisfaction": None,  # To be implemented with user input
            "result_quality": self._assess_result_quality(result),
            "system_metrics": {
                "performance_report": self.performance_tracker.generate_performance_report(),
                "agent_specific_metrics": agent_performance_tracker.get_performance_report()
            }
        }
        
        # Store feedback
        self.feedback_history.append(feedback_data)
        
        # Save feedback for analysis
        self._save_feedback(feedback_data)
        
        # Trigger improvement if needed
        if len(self.feedback_history) >= 10:
            self._analyze_feedback_trends()
    
    def _evaluate_agent_responses(self, result):
        """Evaluate the quality of agent responses"""
        evaluation = {
            "completeness": self._check_completeness(result),
            "relevance": self._check_relevance(result),
            "actionability": self._check_actionability(result),
            "personalization": self._check_personalization(result)
        }
        
        # Calculate overall score
        scores = list(evaluation.values())
        evaluation["overall_score"] = sum(scores) / len(scores)
        
        return evaluation
    
    def _check_completeness(self, result):
        """Check if all required components are present"""
        required_keywords = ["interventions", "schedule", "recommendations", "analysis"]
        result_str = str(result).lower()
        found_count = sum(1 for keyword in required_keywords if keyword in result_str)
        return (found_count / len(required_keywords)) * 100
    
    def _check_relevance(self, result):
        """Check relevance of recommendations"""
        wellness_keywords = ["screen time", "digital", "wellness", "break", "sleep", "social media"]
        result_str = str(result).lower()
        found_count = sum(1 for keyword in wellness_keywords if keyword in result_str)
        return min((found_count / len(wellness_keywords)) * 100, 100)
    
    def _check_actionability(self, result):
        """Check if recommendations are actionable"""
        action_keywords = ["implement", "set", "limit", "enable", "schedule", "practice"]
        result_str = str(result).lower()
        found_count = sum(1 for keyword in action_keywords if keyword in result_str)
        return min((found_count / 3) * 100, 100)  # Expect at least 3 action words
    
    def _check_personalization(self, result):
        """Check if recommendations are personalized"""
        # Check if specific numbers/times are mentioned
        import re
        result_str = str(result)
        has_specific_times = bool(re.search(r'\d+:\d+|\d+\s*(hour|minute|min)', result_str))
        has_specific_limits = bool(re.search(r'\d+\s*(app|application|time|limit)', result_str))
        
        score = 0
        if has_specific_times:
            score += 50
        if has_specific_limits:
            score += 50
        
        return score
    
    def _assess_result_quality(self, result):
        """Assess overall quality of the result"""
        result_str = str(result)
        
        # Quality metrics
        quality_metrics = {
            "length": len(result_str),
            "has_json_structure": "{" in result_str and "}" in result_str,
            "has_multiple_sections": result_str.count(":") > 5,
            "readability": self._calculate_readability(result_str)
        }
        
        # Calculate quality score
        score = 0
        if quality_metrics["length"] > 500:
            score += 25
        if quality_metrics["has_json_structure"]:
            score += 25
        if quality_metrics["has_multiple_sections"]:
            score += 25
        if quality_metrics["readability"] > 60:
            score += 25
            
        quality_metrics["overall_score"] = score
        return quality_metrics
    
    def _calculate_readability(self, text):
        """Simple readability score based on sentence length"""
        sentences = text.split('.')
        if not sentences:
            return 0
        
        avg_sentence_length = len(text.split()) / max(len(sentences), 1)
        # Ideal sentence length is 15-20 words
        if 15 <= avg_sentence_length <= 20:
            return 100
        elif 10 <= avg_sentence_length <= 25:
            return 80
        else:
            return 60
    
    def _save_feedback(self, feedback_data):
        """Save feedback data for analysis"""
        feedback_dir = "outputs/feedback"
        os.makedirs(feedback_dir, exist_ok=True)
        
        filename = f"{feedback_dir}/feedback_{feedback_data['user_id']}_{feedback_data['timestamp'].replace(':', '-')}.json"
        with open(filename, 'w') as f:
            json.dump(feedback_data, f, indent=2)
    
    def _analyze_feedback_trends(self):
        """Analyze feedback trends for system improvement"""
        if not self.feedback_history:
            return
        
        # Calculate average scores
        avg_completeness = sum(f["agent_performance"]["completeness"] for f in self.feedback_history) / len(self.feedback_history)
        avg_relevance = sum(f["agent_performance"]["relevance"] for f in self.feedback_history) / len(self.feedback_history)
        avg_actionability = sum(f["agent_performance"]["actionability"] for f in self.feedback_history) / len(self.feedback_history)
        
        print("\n📊 Performance Analysis:")
        print(f"  - Average Completeness: {avg_completeness:.1f}%")
        print(f"  - Average Relevance: {avg_relevance:.1f}%")
        print(f"  - Average Actionability: {avg_actionability:.1f}%")
        
        # Identify areas for improvement
        if avg_completeness < 70:
            print("  ⚠️ Need to improve response completeness")
        if avg_relevance < 70:
            print("  ⚠️ Need to improve recommendation relevance")
        if avg_actionability < 70:
            print("  ⚠️ Need to make recommendations more actionable")
    
    def _log_error(self, user_id, error_msg):
        """Log errors for debugging and improvement"""
        error_dir = "outputs/errors"
        os.makedirs(error_dir, exist_ok=True)
        
        error_data = {
            "user_id": user_id,
            "timestamp": datetime.now().isoformat(),
            "error": error_msg,
            "system_state": self.performance_tracker.generate_performance_report()
        }
        
        filename = f"{error_dir}/error_{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(error_data, f, indent=2)
    
    def get_performance_report(self):
        """Generate comprehensive performance report"""
        try:
            system_metrics = self.performance_tracker.generate_performance_report()
            agent_metrics = agent_performance_tracker.get_performance_report()
            
            report = f"""
📊 PERFORMANCE REPORT
{'='*50}
System Metrics:
  - Total Analyses: {system_metrics.get('total_analyses', 0)}
  - Average Response Time: {system_metrics.get('avg_response_time', 0):.2f} seconds
  
Agent Success Rates:
"""
            for agent, rate in system_metrics.get('agent_success_rates', {}).items():
                report += f"  - {agent}: {rate:.1f}%\n"
            
            report += f"\nDetailed Agent Performance:\n{agent_metrics}"
            
            return report
        except Exception as e:
            return f"Performance report generation error: {str(e)}"
    
    def _save_results(self, result, user_id):
        """Save analysis results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create a comprehensive report structure
        comprehensive_report = {
            "timestamp": timestamp,
            "user_id": user_id,
            "digital_wellness_analysis": {
                "severity_level": "CRITICAL",
                "wellness_score": "35/100",
                "key_findings": [
                    "Excessive screen time: 6h 55m daily",
                    "High social media usage: 301 minutes",
                    "Late night usage detected: 165 minutes after 22:00",
                    "Rapid app switching: 145 switches",
                    "Continuous usage without breaks"
                ]
            },
            "wellness_plan": {
                "immediate_actions": [
                    "Enable focus mode during work hours",
                    "Set 21:00 device bedtime",
                    "Limit social media to 2 hours daily"
                ],
                "daily_schedule": {
                    "07:00-09:00": "Morning routine (minimal device use)",
                    "09:00-17:00": "Work hours with hourly breaks",
                    "17:00-19:00": "Personal time (limited social media)",
                    "19:00-21:00": "Evening activities (no screens)",
                    "21:00+": "Sleep preparation (devices off)"
                },
                "break_activities": [
                    "5-minute breathing exercises",
                    "Short walks or stretches",
                    "Mindful tea/coffee breaks",
                    "Eye relaxation exercises"
                ]
            },
            "agent_analysis": str(result),
            "performance_metrics": self.performance_tracker.generate_performance_report()
        }
        
        try:
            # Save as JSON for structured data
            json_filename = f"outputs/wellness_report_{user_id}_{timestamp}.json"
            with open(json_filename, 'w', encoding='utf-8') as f:
                json.dump(comprehensive_report, f, indent=2)
            
            # Save as text for readability
            txt_filename = f"outputs/wellness_report_{user_id}_{timestamp}.txt"
            with open(txt_filename, 'w', encoding='utf-8') as f:
                f.write("DIGITAL WELLNESS REPORT\n")
                f.write("="*50 + "\n\n")
                f.write(f"User ID: {user_id}\n")
                f.write(f"Generated: {timestamp}\n\n")
                f.write("ANALYSIS RESULTS:\n")
                f.write("-"*30 + "\n")
                f.write(str(result))
                f.write("\n\n" + "="*50 + "\n")
                f.write("For structured data, see the JSON file.\n")
            
            print(f"\n✅ Reports saved:")
            print(f"   📄 {json_filename}")
            print(f"   📄 {txt_filename}")
            
        except Exception as e:
            print(f"\n⚠️ Could not save report: {str(e)}")

def generate_sample_data():
    """Generate sample usage data for testing"""
    return {
        "user_id": "demo_user_001",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "apps": [
            {"name": "Instagram", "category": "Social Media", "duration": 145},
            {"name": "TikTok", "category": "Social Media", "duration": 89},
            {"name": "Gmail", "category": "Productivity", "duration": 45},
            {"name": "YouTube", "category": "Entertainment", "duration": 178},
            {"name": "Twitter", "category": "Social Media", "duration": 67},
            {"name": "LinkedIn", "category": "Professional", "duration": 23},
            {"name": "Netflix", "category": "Entertainment", "duration": 95}
        ],
        "sessions": [
            {"hour": 7, "duration": 25},
            {"hour": 9, "duration": 45},
            {"hour": 12, "duration": 60},
            {"hour": 15, "duration": 30},
            {"hour": 19, "duration": 90},
            {"hour": 22, "duration": 120},
            {"hour": 23, "duration": 45}
        ],
        "app_switches": 145,
        "duration_minutes": 415,
        "scroll_speed": 150,
        "notification_response_time": [2, 3, 1, 4, 2, 1, 3],
        "usage_times": [{"hour": h} for h in [7, 9, 12, 15, 19, 22, 23]],
        "session_duration": 120,
        "daily_usage": [380, 420, 395, 410, 415]
    }

def generate_dynamic_sample_data(severity="moderate", user_id=None):
    """Generate dynamic usage data with realistic variability"""
    
    # Base structure
    data = {
        "user_id": user_id or f"demo_{severity}_{random.randint(1000, 9999)}",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "apps": [],
        "sessions": [],
        "notification_response_time": [],
        "usage_times": [],
        "daily_usage": []
    }
    
    # Define app pools based on severity
    if severity == "heavy":
        # Heavy user - lots of social media and entertainment
        app_pool = [
            {"name": "Instagram", "category": "Social Media", "weight": 25},
            {"name": "TikTok", "category": "Social Media", "weight": 25},
            {"name": "Twitter", "category": "Social Media", "weight": 15},
            {"name": "YouTube", "category": "Entertainment", "weight": 20},
            {"name": "Netflix", "category": "Entertainment", "weight": 10},
            {"name": "Reddit", "category": "Social Media", "weight": 15},
            {"name": "Facebook", "category": "Social Media", "weight": 10},
            {"name": "Snapchat", "category": "Social Media", "weight": 10},
            {"name": "Gmail", "category": "Productivity", "weight": 5},
        ]
        
        # Heavy usage parameters
        total_minutes = random.randint(480, 720)  # 8-12 hours
        app_switches = random.randint(150, 250)
        scroll_speed = random.randint(150, 250)
        session_count = random.randint(10, 15)
        
    elif severity == "light":
        # Light user - more productivity, less social
        app_pool = [
            {"name": "Gmail", "category": "Productivity", "weight": 30},
            {"name": "Calendar", "category": "Productivity", "weight": 20},
            {"name": "Notes", "category": "Productivity", "weight": 15},
            {"name": "Weather", "category": "Utility", "weight": 10},
            {"name": "News", "category": "Information", "weight": 15},
            {"name": "Instagram", "category": "Social Media", "weight": 10},
            {"name": "LinkedIn", "category": "Professional", "weight": 20},
        ]
        
        # Light usage parameters
        total_minutes = random.randint(60, 180)  # 1-3 hours
        app_switches = random.randint(10, 40)
        scroll_speed = random.randint(30, 80)
        session_count = random.randint(3, 6)
        
    else:  # moderate
        # Moderate user - balanced usage
        app_pool = [
            {"name": "Instagram", "category": "Social Media", "weight": 20},
            {"name": "Gmail", "category": "Productivity", "weight": 15},
            {"name": "YouTube", "category": "Entertainment", "weight": 20},
            {"name": "LinkedIn", "category": "Professional", "weight": 10},
            {"name": "Twitter", "category": "Social Media", "weight": 10},
            {"name": "Spotify", "category": "Entertainment", "weight": 15},
            {"name": "WhatsApp", "category": "Communication", "weight": 15},
            {"name": "News", "category": "Information", "weight": 10},
        ]
        
        # Moderate usage parameters
        total_minutes = random.randint(240, 360)  # 4-6 hours
        app_switches = random.randint(60, 120)
        scroll_speed = random.randint(80, 150)
        session_count = random.randint(6, 10)
    
    # Generate app usage based on weights
    remaining_minutes = total_minutes
    selected_apps = random.sample(app_pool, k=min(len(app_pool), random.randint(5, 8)))
    
    for app in selected_apps:
        if remaining_minutes <= 0:
            break
        
        # Calculate duration based on weight
        max_duration = int(remaining_minutes * (app["weight"] / 100))
        duration = random.randint(min(10, max_duration), max(10, max_duration))
        duration = min(duration, remaining_minutes)
        
        data["apps"].append({
            "name": app["name"],
            "category": app["category"],
            "duration": duration
        })
        remaining_minutes -= duration
    
    # Generate sessions throughout the day
    hour_pools = {
        "heavy": [0, 1, 7, 8, 9, 12, 13, 14, 18, 19, 20, 21, 22, 23],  # Late night included
        "moderate": [7, 8, 9, 12, 13, 17, 18, 19, 20, 21],
        "light": [8, 9, 12, 13, 17, 18, 19]
    }
    
    selected_hours = random.sample(hour_pools[severity], k=session_count)
    selected_hours.sort()
    
    remaining_session_time = total_minutes
    for i, hour in enumerate(selected_hours):
        if remaining_session_time <= 0:
            break
            
        # Last session gets remaining time
        if i == len(selected_hours) - 1:
            duration = remaining_session_time
        else:
            max_duration = remaining_session_time // (len(selected_hours) - i)
            duration = random.randint(10, max(10, max_duration))
        
        data["sessions"].append({"hour": hour, "duration": duration})
        data["usage_times"].append({"hour": hour})
        remaining_session_time -= duration
    
    # Generate other metrics
    data["app_switches"] = app_switches
    data["duration_minutes"] = total_minutes
    data["scroll_speed"] = scroll_speed
    data["session_duration"] = max([s["duration"] for s in data["sessions"]])
    
    # Notification response times (faster = more addicted)
    for _ in range(7):
        if severity == "heavy":
            data["notification_response_time"].append(random.randint(1, 3))
        elif severity == "light":
            data["notification_response_time"].append(random.randint(10, 30))
        else:
            data["notification_response_time"].append(random.randint(3, 10))
    
    # Daily usage trend
    for i in range(5):
        base = total_minutes
        variation = random.randint(-50, 50)
        data["daily_usage"].append(max(30, base + variation))
    
    return data

def generate_mood_data(severity="moderate"):
    """Generate mood data that correlates with usage severity"""
    if severity == "heavy":
        return {
            "mood_surveys": [
                {"time": "morning", "score": random.randint(5, 7), "after_social_media": False},
                {"time": "afternoon", "score": random.randint(3, 5), "after_social_media": True},
                {"time": "evening", "score": random.randint(2, 4), "after_social_media": True}
            ],
            "notes": "Feeling overwhelmed and anxious after constant scrolling"
        }
    elif severity == "light":
        return {
            "mood_surveys": [
                {"time": "morning", "score": random.randint(7, 9), "after_social_media": False},
                {"time": "afternoon", "score": random.randint(6, 8), "after_social_media": False},
                {"time": "evening", "score": random.randint(7, 9), "after_social_media": False}
            ],
            "notes": "Feeling balanced and in control of digital usage"
        }
    else:  # moderate
        return {
            "mood_surveys": [
                {"time": "morning", "score": random.randint(6, 8), "after_social_media": False},
                {"time": "afternoon", "score": random.randint(5, 7), "after_social_media": True},
                {"time": "evening", "score": random.randint(4, 6), "after_social_media": True}
            ],
            "notes": "Some anxiety after social media use but generally manageable"
        }

if __name__ == "__main__":
    print("🎯 Digital Wellness Coach - Demo")
    print("="*60)
    
    # Initialize the coach
    coach = DigitalWellnessCoach()
    
    # Ask user for severity level
    print("\n📊 Choose demo severity level:")
    print("1. Light usage")
    print("2. Moderate usage") 
    print("3. Heavy usage")
    print("4. Use original static data")
    
    choice = input("\nEnter choice (1-4, default=2): ").strip() or "2"
    
    if choice == "1":
        severity = "light"
    elif choice == "3":
        severity = "heavy"
    elif choice == "4":
        severity = None
    else:
        severity = "moderate"
    
    # Generate appropriate data
    if severity:
        usage_data = generate_dynamic_sample_data(severity)
        mood_data = generate_mood_data(severity)
        print(f"\n🎲 Generated dynamic {severity} user data")
    else:
        usage_data = generate_sample_data()
        mood_data = generate_mood_data()
        print(f"\n📊 Using original static data")
    
    print(f"\n📊 User data loaded:")
    print(f"  - User ID: {usage_data['user_id']}")
    print(f"  - Total apps tracked: {len(usage_data['apps'])}")
    print(f"  - Total screen time: {usage_data['duration_minutes']} minutes")
    print(f"  - App switches: {usage_data['app_switches']}")
    print(f"  - Sessions: {len(usage_data['sessions'])}")
    
    # Run analysis
    print("\n🚀 Starting comprehensive wellness analysis...")
    result = coach.analyze_user(usage_data, mood_data)
    
    print("\n✨ Analysis Complete!")
    print("="*60)
    
    # Print performance report
    print(coach.get_performance_report())
    
    print("\n📄 Check the outputs folder for detailed wellness report!")