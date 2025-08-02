"""Performance metrics for Digital Wellness Coach"""
import time
from datetime import datetime

class PerformanceTracker:
    def __init__(self):
        self.metrics = {
            "response_times": [],
            "agent_success_rates": {},
            "tool_usage_stats": {},
            "memory_usage": []
        }
    
    def track_agent_performance(self, agent_name, start_time, success):
        """Track individual agent performance"""
        duration = time.time() - start_time
        self.metrics["response_times"].append(duration)
        
        if agent_name not in self.metrics["agent_success_rates"]:
            self.metrics["agent_success_rates"][agent_name] = {"success": 0, "total": 0}
        
        self.metrics["agent_success_rates"][agent_name]["total"] += 1
        if success:
            self.metrics["agent_success_rates"][agent_name]["success"] += 1
    
    def generate_performance_report(self):
        """Generate performance metrics report"""
        return {
            "avg_response_time": sum(self.metrics["response_times"]) / len(self.metrics["response_times"]),
            "agent_success_rates": {
                agent: (stats["success"] / stats["total"] * 100)
                for agent, stats in self.metrics["agent_success_rates"].items()
            },
            "total_analyses": len(self.metrics["response_times"])
        }