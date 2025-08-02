"""Visualization tools for wellness reports"""
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import numpy as np
import json

# Set style for better-looking plots
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

def create_wellness_dashboard(usage_data, analysis_results=None):
    """Create a comprehensive visual dashboard of wellness metrics"""
    fig = plt.figure(figsize=(16, 12))
    
    # Create a more complex grid layout
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    
    # 1. Daily Usage Pattern (larger, top row)
    ax1 = fig.add_subplot(gs[0, :2])
    hours = [s["hour"] for s in usage_data["sessions"]]
    durations = [s["duration"] for s in usage_data["sessions"]]
    
    # Create a more detailed bar chart with color coding
    colors = ['green' if h < 22 and h > 6 else 'red' for h in hours]
    bars = ax1.bar(hours, durations, color=colors, alpha=0.7, edgecolor='black')
    
    # Add threshold line
    ax1.axhline(y=60, color='orange', linestyle='--', label='Recommended limit (60 min/session)')
    
    ax1.set_title('Daily Usage Pattern', fontsize=16, fontweight='bold')
    ax1.set_xlabel('Hour of Day', fontsize=12)
    ax1.set_ylabel('Duration (minutes)', fontsize=12)
    ax1.legend()
    ax1.set_xticks(range(0, 24, 2))
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax1.annotate(f'{int(height)}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=8)
    
    # 2. App Category Breakdown (top right)
    ax2 = fig.add_subplot(gs[0, 2])
    categories = {}
    for app in usage_data["apps"]:
        cat = app["category"]
        categories[cat] = categories.get(cat, 0) + app["duration"]
    
    # Create a more stylish pie chart
    colors_pie = plt.cm.Set3(np.linspace(0, 1, len(categories)))
    wedges, texts, autotexts = ax2.pie(categories.values(), labels=categories.keys(), 
                                        autopct='%1.1f%%', colors=colors_pie,
                                        explode=[0.05] * len(categories),
                                        shadow=True, startangle=90)
    
    # Improve text appearance
    for text in texts:
        text.set_fontsize(10)
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(9)
    
    ax2.set_title('Usage by Category', fontsize=14, fontweight='bold')
    
    # 3. Wellness Score Gauge (middle left)
    ax3 = fig.add_subplot(gs[1, 0])
    wellness_score = extract_wellness_score(analysis_results) if analysis_results else 35
    
    # Create a gauge-like visualization
    create_gauge(ax3, wellness_score)
    ax3.set_title('Digital Wellness Score', fontsize=14, fontweight='bold')
    
    # 4. App Usage Ranking (middle center)
    ax4 = fig.add_subplot(gs[1, 1])
    apps_sorted = sorted(usage_data["apps"], key=lambda x: x["duration"], reverse=True)[:5]
    app_names = [app["name"] for app in apps_sorted]
    app_durations = [app["duration"] for app in apps_sorted]
    
    bars = ax4.barh(app_names, app_durations, color='skyblue')
    ax4.set_xlabel('Duration (minutes)', fontsize=12)
    ax4.set_title('Top 5 Apps by Usage', fontsize=14, fontweight='bold')
    
    # Add value labels
    for i, (bar, duration) in enumerate(zip(bars, app_durations)):
        ax4.text(bar.get_width() + 3, bar.get_y() + bar.get_height()/2, 
                f'{duration}m', va='center', fontsize=10)
    
    # 5. Intervention Timeline (middle right)
    ax5 = fig.add_subplot(gs[1, 2])
    interventions = ['Immediate:\nFocus Mode', 'Short-term:\nApp Limits', 'Long-term:\nDigital Detox']
    timeline = [1, 7, 30]  # days
    colors_timeline = ['red', 'orange', 'green']
    
    ax5.scatter(timeline, [1, 1, 1], s=300, c=colors_timeline, alpha=0.7, edgecolors='black')
    
    for i, txt in enumerate(interventions):
        ax5.annotate(txt, (timeline[i], 1), xytext=(0, 30), 
                    textcoords='offset points', ha='center', fontsize=10,
                    bbox=dict(boxstyle="round,pad=0.3", facecolor=colors_timeline[i], alpha=0.3))
    
    ax5.set_xlabel('Days', fontsize=12)
    ax5.set_xlim(0, 35)
    ax5.set_ylim(0.5, 1.5)
    ax5.set_title('Intervention Timeline', fontsize=14, fontweight='bold')
    ax5.set_yticks([])
    
    # 6. Usage Trend (bottom left)
    ax6 = fig.add_subplot(gs[2, 0])
    daily_usage = usage_data.get("daily_usage", [380, 420, 395, 410, 415])
    days = list(range(1, len(daily_usage) + 1))
    
    ax6.plot(days, daily_usage, marker='o', linewidth=2, markersize=8, color='darkblue')
    ax6.fill_between(days, daily_usage, alpha=0.3, color='lightblue')
    ax6.axhline(y=360, color='red', linestyle='--', label='Recommended limit (6 hours)')
    
    ax6.set_xlabel('Days', fontsize=12)
    ax6.set_ylabel('Minutes', fontsize=12)
    ax6.set_title('5-Day Usage Trend', fontsize=14, fontweight='bold')
    ax6.legend()
    ax6.grid(True, alpha=0.3)
    
    # 7. Notification Response Pattern (bottom center)
    ax7 = fig.add_subplot(gs[2, 1])
    response_times = usage_data.get("notification_response_time", [2, 3, 1, 4, 2, 1, 3])
    
    ax7.hist(response_times, bins=range(0, max(response_times) + 2), 
             color='purple', alpha=0.7, edgecolor='black')
    ax7.axvline(x=5, color='green', linestyle='--', label='Healthy response (>5s)')
    
    ax7.set_xlabel('Response Time (seconds)', fontsize=12)
    ax7.set_ylabel('Frequency', fontsize=12)
    ax7.set_title('Notification Response Pattern', fontsize=14, fontweight='bold')
    ax7.legend()
    
    # 8. Addiction Indicators (bottom right)
    ax8 = fig.add_subplot(gs[2, 2])
    indicators = extract_addiction_indicators(analysis_results) if analysis_results else {
        'App Switching': 85,
        'Doom Scrolling': 70,
        'Late Night Use': 90,
        'Continuous Use': 80,
        'Notification Loops': 75
    }
    
    # Create a radar chart
    create_radar_chart(ax8, indicators)
    ax8.set_title('Digital Addiction Indicators', fontsize=14, fontweight='bold')
    
    # Add overall title and timestamp
    fig.suptitle(f'Digital Wellness Dashboard - {usage_data.get("user_id", "User")}', 
                 fontsize=18, fontweight='bold', y=0.98)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fig.text(0.99, 0.01, f'Generated: {timestamp}', ha='right', va='bottom', 
             fontsize=10, style='italic', alpha=0.7)
    
    # Save the dashboard
    plt.tight_layout()
    output_path = f'outputs/wellness_dashboard_{usage_data.get("user_id", "user")}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    
    print(f"📊 Dashboard saved to: {output_path}")
    return fig

def create_gauge(ax, score):
    """Create a gauge visualization for wellness score"""
    # Create the gauge
    theta = np.linspace(0, np.pi, 100)
    r_inner = 0.7
    r_outer = 1.0
    
    # Color zones
    colors = ['red', 'orange', 'yellow', 'lightgreen', 'green']
    boundaries = [0, 20, 40, 60, 80, 100]
    
    for i in range(len(colors)):
        theta_start = np.pi * (1 - boundaries[i] / 100)
        theta_end = np.pi * (1 - boundaries[i + 1] / 100)
        theta_range = np.linspace(theta_start, theta_end, 50)
        
        x_inner = r_inner * np.cos(theta_range)
        y_inner = r_inner * np.sin(theta_range)
        x_outer = r_outer * np.cos(theta_range)
        y_outer = r_outer * np.sin(theta_range)
        
        verts = list(zip(x_outer, y_outer)) + list(zip(x_inner[::-1], y_inner[::-1]))
        poly = plt.Polygon(verts, facecolor=colors[i], edgecolor='white')
        ax.add_patch(poly)
    
    # Add needle
    angle = np.pi * (1 - score / 100)
    x_needle = [0, 0.9 * np.cos(angle)]
    y_needle = [0, 0.9 * np.sin(angle)]
    ax.plot(x_needle, y_needle, 'k-', linewidth=3)
    ax.plot(0, 0, 'ko', markersize=10)
    
    # Add score text
    ax.text(0, -0.3, f'{score}/100', ha='center', va='center', 
            fontsize=24, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
    
    # Add labels
    ax.text(0, -0.5, get_wellness_rating(score), ha='center', va='center', 
            fontsize=16, style='italic')
    
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-0.6, 1.2)
    ax.axis('off')

def create_radar_chart(ax, indicators):
    """Create a radar chart for addiction indicators"""
    categories = list(indicators.keys())
    values = list(indicators.values())
    
    # Number of variables
    num_vars = len(categories)
    
    # Compute angle for each axis
    angles = [n / float(num_vars) * 2 * np.pi for n in range(num_vars)]
    values += values[:1]  # Complete the circle
    angles += angles[:1]
    
    # Initialize the plot
    ax = plt.subplot(projection='polar', position=ax.get_position())
    
    # Draw the outline of our data
    ax.plot(angles, values, 'o-', linewidth=2, color='red')
    ax.fill(angles, values, alpha=0.25, color='red')
    
    # Fix axis to go in the right order and start at 12 o'clock
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    
    # Draw axis lines for each angle and label
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, size=10)
    
    # Set y-axis limits and labels
    ax.set_ylim(0, 100)
    ax.set_yticks([20, 40, 60, 80])
    ax.set_yticklabels(['20', '40', '60', '80'], size=8)
    
    # Add grid
    ax.grid(True)

