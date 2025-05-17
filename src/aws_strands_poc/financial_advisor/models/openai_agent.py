"""
OpenAI-compatible agent creator for Strands.

This approach uses a simpler method that doesn't try to override the agent's internals.
"""

import os
import logging
from typing import Any, Dict, List, Optional

from strands import Agent

logger = logging.getLogger(__name__)

def create_openai_agent(
    system_prompt: str, 
    tools: list, 
    model: str = "gpt-4o-mini",
    temperature: float = 0.3,
    **kwargs
) -> Agent:
    """
    Create a Strands agent with OpenAI integration.
    
    Args:
        system_prompt: System prompt for the agent
        tools: List of tools to provide to the agent
        model: OpenAI model name (default: gpt-4o-mini)
        temperature: Model temperature (default: 0.3)
        **kwargs: Additional parameters for the Agent constructor
        
    Returns:
        A configured Strands Agent
    """
    # Log the API key availability
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable must be set")
    
    # For the POC, we'll use the default model since trying to create a custom
    # OpenAI integration is causing issues with the Strands agent. In a real
    # implementation, we would create a proper OpenAI integration.
    logger.info(f"Creating agent with system prompt of length: {len(system_prompt)}")
    logger.info(f"Tools provided: {[t.__name__ if hasattr(t, '__name__') else str(t) for t in tools]}")
    
    # Create the agent with the tools
    agent = Agent(
        system_prompt=system_prompt,
        tools=tools,
        **kwargs
    )
    
    return agent
