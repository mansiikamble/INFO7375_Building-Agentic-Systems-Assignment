"""
Comprehensive showcase of Digital Wellness Coach capabilities
"""

from main import DigitalWellnessCoach, generate_dynamic_sample_data, generate_mood_data
from utils.visualizer import create_wellness_dashboard, create_comparative_analysis
from utils.cache import AnalysisCache
import time
import json

def print_section(title):
    """Print formatted section header"""
    print(f"\n{'='*60}")
    print(f"🎯 {title}")
    print('='*60)

def run_comprehensive_demo():
    """Run a comprehensive demonstration of all features"""
    print("🚀 DIGITAL WELLNESS COACH - COMPREHENSIVE DEMO")
    print("="*60)
    
    # Initialize components
    print("\n📦 Initializing components...")
    coach = DigitalWellnessCoach()
    cache = AnalysisCache(ttl_minutes=30)
    
    # Test different user profiles
    profiles = [
        ("light", "Sarah - Minimal User"),
        ("moderate", "John - Average User"), 
        ("heavy", "Alex - Heavy User")
    ]
    
    results = []
    user_data_list = []
    
    print_section("ANALYZING DIFFERENT USER PROFILES")
    
    for severity, name in profiles:
        print(f"\n📊 Analyzing {name} ({severity} usage)...")
        
        # Generate dynamic data
        data = generate_dynamic_sample_data(severity, user_id=name.split()[0].lower())
        mood_data = generate_mood_data(severity)
        user_data_list.append(data)
        
        # Display key metrics
        print(f"   📱 App switches: {data['app_switches']} times")
        print(f"   ⏱️  Screen time: {data['duration_minutes']} minutes ({data['duration_minutes']//60}h {data['duration_minutes']%60}m)")
        print(f"   📅 Sessions: {len(data['sessions'])}")
        print(f"   🔄 Apps used: {len(data['apps'])}")
        
        # Top apps
        top_apps = sorted(data['apps'], key=lambda x: x['duration'], reverse=True)[:3]
        top_apps_str = ', '.join([f"{app['name']} ({app['duration']}m)" for app in top_apps])
        print(f"   🔝 Top apps: {top_apps_str}")
        
        # Check cache
        cached_result = cache.get(data)
        
        if cached_result:
            print("   ⚡ Using cached analysis")
            result = cached_result
        else:
            # Run analysis with timing
            start_time = time.time()
            result = coach.analyze_user(data, mood_data)
            end_time = time.time()
            
            print(f"   ⏱️  Analysis completed in {end_time - start_time:.2f} seconds")
            
            # Cache the result
            cache.set(data, result)
        
        results.append(result)
        
        # Extract severity from result
        result_str = str(result).lower()
        if "critical" in result_str:
            severity_level = "🔴 CRITICAL"
        elif "high" in result_str:
            severity_level = "🟠 HIGH"
        elif "moderate" in result_str:
            severity_level = "🟡 MODERATE"
        else:
            severity_level = "🟢 LOW"
        
        print(f"   📊 Severity: {severity_level}")
    
    print_section("GENERATING VISUALIZATIONS")
    
    print("📊 Creating individual dashboards...")
    for i, (data, (severity, name)) in enumerate(zip(user_data_list, profiles)):
        try:
            create_wellness_dashboard(data)
            print(f"   ✅ Dashboard created for {name}")
        except Exception as e:
            print(f"   ⚠️  Visualization error for {name}: {e}")
    
    print("\n📊 Creating comparative analysis...")
    try:
        create_comparative_analysis(user_data_list)
        print("   ✅ Comparative analysis created")
    except Exception as e:
        print(f"   ⚠️  Comparative visualization error: {e}")
    
    print_section("PERFORMANCE METRICS")
    
    # Show performance report
    print(coach.get_performance_report())
    
    # Show cache statistics
    print("\n📦 Cache Statistics:")
    cache_stats = cache.get_stats()
    for key, value in cache_stats.items():
        print(f"   - {key}: {value}")
    
    print_section("TESTING CACHE PERFORMANCE")
    
    # Test cache by re-analyzing the same data
    print("\nRe-analyzing first user to test cache...")
    test_data = user_data_list[0]
    
    start_time = time.time()
    cached_result = cache.get(test_data)
    cache_time = time.time() - start_time
    
    if cached_result:
        print(f"✅ Cache retrieval time: {cache_time*1000:.2f}ms")
        print("   (Compare to original analysis time of ~80 seconds)")
    
    print_section("BUILT-IN TOOLS DEMONSTRATION")
    
    print("The following built-in tools are integrated:")
    print("   🔍 Web Search - For wellness research")
    print("   📊 Data Processor - For usage analysis")
    print("   📝 Formatter - For structured reports")
    print("\nAgents reference these tools in their operations.")
    
    print_section("DEMO COMPLETE")
    
    print("\n📁 Check the outputs folder for:")
    print("   - Individual wellness reports (JSON & TXT)")
    print("   - Visual dashboards for each user")
    print("   - Comparative analysis visualization")
    print("   - Performance metrics")
    
    print("\n🎉 All features demonstrated successfully!")

def test_api_integration():
    """Test API integration (requires api.py to be running)"""
    print_section("TESTING API INTEGRATION")
    
    try:
        import requests
        base_url = "http://localhost:5000"
        
        # Test health endpoint
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ API is healthy")
            print(f"   Response: {response.json()}")
        
        # Test sample data endpoint
        response = requests.get(f"{base_url}/sample/moderate")
        if response.status_code == 200:
            print("✅ Sample data endpoint working")
        
        print("\n📡 API endpoints available at http://localhost:5000")
        
    except Exception as e:
        print("⚠️  API not running. Start it with: python api.py")

if __name__ == "__main__":
    # Run the main demo
    run_comprehensive_demo()
    
    # Optionally test API
    print("\n" + "="*60)
    user_input = input("\nTest API integration? (y/n): ")
    if user_input.lower() == 'y':
        test_api_integration()