def get_wellness_rating(score):
    """Get wellness rating based on score"""
    if score >= 80:
        return "Excellent"
    elif score >= 60:
        return "Good"
    elif score >= 40:
        return "Fair"
    else:
        return "Poor"

def extract_wellness_score(analysis_results):
    """Extract wellness score from analysis results"""
    if not analysis_results:
        return 35
    
    # Try to extract score from results
    result_str = str(analysis_results)
    if "wellness_score" in result_str:
        # Simple extraction - you might need to adjust based on actual format
        try:
            import re
            match = re.search(r'wellness_score["\s:]+(\d+)', result_str)
            if match:
                return int(match.group(1))
        except:
            pass
    
    return 35  # Default score

def extract_addiction_indicators(analysis_results):
    """Extract addiction indicators from analysis results"""
    # Default values
    default_indicators = {
        'App Switching': 85,
        'Doom Scrolling': 70,
        'Late Night Use': 90,
        'Continuous Use': 80,
        'Notification Loops': 75
    }
    
    if not analysis_results:
        return default_indicators
    
    # Try to extract from actual results
    # This would need to be adapted based on your actual result format
    return default_indicators

def create_comparison_chart(user_data_list):
    """Create a comparison chart for multiple users"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Extract data for comparison
    users = [data.get("user_id", f"User {i}") for i, data in enumerate(user_data_list)]
    screen_times = [data.get("duration_minutes", 0) for data in user_data_list]
    app_switches = [data.get("app_switches", 0) for data in user_data_list]
    
    # Screen time comparison
    bars1 = ax1.bar(users, screen_times, color=['red' if t > 360 else 'green' for t in screen_times])
    ax1.axhline(y=360, color='orange', linestyle='--', label='Recommended limit')
    ax1.set_ylabel('Screen Time (minutes)')
    ax1.set_title('Screen Time Comparison')
    ax1.legend()
    
    # Add value labels
    for bar in bars1:
        height = bar.get_height()
        ax1.annotate(f'{int(height)}m',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom')
    
    # App switching comparison
    bars2 = ax2.bar(users, app_switches, color=['red' if s > 50 else 'green' for s in app_switches])
    ax2.axhline(y=50, color='orange', linestyle='--', label='Healthy limit')
    ax2.set_ylabel('App Switches')
    ax2.set_title('App Switching Comparison')
    ax2.legend()
    
    # Add value labels
    for bar in bars2:
        height = bar.get_height()
        ax2.annotate(f'{int(height)}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom')
    
    plt.suptitle('Multi-User Digital Wellness Comparison', fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    output_path = f'outputs/comparison_chart_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    
    return fig

def create_comparative_analysis(user_data_list):
    """Create comparative analysis visualization for multiple users"""
    # Set dark theme for better visual appeal
    plt.style.use('dark_background')
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.patch.set_facecolor('#0a0a0a')
    
    # Extract data for comparison
    users = []
    app_switches = []
    screen_times = []
    wellness_scores = []
    
    for data in user_data_list:
        users.append(data.get("user_id", "User"))
        app_switches.append(data.get("app_switches", 0))
        screen_times.append(data.get("duration_minutes", 0))
        
        # Calculate wellness score based on metrics
        score = 100
        if data.get("duration_minutes", 0) > 360:
            score -= 30
        if data.get("app_switches", 0) > 100:
            score -= 20
        if data.get("duration_minutes", 0) > 480:
            score -= 20
        wellness_scores.append(max(score, 0))
    
    # 1. App Switches Comparison
    ax1 = axes[0, 0]
    colors1 = ['#ff4444' if x > 100 else '#ffaa44' if x > 50 else '#44ff44' for x in app_switches]
    bars1 = ax1.bar(users, app_switches, color=colors1, edgecolor='white', linewidth=2)
    ax1.set_title('App Switching Behavior Comparison', fontsize=14, fontweight='bold', color='white')
    ax1.set_ylabel('Number of App Switches', fontsize=12, color='white')
    ax1.axhline(y=50, color='orange', linestyle='--', alpha=0.5, label='Healthy limit')
    ax1.set_facecolor('#1a1a1a')
    ax1.grid(True, alpha=0.2)
    
    # Add value labels on bars
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}', ha='center', va='bottom', color='white')
    
    # 2. Screen Time Comparison
    ax2 = axes[0, 1]
    colors2 = ['#ff4444' if x > 360 else '#ffaa44' if x > 240 else '#44ff44' for x in screen_times]
    bars2 = ax2.bar(users, screen_times, color=colors2, edgecolor='white', linewidth=2)
    ax2.set_title('Daily Screen Time Comparison', fontsize=14, fontweight='bold', color='white')
    ax2.set_ylabel('Minutes', fontsize=12, color='white')
    ax2.axhline(y=240, color='orange', linestyle='--', alpha=0.5, label='Recommended limit')
    ax2.set_facecolor('#1a1a1a')
    ax2.grid(True, alpha=0.2)
    
    # Add value labels on bars
    for bar in bars2:
        height = bar.get_height()
        hours = int(height) // 60
        minutes = int(height) % 60
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{hours}h {minutes}m', ha='center', va='bottom', color='white', fontsize=10)
    
    # 3. Wellness Score Comparison
    ax3 = axes[1, 0]
    colors3 = ['#44ff44' if x > 70 else '#ffaa44' if x > 40 else '#ff4444' for x in wellness_scores]
    bars3 = ax3.bar(users, wellness_scores, color=colors3, edgecolor='white', linewidth=2)
    ax3.set_title('Digital Wellness Scores', fontsize=14, fontweight='bold', color='white')
    ax3.set_ylabel('Score (0-100)', fontsize=12, color='white')
    ax3.set_ylim(0, 100)
    ax3.set_facecolor('#1a1a1a')
    ax3.grid(True, alpha=0.2)
    
    # Add value labels on bars
    for bar in bars3:
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}', ha='center', va='bottom', color='white')
    
    # 4. Risk Matrix
    ax4 = axes[1, 1]
    scatter = ax4.scatter(app_switches, screen_times, s=300, c=wellness_scores, 
                         cmap='RdYlGn', edgecolors='white', linewidth=2, alpha=0.8)
    ax4.set_xlabel('App Switches', fontsize=12, color='white')
    ax4.set_ylabel('Screen Time (minutes)', fontsize=12, color='white')
    ax4.set_title('User Risk Matrix', fontsize=14, fontweight='bold', color='white')
    ax4.set_facecolor('#1a1a1a')
    ax4.grid(True, alpha=0.2)
    
    # Add user labels
    for i, user in enumerate(users):
        ax4.annotate(user, (app_switches[i], screen_times[i]), 
                    xytext=(5, 5), textcoords='offset points', 
                    color='white', fontsize=10, fontweight='bold')
    
    # Add risk zones
    ax4.axvline(x=100, color='red', linestyle='--', alpha=0.3)
    ax4.axhline(y=360, color='red', linestyle='--', alpha=0.3)
    ax4.text(150, 50, 'High Risk Zone', color='red', alpha=0.5, fontsize=12)
    
    # Add colorbar for wellness scores
    cbar = plt.colorbar(scatter, ax=ax4)
    cbar.set_label('Wellness Score', color='white')
    cbar.ax.yaxis.set_tick_params(color='white')
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')
    
    # Overall title
    fig.suptitle('Digital Wellness Comparative Analysis', fontsize=16, fontweight='bold', color='white')
    
    plt.tight_layout()
    
    # Save the figure
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'outputs/comparative_analysis_{timestamp}.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='#0a0a0a')
    plt.close()
    
    print(f"   📊 Comparative analysis saved to: {filename}")
    
    # Reset style to default
    plt.style.use('seaborn-v0_8-darkgrid')
    
    return fig

# Integration function to be called from main.py
def generate_visual_report(usage_data, analysis_results=None):
    """Generate complete visual report for a user"""
    try:
        # Create main dashboard
        dashboard_fig = create_wellness_dashboard(usage_data, analysis_results)
        
        # Close the figure to free memory
        plt.close(dashboard_fig)
        
        return True
    except Exception as e:
        print(f"Error generating visual report: {e}")
        return False