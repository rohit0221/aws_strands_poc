"""
Financial Advisor - Simple POC using OpenAI SDK directly.
"""

import os
import logging
import json
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("financial_advisor")

# Import OpenAI SDK
from openai import OpenAI

# Define tool schemas for the calculator
CALCULATOR_SCHEMA = {
    "type": "function",
    "function": {
        "name": "calculator",
        "description": "Calculate mathematical expressions",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "The mathematical expression to evaluate"
                }
            },
            "required": ["expression"]
        }
    }
}

# Define a system prompt
FINANCIAL_ADVISOR_PROMPT = """
You are a financial advisory assistant that helps users with financial questions,
investment advice, market analysis, portfolio management, compliance, and tax guidance.

You can use the calculator tool for financial calculations when needed.

Provide clear, helpful financial advice and calculations.
"""

class SimpleCalculator:
    """A simple calculator for financial calculations."""
    
    @staticmethod
    def calculate(expression: str) -> float:
        """
        Safely evaluate a mathematical expression.
        """
        try:
            # Use eval with restricted globals for simple calculations
            # In a production environment, use a safer alternative like sympy
            result = eval(expression, {"__builtins__": {}}, {})
            return result
        except Exception as e:
            logger.error(f"Calculator error: {str(e)}")
            return f"Error: {str(e)}"

class FinancialAdvisor:
    """A simple financial advisor agent using OpenAI directly."""
    
    def __init__(self, user_id: str = "financial_user", model: str = "gpt-4o-mini"):
        """
        Initialize the Financial Advisor.
        
        Args:
            user_id: Identifier for the user
            model: OpenAI model name
        """
        self.user_id = user_id
        self.model = model
        
        # Check for OpenAI API key
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable must be set")
        
        # Initialize OpenAI client
        self.client = OpenAI(api_key=api_key)
        
        # Initialize conversation history
        self.conversation_history = [
            {"role": "system", "content": FINANCIAL_ADVISOR_PROMPT}
        ]
        
        logger.info(f"Financial Advisor initialized with user_id: {user_id} and model: {model}")
    
    def _run_tool(self, tool_calls: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Execute tool calls made by the model.
        
        Args:
            tool_calls: List of tool calls from OpenAI
            
        Returns:
            List of tool results to send back to OpenAI
        """
        tool_results = []
        
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            if function_name == "calculator":
                expression = function_args.get("expression", "")
                result = SimpleCalculator.calculate(expression)
                tool_results.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "content": str(result)
                })
            else:
                tool_results.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "content": f"Tool {function_name} not found"
                })
        
        return tool_results
        
    def query(self, message: str) -> str:
        """
        Process a user query through the financial advisor.
        
        Args:
            message: The user's message or query
            
        Returns:
            The agent's response
        """
        logger.info(f"Processing query: {message[:50]}...")
        
        # Add user message to conversation history
        self.conversation_history.append({"role": "user", "content": message})
        
        # Process with OpenAI
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation_history,
                tools=[CALCULATOR_SCHEMA],
                tool_choice="auto"
            )
            
            assistant_message = response.choices[0].message
            self.conversation_history.append(assistant_message)
            
            # Check if the model wants to use a tool
            if assistant_message.tool_calls:
                logger.info(f"Model requested to use tools: {assistant_message.tool_calls}")
                
                # Execute the tool calls
                tool_results = self._run_tool(assistant_message.tool_calls)
                
                # Add tool results to conversation history
                self.conversation_history.extend(tool_results)
                
                # Call the model again with the tool results
                second_response = self.client.chat.completions.create(
                    model=self.model,
                    messages=self.conversation_history,
                    tools=[CALCULATOR_SCHEMA],
                    tool_choice="auto"
                )
                
                final_message = second_response.choices[0].message
                self.conversation_history.append(final_message)
                return final_message.content
            
            return assistant_message.content
            
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return f"Sorry, I encountered an error: {str(e)}"
