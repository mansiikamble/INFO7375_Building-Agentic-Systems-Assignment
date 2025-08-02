"""
Digital Wellness Coach Agents
"""

from crewai import Agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from config import AGENT_CONFIG
import json

# Import our custom tool classes
from tools.dopamine_cycle_breaker import dopamine_cycle_breaker
from tools.screen_time_analyzer import screen_time_analyzer

# Initialize language model
llm = ChatOpenAI(
    model=AGENT_CONFIG["model"],
    temperature=AGENT_CONFIG["temperature"]
)

# Create LangChain compatible tools
@tool
def analyze_screen_time(device_data: str) -> str:
    """Analyze screen time data to get usage insights and wellness score"""
    return screen_time_analyzer.run(device_data)

@tool
def check_dopamine_patterns(usage_data: str) -> str:
    """Detect addictive behavior patterns and suggest interventions"""
    return dopamine_cycle_breaker.run(usage_data)

# Controller Agent - Orchestrates the entire system
wellness_orchestrator = Agent(
    role='Digital Wellness Orchestrator',
    goal='Coordinate and optimize digital wellness interventions for users',
    backstory="""You are the master coordinator of a digital wellness system. 
    With years of experience in behavioral psychology and digital health, 
    you understand how to help people build healthier relationships with technology. 
    You delegate tasks to specialized agents and ensure interventions are timely, 
    personalized, and effective. You synthesize insights from all other agents 
    to create comprehensive wellness plans.""",
    llm=llm,
    verbose=True,
    allow_delegation=True,
    max_iter=AGENT_CONFIG["max_iterations"]
)

# Screen Time Analyst Agent
screen_analyst = Agent(
    role='Digital Behavior Analyst',
    goal='Analyze screen time patterns and identify problematic usage behaviors',
    backstory="""You are a data scientist specializing in behavioral analytics. 
    You can spot patterns in digital usage that indicate addiction, anxiety, 
    or other wellness issues. Your insights help people understand their 
    relationship with their devices. You use tools to provide detailed usage 
    breakdowns and identify concerning patterns.""",
    tools=[analyze_screen_time],
    llm=llm,
    verbose=True,
    allow_delegation=False
)

# Mindful Break Agent
break_suggester = Agent(
    role='Mindfulness and Break Strategist',
    goal='Design personalized break activities that effectively interrupt digital addiction cycles',
    backstory="""You are a mindfulness coach with expertise in attention restoration. 
    You understand that not all breaks are equal - some people need movement, 
    others need stillness. You craft interventions that actually work for each individual's 
    psychology and circumstances. You use tools to identify when and how to intervene.""",
    tools=[check_dopamine_patterns],
    llm=llm,
    verbose=True,
    allow_delegation=False
)

# Sleep Hygiene Agent
sleep_monitor = Agent(
    role='Sleep and Circadian Rhythm Specialist',
    goal='Optimize device usage patterns to improve sleep quality',
    backstory="""You are a sleep scientist who understands the profound impact 
    of blue light and digital stimulation on sleep. You help people establish 
    healthy digital boundaries that protect their rest and recovery. You analyze 
    usage patterns to identify sleep-disrupting behaviors and recommend 
    evidence-based interventions.""",
    tools=[analyze_screen_time],
    llm=llm,
    verbose=True,
    allow_delegation=False
)

# Social Media Sentiment Agent
sentiment_tracker = Agent(
    role='Emotional Wellness Monitor',
    goal='Detect correlations between social media usage and emotional well-being',
    backstory="""You are an emotional intelligence expert who recognizes how 
    social media affects mood and self-esteem. You can identify when someone's 
    digital consumption is harming their mental health and suggest healthier 
    engagement patterns. You look for signs of comparison, FOMO, and other 
    negative emotional patterns.""",
    llm=llm,
    verbose=True,
    allow_delegation=False
)

def get_all_agents():
    """Return all configured agents"""
    return [
        wellness_orchestrator,
        screen_analyst,
        break_suggester,
        sleep_monitor,
        sentiment_tracker
    ]