"""
Tax Specialist Agent - Specializes in tax planning, calculations, and regulations.
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
from aws_strands_poc.financial_advisor.tools.tax_calculator import tax_calculator

# Load environment variables from .env file
load_dotenv()

# System prompt for the Tax Specialist
TAX_SPECIALIST_PROMPT = """
You are a Tax Specialist focusing on tax planning, calculations, and regulatory guidance
for individuals and businesses.

Your responsibilities include:
1. Explaining tax concepts, regulations, and filing requirements
2. Calculating estimated taxes based on income and deductions
3. Providing general tax planning strategies
4. Addressing questions about tax deductions, credits, and exemptions
5. Helping users understand tax implications of financial decisions

When addressing tax questions:
- Use the tax_calculator tool for estimating taxes
- Use the calculator tool for basic calculations
- Use the python_repl tool for more complex tax calculations
- Provide clear explanations of tax concepts and calculations

Always include the following disclaimers:
1. Your guidance is for informational purposes only and does not constitute tax advice
2. Tax laws vary by jurisdiction and change over time
3. Users should consult with qualified tax professionals for specific tax advice
4. Tax calculations are estimates and may not reflect exact tax liabilities

Be thorough, educational, and balanced in your responses, focusing on helping users
understand tax concepts and implications rather than making subjective judgments.
"""

@tool
def tax_specialist(query: str) -> str:
    """
    Process and respond to tax-related queries using a specialized tax specialist agent.
    This tool handles questions about tax planning, calculations, and regulations.
    
    Args:
        query: The tax-related query to analyze
    """
    # Get model from environment variable or default to gpt-4o-mini
    model_name = os.environ.get("MODEL", "gpt-4o-mini")
    
    # Create the tax specialist agent with specialized tools and the specified model
    tools = [calculator, tax_calculator]
    if HAS_PYTHON_REPL:
        tools.append(python_repl)
    
    tax_agent = create_openai_agent(
        system_prompt=TAX_SPECIALIST_PROMPT,
        model=model_name,
        tools=tools,
    )
    
    print("\nRouted to Tax Specialist")
    
    # Process the query using the agent
    response = tax_agent(query)
    
    # Extract the response text
    if hasattr(response, 'message') and response.message:
        if isinstance(response.message, dict) and 'content' in response.message:
            for content in response.message['content']:
                if 'text' in content:
                    return content['text']
        return str(response.message)
    return str(response)
