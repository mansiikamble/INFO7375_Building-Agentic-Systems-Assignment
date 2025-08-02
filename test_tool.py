"""Test the Dopamine Cycle Breaker tool"""
import json
from tools.dopamine_cycle_breaker import dopamine_cycle_breaker

print("Testing Dopamine Cycle Breaker Tool")
print("="*50)

# Test data - unhealthy usage patterns
test_data = {
    "app_switches": 50,
    "duration_minutes": 60,
    "scroll_speed": 120,
    "notification_response_time": [1, 2, 1, 3, 2],
    "usage_times": [{"hour": 23}, {"hour": 0}, {"hour": 1}],
    "session_duration": 150
}

# Run the tool
result = dopamine_cycle_breaker.run(json.dumps(test_data))
print("\nTool Output:")
print(result)

# Parse and display results nicely
print("\n" + "="*50)
result_dict = json.loads(result)

if "error" not in result_dict:
    print(f"Severity Level: {result_dict['severity']}")
    print(f"\nDetected Patterns:")
    for pattern, detected in result_dict['analysis'].items():
        if detected:
            print(f"  ⚠️  {pattern.replace('_', ' ').title()}")

    print(f"\nRecommended Interventions:")
    for intervention in result_dict['interventions']:
        print(f"  • {intervention['action']}")
        print(f"    Reason: {intervention['reasoning']}")
        print(f"    Priority: {intervention['priority']}")
else:
    print(f"Error: {result_dict['error']}")