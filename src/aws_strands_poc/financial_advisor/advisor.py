"""
Financial Advisor - Main orchestrator agent that routes queries to specialized agents.
"""

import logging
import os
import sys
from typing import Optional
from dotenv import load_dotenv

from strands import Agent
from aws_strands_poc.financial_advisor.models import create_openai_agent
from aws_strands_poc.financial_advisor.tools import memory_tool

# Load environment variables from .env file
load_dotenv()

from aws_strands_poc.financial_advisor.specialists import (
    market_analyst,
    portfolio_manager,
    compliance_officer,
    tax_specialist
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("financial_advisor")

# Define the system prompt for the Financial Advisor orchestrator
FINANCIAL_ADVISOR_PROMPT = """
You are a financial advisory assistant that helps users with financial questions, 
investment advice, market analysis, portfolio management, compliance, and tax guidance.

Your role is to understand financial queries and route them to the appropriate specialist:

1. MARKET ANALYST: For questions about:
   - Market trends and stock performance
   - Economic indicators and forecasts
   - Industry or sector analysis
   - Company-specific financial analysis
   - Financial news interpretation

2. PORTFOLIO MANAGER: For questions about:
   - Investment strategy and portfolio construction
   - Asset allocation and diversification
   - Risk management and portfolio optimization
   - Performance analysis and benchmarking
   - Retirement planning and investment vehicles

3. COMPLIANCE OFFICER: For questions about:
   - Financial regulations and legal requirements
   - Regulatory frameworks (SEC, FINRA, Basel, etc.)
   - Compliance best practices and risk management
   - Legal implications of financial decisions
   - Industry standards and ethical considerations

4. TAX SPECIALIST: For questions about:
   - Tax planning and optimization strategies
   - Tax implications of financial decisions
   - Tax deductions, credits, and exemptions
   - Income and capital gains tax considerations
   - Tax filing requirements and calculations

For complex queries that span multiple domains, you can coordinate responses from 
multiple specialists. Always maintain a professional tone, acknowledge financial 
regulations, and emphasize when information is general advice rather than specific 
financial recommendations.

When appropriate, use the memory_tool to store important user context or 
preferences, and retrieve this information to provide personalized responses.
"""

class FinancialAdvisor:
    """Financial Advisor orchestrator class that routes queries to specialized agents."""
    
    def __init__(self, user_id: str = "financial_user", model: Optional[str] = None):
        """
        Initialize the Financial Advisor.
        
        Args:
            user_id: Identifier for the user (used for memory persistence)
            model: OpenAI model name (if not provided, uses MODEL env var or defaults to gpt-4o-mini)
        """
        self.user_id = user_id
        
        # Get model from env var if not provided
        if not model:
            model = os.environ.get("MODEL", "gpt-4o-mini")
        
        # Create the agent using the OpenAI agent creator
        try:
            self.agent = create_openai_agent(
                system_prompt=FINANCIAL_ADVISOR_PROMPT,
                model=model,
                tools=[
                    market_analyst,
                    portfolio_manager,
                    compliance_officer,
                    tax_specialist,
                    memory_tool,
                ]
            )
            
            logger.info(f"Financial Advisor initialized with user_id: {user_id}")
        except Exception as e:
            logger.error(f"Error creating agent: {str(e)}")
            raise
        
    def initialize_memory(self):
        """Initialize user memory with default preferences."""
        try:
            # Store default user preferences in memory
            self.agent.tool.memory_tool(
                action="store",
                content="User has moderate risk tolerance and prefers long-term investment strategies.",
                user_id=self.user_id
            )
            logger.info(f"Initialized memory for user: {self.user_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize memory: {str(e)}")
            return False
            
    def query(self, message: str):
        """
        Process a user query through the financial advisor.
        
        Args:
            message: The user's message or query
            
        Returns:
            The agent's response
        """
        logger.info(f"Processing query: {message[:50]}...")
        
        # Add user_id to context for memory operations
        formatted_message = f"[User ID: {self.user_id}] {message}"
        
        # Process with the agent
        response = self.agent(formatted_message)
        
        # Extract the response text
        if hasattr(response, 'message') and response.message:
            if isinstance(response.message, dict) and 'content' in response.message:
                for content in response.message['content']:
                    if 'text' in content:
                        return content['text']
            return str(response.message)
        return str(response)
