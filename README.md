# Financial Advisor Assistant POC

A Proof of Concept application using AWS Strands to implement a multi-agent architecture for financial advisory services.

## Overview

This POC demonstrates how to build a sophisticated agentic application using the AWS Strands framework. The application features:

- A multi-agent architecture with specialized financial experts
- Dynamic query routing based on domain expertise
- Custom tools for financial calculations and analysis
- Memory persistence for personalized responses
- Direct OpenAI GPT-4o-mini integration for high-quality responses

## Architecture

The Financial Advisor Assistant uses a central orchestrator that routes queries to specialized agents:

- **Market Analyst**: Handles market trends, stock analysis, and economic outlook
- **Portfolio Manager**: Manages investment strategy and portfolio optimization
- **Compliance Officer**: Provides regulatory and legal guidance
- **Tax Specialist**: Offers tax planning and calculations

Each specialist has access to dedicated tools that enhance their capabilities in their domain of expertise.

## Prerequisites

- Python 3.10+
- OpenAI API key with access to GPT-4o-mini
- Poetry for dependency management

## Installation

1. Make sure you have Poetry installed:
   ```
   pip install poetry
   ```

2. Install the required dependencies:
   ```
   poetry install
   poetry add openai python-dotenv
   ```

3. Configure your environment variables using a `.env` file:
   ```
   OPENAI_API_KEY=your-openai-api-key
   MODEL=gpt-4o-mini  # or any other OpenAI model you want to use
   ```

## Usage

Run the main application:

```
poetry run python src/main.py
```

### Command Line Options

- `--user_id`: Custom identifier for memory persistence (default: "financial_user")
- `--api_key`: OpenAI API key (if not set as environment variable)
- `--model`: OpenAI model name (defaults to MODEL environment variable or gpt-4o-mini)
- `--init_memory`: Initialize user memory with default preferences

Example:
```
poetry run python src/main.py --user_id client123 --api_key sk-... --init_memory
```

## Example Queries

Try asking the Financial Advisor Assistant questions like:

### Market Analysis
- "What are the current trends in tech stocks?"
- "Can you analyze the performance of AAPL over the last month?"
- "What's the outlook for the banking sector?"

### Portfolio Management
- "Can you analyze a portfolio with 30% AAPL, 25% MSFT, 25% GOOGL, and 20% AMZN?"
- "What's an appropriate asset allocation for a conservative investor nearing retirement?"
- "How can I optimize my portfolio for higher returns while maintaining moderate risk?"

### Regulatory Compliance
- "What are the key SEC regulations for individual investors?"
- "Can you explain the rules around insider trading?"
- "What compliance considerations are there for retirement account withdrawals?"

### Tax Planning
- "What would be my estimated taxes on an income of $150,000 with $20,000 in deductions?"
- "How are capital gains taxed compared to regular income?"
- "What tax strategies can help minimize my investment taxes?"

## Project Structure

```
src/
└── aws_strands_poc/
    ├── financial_advisor/
    │   ├── models/
    │   │   └── openai_agent.py      # OpenAI integration helper
    │   ├── specialists/
    │   │   ├── market_analyst.py      # Market analysis specialist
    │   │   ├── portfolio_manager.py   # Portfolio management specialist
    │   │   ├── compliance_officer.py  # Regulatory compliance specialist
    │   │   └── tax_specialist.py      # Tax planning specialist
    │   ├── tools/
    │   │   ├── memory/
    │   │   │   └── simple_memory.py    # Custom memory implementation
    │   │   ├── stock_data.py          # Tool for retrieving stock data
    │   │   ├── portfolio_analysis.py  # Tool for portfolio metrics
    │   │   └── tax_calculator.py      # Tool for tax calculations
    │   └── advisor.py                 # Main orchestrator agent
    └── main.py                        # Application entry point
```

## How It Works

1. The user submits a financial query through the CLI
2. The main orchestrator agent analyzes the query to determine which specialist(s) should handle it
3. The appropriate specialist agent processes the query using its specialized knowledge and tools
4. Results are returned to the user with a comprehensive answer

All agents use OpenAI's GPT-4o-mini model through our OpenAI integration helper that properly connects with the Strands framework.

## Future Enhancements

- Web interface for easier interaction
- Integration with real financial data APIs
- Additional specialists for estate planning, insurance, etc.
- Performance monitoring and evaluation framework
- Deployment to AWS Lambda or Fargate for production scaling

## Acknowledgements

This project uses the [AWS Strands](https://github.com/strands-agents/sdk-python) framework for building agentic applications.
