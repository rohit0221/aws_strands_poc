"""
Portfolio Manager Agent - Specializes in portfolio analysis, investment strategy, and asset allocation.
"""

import os
import sys
from dotenv import load_dotenv

from strands import Agent, tool
# Handle Windows platform incompatibility
if sys.platform == 'win32':
    # On Windows, import only tools that don't require fcntl
    from strands_tools import calculator
    HAS_PYTHON_REPL = False
else:
    # On Unix-like systems, import all tools
    from strands_tools import calculator, python_repl
    HAS_PYTHON_REPL = True

from aws_strands_poc.financial_advisor.models import create_openai_agent
from aws_strands_poc.financial_advisor.tools.portfolio_analysis import portfolio_analysis
from aws_strands_poc.financial_advisor.tools.stock_data import stock_data

# Load environment variables from .env file
load_dotenv()

# System prompt for the Portfolio Manager
PORTFOLIO_MANAGER_PROMPT = """
You are a Portfolio Manager specializing in investment strategy, portfolio construction, 
asset allocation, and risk management.

Your responsibilities include:
1. Analyzing investment portfolios for performance and risk metrics
2. Recommending asset allocations based on risk profiles
3. Providing diversification strategies
4. Explaining investment concepts and strategies
5. Evaluating portfolio performance against benchmarks

When analyzing portfolios:
- Use the portfolio_analysis tool to calculate key portfolio metrics
- Use the stock_data tool to retrieve information about individual securities
- Use the calculator tool for financial calculations
- Use the python_repl tool for more complex analysis when needed

Always consider:
- Diversification across asset classes, sectors, and geographies
- Risk-return tradeoffs appropriate to the investor's goals
- Time horizon and liquidity needs
- Tax efficiency when applicable

Clearly indicate that your analysis is for informational purposes only and does not 
constitute personalized investment advice. Recommend consulting with a licensed financial 
advisor before making investment decisions.
"""

@tool
def portfolio_manager(query: str) -> str:
    """
    Process and respond to portfolio management queries using a specialized portfolio manager agent.
    This tool handles questions about investment strategies, portfolio analysis, asset allocation,
    and risk management.
    
    Args:
        query: The portfolio management query to analyze
    """
    # Get model from environment variable or default to gpt-4o-mini
    model_name = os.environ.get("MODEL", "gpt-4o-mini")
    
    # Create the portfolio manager agent with specialized tools and the specified model
    tools = [calculator, portfolio_analysis, stock_data]
    if HAS_PYTHON_REPL:
        tools.append(python_repl)
    
    portfolio_agent = create_openai_agent(
        system_prompt=PORTFOLIO_MANAGER_PROMPT,
        model=model_name,
        tools=tools,
    )
    
    print("\nRouted to Portfolio Manager")
    
    # Process the query using the agent
    response = portfolio_agent(query)
    
    # Extract the response text
    if hasattr(response, 'message') and response.message:
        if isinstance(response.message, dict) and 'content' in response.message:
            for content in response.message['content']:
                if 'text' in content:
                    return content['text']
        return str(response.message)
    return str(response)
