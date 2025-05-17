"""
Main application for the Financial Advisor Assistant using OpenAI directly.

This script initializes and runs the Financial Advisor application,
which uses OpenAI for financial guidance without relying on Strands.
"""

import os
import logging
import argparse
import sys
from dotenv import load_dotenv

# Load environment variables from .env file first thing
load_dotenv()

from aws_strands_poc.financial_advisor.simple_openai import FinancialAdvisor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("financial_advisor_app")

def main():
    """Run the Financial Advisor application."""
    parser = argparse.ArgumentParser(description="Financial Advisor Assistant")
    parser.add_argument(
        "--user_id", 
        default="financial_user",
        help="User ID for memory persistence"
    )
    parser.add_argument(
        "--api_key", 
        default=None,
        help="OpenAI API key (defaults to OPENAI_API_KEY environment variable)"
    )
    parser.add_argument(
        "--model", 
        default=None,
        help="OpenAI model name (defaults to MODEL environment variable or gpt-4o-mini)"
    )
    
    args = parser.parse_args()
    
    # Check for OpenAI API key
    if not args.api_key and not os.environ.get("OPENAI_API_KEY"):
        logger.error(
            "OpenAI API key not provided. Please set the OPENAI_API_KEY environment variable "
            "or provide it using the --api_key argument."
        )
        return
    
    # If API key is provided via command line, set it in the environment
    if args.api_key:
        os.environ["OPENAI_API_KEY"] = args.api_key
        logger.info("Using API key provided via command line argument")
    
    # If API key is provided via command line but no .env file exists, create one
    if args.api_key and not os.path.exists(".env"):
        with open(".env", "w") as f:
            f.write(f"OPENAI_API_KEY={args.api_key}\n")
            if args.model:
                f.write(f"MODEL={args.model}\n")
        logger.info("Created .env file with provided API key")
        # Reload environment variables
        load_dotenv()
    
    # Debug: Print environment variables
    logger.info(f"Platform: {sys.platform}")
    logger.info(f"OpenAI API Key present: {bool(os.environ.get('OPENAI_API_KEY'))}")
    logger.info(f"MODEL environment variable: {os.environ.get('MODEL', 'Not set, using default gpt-4o-mini')}")
    
    # Create the Financial Advisor
    try:
        model = args.model or os.environ.get("MODEL", "gpt-4o-mini")
        advisor = FinancialAdvisor(user_id=args.user_id, model=model)
    except Exception as e:
        logger.error(f"Failed to create Financial Advisor: {str(e)}")
        if "api_key" in str(e).lower():
            logger.error("API key error. Make sure your OpenAI API key is correctly set.")
            # Check .env file exists
            if not os.path.exists(".env"):
                logger.error("No .env file found. Create one with OPENAI_API_KEY=your-key")
        return
    
    # Welcome message
    print("\n" + "="*80)
    print("💼 Financial Advisor Assistant 💼")
    print("="*80)
    print("\nThis application uses OpenAI for financial guidance.")
    print(f"Powered by OpenAI's {model} model")
    print("\nAsk me any financial questions, and I'll do my best to help!")
    print("\nType 'exit' or 'quit' to end the session.")
    print("="*80 + "\n")
    
    # Main interaction loop
    try:
        while True:
            # Get user input
            user_input = input("Question: ")
            
            # Check for exit command
            if user_input.lower() in ["exit", "quit"]:
                print("\nThank you for using the Financial Advisor. Goodbye!")
                break
                
            # Process the query
            print("\nProcessing your query...\n")
            response = advisor.query(user_input)
            
            # Print the response
            print(f"Response: {response}\n")
            print("-"*80 + "\n")
            
    except KeyboardInterrupt:
        print("\n\nSession terminated by user. Goodbye!")
    except Exception as e:
        logger.error(f"Error in main loop: {str(e)}")
        print(f"\nAn error occurred: {str(e)}")
        print("The application will now exit.")

if __name__ == "__main__":
    main()
