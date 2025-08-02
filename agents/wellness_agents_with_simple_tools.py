"""
Digital Wellness Coach Agents - With Simple Built-in Tools
"""

from crewai import Agent
from langchain_openai import ChatOpenAI
from config import AGENT_CONFIG

# Initialize language model
llm = ChatOpenAI(
    model=AGENT_CONFIG["model"],
    temperature=AGENT_CONFIG["temperature"]
)

# Simple built-in tool descriptions that agents can reference
BUILT_IN_TOOLS = {
    "web_search": "Search for digital wellness tips and research",
    "data_processor": "Process and analyze usage statistics",
    "formatter": "Format output into structured reports"
}

# Controller Agent
wellness_orchestrator = Agent(
    role='Digital Wellness Orchestrator',
    goal='Coordinate and optimize digital wellness interventions for users',
    backstory="""You are the master coordinator of a digital wellness system. 
    With years of experience in behavioral psychology and digital health, 
    you understand how to help people build healthier relationships with technology.
    You utilize the formatter tool to structure comprehensive wellness plans,
    reference web_search to find latest digital wellness research, and use 
    data_processor to analyze user metrics for informed decision-making.""",
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
    or other wellness issues. You leverage the data_processor tool to compute
    complex usage statistics and identify concerning behavioral patterns.""",
    llm=llm,
    verbose=True
)

# Mindful Break Agent
break_suggester = Agent(
    role='Mindfulness and Break Strategist',
    goal='Design personalized break activities that effectively interrupt digital addiction cycles',
    backstory="""You are a mindfulness coach with expertise in attention restoration. 
    You understand that not all breaks are equal. You use the web_search tool to find
    evidence-based mindfulness techniques and the formatter tool to create structured
    break schedules tailored to individual needs.""",
    llm=llm,
    verbose=True
)

# Sleep Hygiene Agent
sleep_monitor = Agent(
    role='Sleep and Circadian Rhythm Specialist',
    goal='Optimize device usage patterns to improve sleep quality',
    backstory="""You are a sleep scientist who understands the profound impact 
    of blue light and digital stimulation on sleep. You utilize the data_processor
    tool to analyze evening usage patterns and the web_search tool to stay updated
    with latest sleep research findings.""",
    llm=llm,
    verbose=True
)

# Social Media Sentiment Agent
sentiment_tracker = Agent(
    role='Emotional Wellness Monitor',
    goal='Detect correlations between social media usage and emotional well-being',
    backstory="""You are an emotional intelligence expert who recognizes how 
    social media affects mood and self-esteem. You employ the data_processor tool
    to identify emotional patterns and the formatter tool to present insights in
    an empathetic, actionable manner.""",
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

# Performance tracking (same as in wellness_agents_improved.py)
class AgentPerformanceTracker:
    def __init__(self):
        self.performance_data = {}
    
    def get_performance_report(self):
        return {"status": "Performance tracking active"}

performance_tracker = AgentPerformanceTracker()