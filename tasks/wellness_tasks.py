"""
Tasks for Digital Wellness Coach
"""

from crewai import Task
from agents.wellness_agents_improved import (
    wellness_orchestrator,
    screen_analyst,
    break_suggester,
    sleep_monitor,
    sentiment_tracker
)

# Task 1: Analyze Usage Patterns
analyze_usage_task = Task(
    description="""Analyze the user's device usage data to identify patterns, 
    concerning behaviors, and areas for improvement. 
    
    Input data: {usage_data}
    
    Provide a comprehensive analysis including:
    1. Total screen time and app breakdown
    2. Peak usage times and patterns
    3. Apps causing most disruption
    4. Initial wellness score (0-100)
    5. Key areas of concern
    
    Use the Screen Time Analyzer tool to get detailed metrics.""",
    expected_output="""A detailed JSON report containing usage analysis, 
    identified patterns, wellness score, and specific areas of concern highlighted.""",
    agent=screen_analyst
)

# Task 2: Detect Addictive Patterns
detect_addiction_task = Task(
    description="""Using the Dopamine Cycle Breaker tool, analyze the user's 
    behavior for addictive patterns and problematic usage.
    
    Input data: {usage_data}
    
    Focus on:
    1. Rapid app switching behavior
    2. Doom scrolling patterns
    3. Notification response patterns
    4. Late night usage
    5. Continuous usage without breaks
    
    Determine the severity level and specific interventions needed.""",
    expected_output="""A comprehensive report on addictive patterns detected, 
    severity level, and specific intervention recommendations.""",
    agent=break_suggester
)

# Task 3: Assess Sleep Impact
sleep_assessment_task = Task(
    description="""Evaluate how the user's device usage affects their sleep quality.
    
    Previous analysis: {usage_analysis}
    
    Examine:
    1. Evening and night-time device usage
    2. Blue light exposure patterns
    3. Stimulating content before bed
    4. Sleep disruption indicators
    5. Circadian rhythm impact
    
    Provide specific recommendations for better sleep hygiene.""",
    expected_output="""A sleep impact report with specific recommendations 
    for improving sleep quality through better device usage habits.""",
    agent=sleep_monitor
)

# Task 4: Emotional Impact Analysis
emotional_impact_task = Task(
    description="""Analyze the correlation between social media usage and emotional well-being.
    
    Usage data: {usage_data}
    Mood data: {mood_data}
    
    Look for:
    1. Time spent on social platforms
    2. Posting vs. scrolling behavior
    3. Peak emotional vulnerability times
    4. Comparison and FOMO indicators
    5. Emotional patterns after social media use
    
    Identify specific triggers and suggest healthier engagement patterns.""",
    expected_output="""An emotional wellness report linking social media behaviors 
    to emotional patterns, with specific recommendations for healthier engagement.""",
    agent=sentiment_tracker
)

# Task 5: Create Comprehensive Wellness Plan
create_wellness_plan_task = Task(
    description="""Synthesize all analyses into a comprehensive, personalized digital wellness plan.
    
    All analyses: {all_analyses}
    
    The plan must include:
    1. Executive summary of key issues
    2. Prioritized interventions (immediate, short-term, long-term)
    3. Daily wellness schedule
    4. Specific app limits and boundaries
    5. Break and mindfulness activities
    6. Sleep optimization protocol
    7. Progress tracking metrics
    8. Emergency protocols for high-risk behaviors
    
    Make the plan actionable, realistic, and personalized to the user's specific patterns.""",
    expected_output="""A complete digital wellness plan formatted as a structured 
    document with clear action items, timelines, and success metrics.""",
    agent=wellness_orchestrator
)

def get_all_tasks():
    """Return all configured tasks in execution order"""
    return [
        analyze_usage_task,
        detect_addiction_task,
        sleep_assessment_task,
        emotional_impact_task,
        create_wellness_plan_task
    ]