# OpenAI Integration for Strands

This module provides a simple integration between the OpenAI SDK and the Strands framework.

## Overview

Instead of implementing a full custom `Model` for Strands, which requires detailed knowledge of the framework's internal message formats, this module takes a simpler approach:

1. It creates a standard Strands `Agent` with all the required tools and system prompt
2. It overrides the agent's internal model's `generate` method with a custom implementation
3. This custom implementation converts Strands messages to OpenAI format and calls the OpenAI API directly

## Usage

```python
from aws_strands_poc.financial_advisor.models import create_openai_agent

# Create an agent with direct OpenAI integration
agent = create_openai_agent(
    system_prompt="You are a helpful assistant",
    model="gpt-4o-mini",  # or any other OpenAI model
    tools=[my_tool1, my_tool2],
    temperature=0.3  # optional
)

# Use the agent just like any other Strands agent
response = agent("Hello, can you help me with something?")
```

## Benefits

- **Simplicity**: No need to implement complex message conversion logic
- **Compatibility**: Works with the standard Strands `Agent` interface
- **Flexibility**: Can be configured with different OpenAI models and parameters
- **Direct Integration**: Uses the official OpenAI SDK directly

## Limitations

- The implementation is simplified and may not support all Strands features
- Complex tool interactions might not be fully supported
- This is a pragmatic approach for a POC, not a production-ready solution
