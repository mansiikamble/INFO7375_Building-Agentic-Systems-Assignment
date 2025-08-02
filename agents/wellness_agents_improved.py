"""
Digital Wellness Coach Agents - Improved Version
"""

from crewai import Agent
from langchain_openai import ChatOpenAI
from config import AGENT_CONFIG

# Initialize language model
llm = ChatOpenAI(
    model=AGENT_CONFIG["model"],
    temperature=AGENT_CONFIG["temperature"]
)

# Controller Agent
wellness_orchestrator = Agent(
    role='Digital Wellness Orchestrator',
    goal='Coordinate and optimize digital wellness interventions for users',
    backstory="""You are the master coordinator of a digital wellness system. 
    With years of experience in behavioral psychology and digital health, 
    you understand how to help people build healthier relationships with technology.""",
    llm=llm,
    verbose=True,
    allow_delegation=True
)

# Screen Time Analyst Agent
screen_analyst = Agent(
    role='Digital Behavior Analyst',
    goal='Analyze screen time patterns and identify problematic usage behaviors',
    backstory="""You are a data scientist specializing in behavioral analytics. 
    You can spot patterns in digital usage that indicate addiction, anxiety, 
    or other wellness issues.""",
    llm=llm,
    verbose=True
)

# Mindful Break Agent
break_suggester = Agent(
    role='Mindfulness and Break Strategist',
    goal='Design personalized break activities that effectively interrupt digital addiction cycles',
    backstory="""You are a mindfulness coach with expertise in attention restoration. 
    You understand that not all breaks are equal.""",
    llm=llm,
    verbose=True
)

# Sleep Hygiene Agent
sleep_monitor = Agent(
    role='Sleep and Circadian Rhythm Specialist',
    goal='Optimize device usage patterns to improve sleep quality',
    backstory="""You are a sleep scientist who understands the profound impact 
    of blue light and digital stimulation on sleep.""",
    llm=llm,
    verbose=True
)

# Social Media Sentiment Agent
sentiment_tracker = Agent(
    role='Emotional Wellness Monitor',
    goal='Detect correlations between social media usage and emotional well-being',
    backstory="""You are an emotional intelligence expert who recognizes how 
    social media affects mood and self-esteem.""",
    llm=llm,
    verbose=True
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

class AgentPerformanceTracker:
    def __init__(self):
        self.performance_data = {}
    
    def get_performance_report(self):
        return {"status": "Performance tracking active"}

performance_tracker = AgentPerformanceTracker()