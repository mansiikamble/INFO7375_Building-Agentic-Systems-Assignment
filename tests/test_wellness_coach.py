"""Test cases for Digital Wellness Coach"""
import unittest
import json
import os
import time
from main import DigitalWellnessCoach, generate_sample_data, generate_mood_data
from tools.dopamine_cycle_breaker import dopamine_cycle_breaker
from tools.screen_time_analyzer import screen_time_analyzer

class TestDigitalWellnessCoach(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        self.coach = DigitalWellnessCoach()
        # Create output directory if it doesn't exist
        os.makedirs("outputs", exist_ok=True)
        os.makedirs("outputs/feedback", exist_ok=True)
        os.makedirs("outputs/errors", exist_ok=True)
        
    def test_heavy_user_analysis(self):
        """Test analysis of heavy user patterns"""
        heavy_user_data = generate_sample_data()
        heavy_user_data["app_switches"] = 200  # Very high
        heavy_user_data["session_duration"] = 180  # 3 hours continuous
        heavy_user_data["duration_minutes"] = 600  # 10 hours total
        heavy_user_data["sessions"].append({"hour": 2, "duration": 120})  # Late night usage
        
        result = self.coach.analyze_user(heavy_user_data)
        self.assertIsNotNone(result)
        
        # Verify critical severity detected
        result_str = str(result).lower()
        self.assertTrue(
            "critical" in result_str or 
            "severe" in result_str or 
            "high" in result_str,
            "Heavy usage should trigger high severity warnings"
        )
        
    def test_healthy_user_analysis(self):
        """Test analysis of healthy usage patterns"""
        healthy_user_data = generate_sample_data()
        healthy_user_data["app_switches"] = 20
        healthy_user_data["duration_minutes"] = 120  # 2 hours
        healthy_user_data["sessions"] = [
            {"hour": 9, "duration": 30},
            {"hour": 13, "duration": 45},
            {"hour": 18, "duration": 45}
        ]
        healthy_user_data["apps"] = [
            {"name": "Gmail", "category": "Productivity", "duration": 45},
            {"name": "Calendar", "category": "Productivity", "duration": 30},
            {"name": "News", "category": "Information", "duration": 45}
        ]
        
        result = self.coach.analyze_user(healthy_user_data)
        self.assertIsNotNone(result)
        
        # Verify healthier patterns recognized
        result_str = str(result).lower()
        self.assertFalse(
            "critical" in result_str,
            "Healthy usage should not trigger critical warnings"
        )
        
    def test_custom_tools(self):
        """Test custom tool functionality"""
        # Test Dopamine Cycle Breaker
        test_data = json.dumps({
            "app_switches": 150,
            "scroll_speed": 200,
            "notification_response_time": [1, 1, 2, 1],
            "usage_times": [{"hour": 23}, {"hour": 0}],
            "session_duration": 150,
            "duration_minutes": 300
        })
        
        result = dopamine_cycle_breaker.run(test_data)
        self.assertIsNotNone(result)
        self.assertIn("CRITICAL", result)
        
        # Verify interventions are generated
        result_dict = json.loads(result)
        self.assertIn("interventions", result_dict)
        self.assertGreater(len(result_dict["interventions"]), 0)
        
    def test_screen_time_analyzer(self):
        """Test Screen Time Analyzer tool"""
        test_data = generate_sample_data()
        
        result = screen_time_analyzer.run(json.dumps(test_data))
        self.assertIsNotNone(result)
        
        # Verify analysis contains expected components
        result_dict = json.loads(result)
        self.assertIn("total_screen_time", result_dict)
        self.assertIn("app_breakdown", result_dict)
        self.assertIn("peak_usage_times", result_dict)
        self.assertIn("wellness_score", result_dict)
        self.assertIn("recommendations", result_dict)
        
    def test_mood_correlation(self):
        """Test mood data integration"""
        usage_data = generate_sample_data()
        mood_data = generate_mood_data()
        
        # Add more social media usage
        usage_data["apps"][0]["duration"] = 200  # Increase Instagram time
        
        result = self.coach.analyze_user(usage_data, mood_data)
        self.assertIsNotNone(result)
        
        # Verify mood data is considered
        result_str = str(result).lower()
        self.assertTrue(
            "mood" in result_str or 
            "emotional" in result_str or 
            "anxiety" in result_str,
            "Analysis should consider mood data"
        )
        
    def test_performance_tracking(self):
        """Test performance tracking functionality"""
        # Run multiple analyses
        for i in range(3):
            data = generate_sample_data()
            data["user_id"] = f"test_user_{i}"
            self.coach.analyze_user(data)
        
        # Get performance report
        report = self.coach.get_performance_report()
        self.assertIsNotNone(report)
        self.assertIn("Total Analyses", report)
        self.assertIn("Average Response Time", report)
        
    def test_feedback_loop(self):
        """Test feedback loop implementation"""
        usage_data = generate_sample_data()
        result = self.coach.analyze_user(usage_data)
        
        # Check feedback was recorded
        self.assertGreater(len(self.coach.feedback_history), 0)
        
        # Verify feedback structure
        feedback = self.coach.feedback_history[-1]
        self.assertIn("agent_performance", feedback)
        self.assertIn("result_quality", feedback)
        self.assertIn("system_metrics", feedback)
        
    def test_error_handling(self):
        """Test error handling and recovery"""
        # Test with invalid data
        invalid_data = {"user_id": "test_error", "invalid_field": "test"}
        
        result = self.coach.analyze_user(invalid_data)
        self.assertIsNotNone(result)  # Should handle error gracefully
        
        # Check error was logged
        error_files = os.listdir("outputs/errors") if os.path.exists("outputs/errors") else []
        self.assertGreater(len(error_files), 0, "Errors should be logged")
        
    def test_edge_cases(self):
        """Test edge cases and boundary conditions"""
        # Test with minimal usage
        minimal_data = generate_sample_data()
        minimal_data["apps"] = [{"name": "Calculator", "category": "Utility", "duration": 5}]
        minimal_data["duration_minutes"] = 5
        minimal_data["app_switches"] = 1
        minimal_data["sessions"] = [{"hour": 12, "duration": 5}]
        
        result = self.coach.analyze_user(minimal_data)
        self.assertIsNotNone(result)
        
        # Test with extreme usage
        extreme_data = generate_sample_data()
        extreme_data["duration_minutes"] = 1440  # 24 hours
        extreme_data["app_switches"] = 500
        
        result = self.coach.analyze_user(extreme_data)
        self.assertIsNotNone(result)
        
    def test_report_generation(self):
        """Test report generation and saving"""
        usage_data = generate_sample_data()
        result = self.coach.analyze_user(usage_data)
        
        # Check if reports were saved
        output_files = os.listdir("outputs")
        json_files = [f for f in output_files if f.endswith('.json') and 'wellness_report' in f]
        txt_files = [f for f in output_files if f.endswith('.txt') and 'wellness_report' in f]
        
        self.assertGreater(len(json_files), 0, "JSON report should be saved")
        self.assertGreater(len(txt_files), 0, "Text report should be saved")
        
        # Verify JSON report structure
        if json_files:
            with open(f"outputs/{json_files[-1]}", 'r') as f:
                report_data = json.load(f)
                self.assertIn("digital_wellness_analysis", report_data)
                self.assertIn("wellness_plan", report_data)
                self.assertIn("performance_metrics", report_data)

class TestIntegration(unittest.TestCase):
    """Integration tests for the complete system"""
    
    def test_full_workflow(self):
        """Test complete analysis workflow"""
        coach = DigitalWellnessCoach()
        
        # Generate comprehensive test data
        usage_data = generate_sample_data()
        mood_data = generate_mood_data()
        
        # Run analysis
        start_time = time.time()
        result = coach.analyze_user(usage_data, mood_data)
        end_time = time.time()
        
        # Verify completion
        self.assertIsNotNone(result)
        
        # Check performance
        execution_time = end_time - start_time
        self.assertLess(execution_time, 60, "Analysis should complete within 60 seconds")
        
        # Verify all components worked
        self.assertIn("Digital Wellness Plan", str(result))
        
    def test_multiple_users(self):
        """Test system with multiple user profiles"""
        coach = DigitalWellnessCoach()
        
        user_profiles = [
            {"type": "heavy_user", "app_switches": 200, "duration_minutes": 600},
            {"type": "moderate_user", "app_switches": 50, "duration_minutes": 240},
            {"type": "light_user", "app_switches": 10, "duration_minutes": 60}
        ]
        
        results = []
        for profile in user_profiles:
            data = generate_sample_data()
            data["user_id"] = profile["type"]
            data["app_switches"] = profile["app_switches"]
            data["duration_minutes"] = profile["duration_minutes"]
            
            result = coach.analyze_user(data)
            results.append(result)
        
        # Verify all analyses completed
        self.assertEqual(len(results), 3)
        for result in results:
            self.assertIsNotNone(result)

def run_specific_test(test_name):
    """Run a specific test by name"""
    suite = unittest.TestSuite()
    suite.addTest(TestDigitalWellnessCoach(test_name))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

if __name__ == "__main__":
    # Run all tests
    unittest.main(verbosity=2)
    
    # Or run specific test:
    # run_specific_test('test_heavy_user_analysis')