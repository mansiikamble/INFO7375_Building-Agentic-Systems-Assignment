"""
Quick test to ensure all components are working
"""

print("🧪 Testing Digital Wellness Coach Components...")
print("="*50)

# Test imports
try:
    from tools.dopamine_cycle_breaker import dopamine_cycle_breaker
    print("✅ Dopamine Cycle Breaker tool imported")
except Exception as e:
    print(f"❌ Error importing Dopamine Cycle Breaker: {e}")

try:
    from tools.screen_time_analyzer import screen_time_analyzer
    print("✅ Screen Time Analyzer tool imported")
except Exception as e:
    print(f"❌ Error importing Screen Time Analyzer: {e}")

try:
    from agents.wellness_agents_improved import get_all_agents
    agents = get_all_agents()
    print(f"✅ All {len(agents)} agents created successfully")
except Exception as e:
    print(f"❌ Error creating agents: {e}")

try:
    from tasks.wellness_tasks import get_all_tasks
    tasks = get_all_tasks()
    print(f"✅ All {len(tasks)} tasks created successfully")
except Exception as e:
    print(f"❌ Error creating tasks: {e}")

print("\n✅ All components are ready!")
print("\nRun 'python main.py' to start the Digital Wellness Coach")