"""
Financial Advisor - Main module for the AWS Strands POC.
"""

import os
import logging
import sys
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Check for OpenAI API key
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable must be set")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("financial_advisor")

# Import Strands after setting up environment
from strands import Agent
from strands_tools import calculator
from strands.models.litellm import LiteLLMModel  # Using litellm for OpenAI

# Define a simple system prompt
FINANCIAL_ADVISOR_PROMPT = """
You are a financial advisory assistant that helps users with financial questions.
You can use the calculator tool to perform calculations when needed.
Provide clear, helpful financial advice and calculations.
"""

class FinancialAdvisor:
    """A simple financial advisor agent for the POC."""
    
    def __init__(self, user_id: str = "financial_user"):
        """
        Initialize the Financial Advisor.
        
        Args:
            user_id: Identifier for the user
        """
        self.user_id = user_id
        
        # Create a model using LiteLLM (to work with OpenAI)
        model = LiteLLMModel(
            client_args={"api_key": api_key},
            model_id="openai/gpt-4o-mini",  # Use the OpenAI model
            params={"temperature": 0.3}
        )
        
        # Create a basic agent with calculator tool
        self.agent = Agent(
            system_prompt=FINANCIAL_ADVISOR_PROMPT,
            model=model,  # Explicitly set the model to use OpenAI
            tools=[calculator],
        )
        
        logger.info(f"Financial Advisor initialized with user_id: {user_id}")
        
    def query(self, message: str):
        """
        Process a user query through the financial advisor.
        
        Args:
            message: The user's message or query
            
        Returns:
            The agent's response
        """
        logger.info(f"Processing query: {message[:50]}...")
        
        # Process with the agent
        try:
            response = self.agent(message)
            
            # Extract the response text
            if hasattr(response, 'message') and response.message:
                if isinstance(response.message, dict) and 'content' in response.message:
                    for content in response.message['content']:
                        if 'text' in content:
                            return content['text']
                return str(response.message)
            return str(response)
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return f"Sorry, I encountered an error: {str(e)}"
