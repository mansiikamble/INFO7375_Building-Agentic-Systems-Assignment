"""
Digital Wellness Coach Agents - Final Version with Built-in Tools
"""

from crewai import Agent
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from datetime import datetime
from config import AGENT_CONFIG

# Initialize language model
llm = ChatOpenAI(
    model=AGENT_CONFIG["model"],
    temperature=AGENT_CONFIG["temperature"]
)

# BUILT-IN TOOL 1: DateTime Tool
def get_current_datetime(format: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Get current date and time"""
    return datetime.now().strftime(format)

datetime_tool = Tool(
    name="DateTime",
    func=get_current_datetime,
    description="Get current date and time for scheduling and time-based recommendations"
)

# BUILT-IN TOOL 2: Calculator Tool
def calculate(expression: str) -> str:
    """Perform basic math calculations"""
    try:
        # Safe evaluation of mathematical expressions
        allowed_names = {
            "abs": abs,
            "round": round,
            "min": min,
            "max": max,
        }
        # Clean the expression
        expression = expression.replace(',', '')
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        return str(result)
    except Exception as e:
        return f"Calculation error: {str(e)}"

math_tool = Tool(
    name="Calculator",
    func=calculate,
    description="Perform mathematical calculations for metrics and statistics"
)

# BUILT-IN TOOL 3: Data Formatter Tool
def format_data(data: str) -> str:
    """Format data into structured output"""
    formatted = f"""
📊 FORMATTED OUTPUT
{'='*40}
{data}
{'='*40}
Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    return formatted

formatter_tool = Tool(
    name="DataFormatter",
    func=format_data,
    description="Format data into structured, readable output"
)

# Create agents with built-in tools
wellness_orchestrator = Agent(
    role='Digital Wellness Orchestrator',
    goal='Coordinate and optimize digital wellness interventions for users',
    backstory="""You are the master coordinator of a digital wellness system. 
    With years of experience in behavioral psychology and digital health, 
    you understand how to help people build healthier relationships with technology.
    You use the DateTime tool to schedule interventions and the DataFormatter to present plans clearly.""",
    tools=[datetime_tool, formatter_tool],
    llm=llm,
    verbose=True,
    allow_delegation=True
)

screen_analyst = Agent(
    role='Digital Behavior Analyst',
    goal='Analyze screen time patterns and identify problematic usage behaviors',
    backstory="""You are a data scientist specializing in behavioral analytics. 
    You can spot patterns in digital usage that indicate addiction, anxiety, 
    or other wellness issues. You use the Calculator tool to compute usage statistics 
    and wellness scores from the data.""",
    tools=[math_tool],
    llm=llm,
    verbose=True
)

break_suggester = Agent(
    role='Mindfulness and Break Strategist',
    goal='Design personalized break activities that effectively interrupt digital addiction cycles',
    backstory="""You are a mindfulness coach with expertise in attention restoration. 
    You understand that not all breaks are equal - some people need movement, 
    others need stillness. You use the DateTime tool to schedule optimal break times 
    based on usage patterns.""",
    tools=[datetime_tool],
    llm=llm,
    verbose=True
)

sleep_monitor = Agent(
    role='Sleep and Circadian Rhythm Specialist',
    goal='Optimize device usage patterns to improve sleep quality',
    backstory="""You are a sleep scientist who understands the profound impact 
    of blue light and digital stimulation on sleep. You help people establish 
    healthy digital boundaries that protect their rest and recovery. You use the 
    Calculator tool to analyze sleep impact metrics.""",
    tools=[math_tool],
    llm=llm,
    verbose=True
)

sentiment_tracker = Agent(
    role='Emotional Wellness Monitor',
    goal='Detect correlations between social media usage and emotional well-being',
    backstory="""You are an emotional intelligence expert who recognizes how 
    social media affects mood and self-esteem. You can identify when someone's 
    digital consumption is harming their mental health. You use the DataFormatter 
    to present emotional wellness insights clearly.""",
    tools=[formatter_tool],
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

# Performance tracking
class AgentPerformanceTracker:
    def __init__(self):
        self.performance_data = {
            "task_completions": {},
            "error_counts": {},
            "tool_usage": {}
        }
    
    def track_tool_usage(self, agent_role: str, tool_name: str):
        """Track which tools agents use"""
        if agent_role not in self.performance_data["tool_usage"]:
            self.performance_data["tool_usage"][agent_role] = {}
        
        if tool_name not in self.performance_data["tool_usage"][agent_role]:
            self.performance_data["tool_usage"][agent_role][tool_name] = 0
        
        self.performance_data["tool_usage"][agent_role][tool_name] += 1
    
    def get_performance_report(self):
        """Generate performance report"""
        total_tool_uses = 0
        for agent_tools in self.performance_data["tool_usage"].values():
            total_tool_uses += sum(agent_tools.values())
        
        return {
            "status": "Performance tracking active",
            "agents_tracked": len(self.performance_data["task_completions"]),
            "total_tool_uses": total_tool_uses,
            "tool_usage_by_agent": self.performance_data["tool_usage"]
        }

# Initialize global performance tracker
performance_tracker = AgentPerformanceTracker()