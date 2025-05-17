"""
Direct OpenAI model implementation for Strands.

This custom model provider uses the OpenAI SDK directly without LiteLLM.
"""

import json
import os
from typing import Any, Dict, List, Optional, Tuple, Union

import openai
from openai import OpenAI
from strands.types.models import Model
from strands.types.messages import Message, Messages

class OpenAIDirectModel(Model):
    """
    A model provider for OpenAI using the direct OpenAI API.
    
    This implementation directly uses the OpenAI Python SDK without any intermediary
    like LiteLLM. It implements the Strands Model interface.
    """
    
    def __init__(
        self,
        model: str = "gpt-4o-mini",
        api_key: Optional[str] = None,
        temperature: float = 0.3,
        max_tokens: int = 1000,
        **kwargs: Any,
    ) -> None:
        """
        Initialize the OpenAIDirectModel.
        
        Args:
            model: OpenAI model name
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
            temperature: Model temperature (0.0 to 1.0)
            max_tokens: Maximum number of tokens to generate
            **kwargs: Additional parameters for OpenAI API
        """
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.kwargs = kwargs
        
        # Set API key from argument or environment variable
        if api_key is not None:
            openai.api_key = api_key
        elif os.environ.get("OPENAI_API_KEY") is not None:
            # Use environment variable if available
            pass
        else:
            raise ValueError(
                "OpenAI API key must be provided either through the api_key parameter "
                "or the OPENAI_API_KEY environment variable."
            )
        
        # Initialize OpenAI client
        self.client = OpenAI(api_key=api_key or os.environ.get("OPENAI_API_KEY"))
    
    def generate(
        self, messages: Messages, stop: Optional[List[str]] = None, **kwargs: Any
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Generate text from the OpenAI model.
        
        Args:
            messages: List of message dictionaries
            stop: Optional list of stop sequences
            **kwargs: Additional parameters for the OpenAI API
        
        Returns:
            Tuple containing the generated text and metadata
        """
        # Convert Strands message format to OpenAI format
        openai_messages = self._convert_messages_to_openai_format(messages)
        
        # Merge instance kwargs with method kwargs
        merged_kwargs = {**self.kwargs, **kwargs}
        if stop:
            merged_kwargs["stop"] = stop
        
        try:
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=openai_messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                **merged_kwargs
            )
            
            # Extract text content from response
            content = response.choices[0].message.content or ""
            
            # Return text and metadata
            return content, {"model": self.model, "response": response}
        
        except Exception as e:
            # Handle potential API errors
            error_msg = f"OpenAI API error: {str(e)}"
            print(f"Error generating text: {error_msg}")
            return error_msg, {"error": str(e)}
    
    def _convert_messages_to_openai_format(self, messages: Messages) -> List[Dict[str, Any]]:
        """
        Convert Strands message format to OpenAI format.
        
        Args:
            messages: List of messages in Strands format
        
        Returns:
            List of messages in OpenAI format
        """
        openai_messages = []
        
        for message in messages:
            # Handle system message
            if message.get("role") == "system":
                openai_messages.append({
                    "role": "system", 
                    "content": message.get("content", "")
                })
                continue
            
            # Handle user and assistant messages
            role = message.get("role", "user")
            content = []
            
            # Handle string content or list content
            if isinstance(message.get("content"), str):
                content_value = message.get("content", "")
                if content_value:
                    openai_messages.append({"role": role, "content": content_value})
                continue
            
            # Handle complex content with text and tool calls
            message_content = []
            has_tool_calls = False
            
            for item in message.get("content", []):
                if "text" in item:
                    message_content.append({"type": "text", "text": item["text"]})
                elif "toolUse" in item:
                    has_tool_calls = True
                    tool_call = item["toolUse"]
                    tool_calls = {
                        "id": tool_call.get("toolUseId", ""),
                        "type": "function",
                        "function": {
                            "name": tool_call.get("name", ""),
                            "arguments": json.dumps(tool_call.get("input", {}))
                        }
                    }
                    message_content.append({"type": "tool_call", "tool_call": tool_calls})
                elif "toolResult" in item:
                    # For tool results in user messages
                    tool_result = item["toolResult"]
                    result_text = ""
                    for content_item in tool_result.get("content", []):
                        if "text" in content_item:
                            result_text = content_item["text"]
                    
                    openai_messages.append({
                        "role": "tool",
                        "tool_call_id": tool_result.get("toolUseId", ""),
                        "content": result_text
                    })
                    continue
            
            # Add message with content if there's any content
            if message_content:
                if has_tool_calls:
                    # For messages with tool calls
                    msg = {"role": role, "content": "", "tool_calls": []}
                    for item in message_content:
                        if item.get("type") == "text":
                            msg["content"] = item.get("text", "")
                        elif item.get("type") == "tool_call":
                            msg["tool_calls"].append(item.get("tool_call", {}))
                    openai_messages.append(msg)
                else:
                    # For regular text messages with complex content
                    text_content = ""
                    for item in message_content:
                        if item.get("type") == "text":
                            text_content += item.get("text", "")
                    if text_content:
                        openai_messages.append({"role": role, "content": text_content})
        
        return openai_messages
