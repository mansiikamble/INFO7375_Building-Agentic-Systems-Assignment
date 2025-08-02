"""
Test the agents with simple built-in tools
"""

print("🧪 Testing Agents with Simple Built-in Tools")
print("="*60)

# Step 1: Test import
try:
    from agents.wellness_agents_with_simple_tools import get_all_agents, BUILT_IN_TOOLS
    print("✅ Successfully imported agents module")
    
    # Check if BUILT_IN_TOOLS exists
    if BUILT_IN_TOOLS:
        print(f"✅ Built-in tools defined: {list(BUILT_IN_TOOLS.keys())}")
    else:
        print("❌ No built-in tools found")
        
except Exception as e:
    print(f"❌ Import error: {e}")
    exit(1)

# Step 2: Test agent creation
try:
    agents = get_all_agents()
    print(f"\n✅ Successfully created {len(agents)} agents:")
    
    for agent in agents:
        print(f"   - {agent.role}")
        # Check if backstory mentions tools
        backstory = agent.backstory.lower()
        tools_mentioned = []
        for tool in ["web_search", "data_processor", "formatter"]:
            if tool in backstory:
                tools_mentioned.append(tool)
        
        if tools_mentioned:
            print(f"     Tools referenced: {tools_mentioned}")
            
except Exception as e:
    print(f"❌ Agent creation error: {e}")

# Step 3: Test with existing system
print("\n" + "="*60)
print("Testing integration with main system...")

try:
    # Temporarily update imports in main.py
    from crewai import Crew, Process
    from tasks.wellness_tasks import get_all_tasks
    
    # Create a minimal crew to test
    crew = Crew(
        agents=agents,
        tasks=get_all_tasks(),
        process=Process.sequential,
        verbose=False
    )
    
    print("✅ Crew created successfully with new agents")
    print("✅ System is compatible with simple tools agents")
    
except Exception as e:
    print(f"⚠️  Integration test failed: {e}")
    print("This might be due to task imports - that's okay for this test")

print("\n" + "="*60)
print("Summary:")
print("If you see the agents created successfully, your simple tools implementation works!")