"""
Market Analyst Agent - Specializes in market trends, stock analysis, and economic outlook.
"""

import os
import sys
from dotenv import load_dotenv

from strands import Agent, tool
# Handle Windows platform incompatibility
if sys.platform == 'win32':
    # On Windows, import only tools that don't require fcntl
    from strands_tools import calculator, http_request
    HAS_PYTHON_REPL = False
else:
    # On Unix-like systems, import all tools
    from strands_tools import calculator, python_repl, http_request
    HAS_PYTHON_REPL = True

from aws_strands_poc.financial_advisor.tools.stock_data import stock_data
from aws_strands_poc.financial_advisor.models import create_openai_agent

# Load environment variables from .env file
load_dotenv()

# System prompt for the Market Analyst
MARKET_ANALYST_PROMPT = """
You are a Market Analyst specializing in financial markets, stock analysis, economic trends, and news.

Your responsibilities include:
1. Analyzing market trends and stock performance
2. Interpreting economic data and indicators
3. Summarizing relevant financial news
4. Explaining market movements and their implications
5. Providing insights on sectors, industries, and specific companies

When analyzing stocks or markets:
- Use the stock_data tool to fetch price data
- Use the calculator tool for financial calculations
- Use the python_repl tool for more complex analysis when needed
- Use the http_request tool for accessing external financial data

Always provide balanced analysis, mentioning both positive and negative factors.
Clearly indicate when you're providing an opinion versus factual analysis.
Use data to support your conclusions whenever possible.
Always remind users that past performance does not guarantee future results.
"""

@tool
def market_analyst(query: str) -> str:
    """
    Process and respond to market analysis queries using a specialized market analyst agent.
    This tool handles questions about market trends, stock performance, economic outlook,
    and financial news.
    
    Args:
        query: The financial market query to analyze
    """
    # Get model from environment variable or default to gpt-4o-mini
    model_name = os.environ.get("MODEL", "gpt-4o-mini")
    
    # Create the market analyst agent with specialized tools and the specified model
    tools = [calculator, http_request, stock_data]
    if HAS_PYTHON_REPL:
        tools.append(python_repl)
    
    market_agent = create_openai_agent(
        system_prompt=MARKET_ANALYST_PROMPT,
        model=model_name,
        tools=tools,
    )
    
    print("\nRouted to Market Analyst")
    
    # Process the query using the agent
    response = market_agent(query)
    
    # Extract the response text
    if hasattr(response, 'message') and response.message:
        if isinstance(response.message, dict) and 'content' in response.message:
            for content in response.message['content']:
                if 'text' in content:
                    return content['text']
        return str(response.message)
    return str(response)
