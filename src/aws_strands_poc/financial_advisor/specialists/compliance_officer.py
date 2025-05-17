"""
Compliance Officer Agent - Specializes in regulatory compliance, legal requirements, and best practices.
"""

import os
from dotenv import load_dotenv

from strands import Agent, tool
from strands_tools import calculator, http_request
from aws_strands_poc.financial_advisor.models import create_openai_agent

# Load environment variables from .env file
load_dotenv()

# System prompt for the Compliance Officer
COMPLIANCE_OFFICER_PROMPT = """
You are a Compliance Officer specializing in financial regulations, legal requirements,
and industry best practices.

Your responsibilities include:
1. Explaining financial regulations and compliance requirements
2. Providing guidance on regulatory frameworks like SEC rules, FINRA, Basel, etc.
3. Advising on compliance best practices for financial activities
4. Highlighting potential compliance risks in financial scenarios
5. Explaining legal implications of financial decisions

When addressing compliance questions:
- Provide clear explanations of relevant regulations
- Cite specific rules and guidelines when applicable
- Highlight regulatory considerations and potential risks
- Recommend compliance best practices
- Use the http_request tool to access current regulatory information if needed

Always include the following disclaimers:
1. Your guidance is for informational purposes only and does not constitute legal advice
2. Financial regulations vary by jurisdiction and change over time
3. Users should consult with legal professionals for specific compliance questions
4. Always verify information with official regulatory sources

Be clear, precise, and balanced in your responses, focusing on explaining regulatory 
requirements rather than making subjective judgments about them.
"""

@tool
def compliance_officer(query: str) -> str:
    """
    Process and respond to compliance and regulatory queries using a specialized compliance officer agent.
    This tool handles questions about financial regulations, legal requirements, and compliance best practices.
    
    Args:
        query: The compliance or regulatory query to analyze
    """
    # Get model from environment variable or default to gpt-4o-mini
    model_name = os.environ.get("MODEL", "gpt-4o-mini")
    
    # Create the compliance officer agent with specialized tools and the specified model
    compliance_agent = create_openai_agent(
        system_prompt=COMPLIANCE_OFFICER_PROMPT,
        model=model_name,
        tools=[calculator, http_request],
    )
    
    print("\nRouted to Compliance Officer")
    
    # Process the query using the agent
    response = compliance_agent(query)
    
    # Extract the response text
    if hasattr(response, 'message') and response.message:
        if isinstance(response.message, dict) and 'content' in response.message:
            for content in response.message['content']:
                if 'text' in content:
                    return content['text']
        return str(response.message)
    return str(response)
