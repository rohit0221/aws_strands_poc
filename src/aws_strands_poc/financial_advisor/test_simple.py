"""
Simple test script for the financial advisor.
"""

import os
import logging
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("financial_advisor_app")

# Enable verbose logging for Strands
logging.getLogger("strands").setLevel(logging.DEBUG)

# Import our simple advisor
from aws_strands_poc.financial_advisor.simple import FinancialAdvisor

def main():
    """Run a simple version of the Financial Advisor application."""
    print("\n" + "="*80)
    print("💼 Simple Financial Advisor Test 💼")
    print("="*80)
    
    # Print environment info
    print(f"\nPlatform: {sys.platform}")
    print(f"OpenAI API Key present: {bool(os.environ.get('OPENAI_API_KEY'))}")
    print(f"MODEL environment variable: {os.environ.get('MODEL', 'Not set, using default')}")
    
    # Create the advisor
    try:
        advisor = FinancialAdvisor()
        
        # Test it with a simple question
        response = advisor.query("What is compound interest?")
        print(f"\nResponse: {response}\n")
        
        # Test with a calculation
        response = advisor.query("If I invest $1000 at 5% interest compounded annually, how much will I have after 10 years?")
        print(f"\nResponse: {response}\n")
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
