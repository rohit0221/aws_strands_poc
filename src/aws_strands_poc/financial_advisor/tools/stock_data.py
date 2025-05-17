"""
Stock Data Tool - Fetches stock price data for a given ticker symbol.
"""

from strands import tool
import json
import random  # For mock data in POC

@tool
def stock_data(ticker: str, timeframe: str = "1d") -> dict:
    """
    Fetch stock price data for a given ticker symbol.
    
    Args:
        ticker: Stock ticker symbol (e.g., AAPL, MSFT)
        timeframe: Time period for data (1d, 5d, 1mo, 3mo, 6mo, 1y, 5y)
    
    Returns:
        Dictionary containing stock price data including open, high, low, close prices
    """
    # Note: In a real implementation, this would use an API like yfinance
    # For the POC, we'll generate mock data
    
    # Mock base prices for common tickers
    base_prices = {
        "AAPL": 175.0,
        "MSFT": 350.0,
        "GOOGL": 140.0,
        "AMZN": 180.0,
        "META": 450.0,
        "TSLA": 180.0,
        "NVDA": 920.0,
        "JPM": 185.0,
        "V": 270.0,
        "WMT": 60.0
    }
    
    # Default price for unknown tickers
    base_price = base_prices.get(ticker.upper(), 100.0)
    
    # Generate mock data with realistic fluctuations
    data = []
    current_price = base_price
    
    # Number of data points based on timeframe
    points = {
        "1d": 24,      # Hourly for 1 day
        "5d": 5,       # Daily for 5 days
        "1mo": 30,     # Daily for 1 month
        "3mo": 90,     # Daily for 3 months
        "6mo": 180,    # Daily for 6 months
        "1y": 12,      # Monthly for 1 year
        "5y": 20       # Quarterly for 5 years
    }.get(timeframe, 10)
    
    for i in range(points):
        # Generate realistic daily fluctuations (within ±2%)
        daily_change = current_price * random.uniform(-0.02, 0.02)
        open_price = current_price
        close_price = current_price + daily_change
        high_price = max(open_price, close_price) * (1 + random.uniform(0, 0.01))
        low_price = min(open_price, close_price) * (1 - random.uniform(0, 0.01))
        
        data.append({
            "date": f"2025-{(5 - i//30):02d}-{(17 - i%30):02d}" if i < 180 else f"2024-{(12 - i//30):02d}-{(30 - i%30):02d}",
            "open": round(open_price, 2),
            "high": round(high_price, 2),
            "low": round(low_price, 2),
            "close": round(close_price, 2),
            "volume": int(random.uniform(1000000, 10000000))
        })
        current_price = close_price
    
    result = {
        "ticker": ticker.upper(),
        "timeframe": timeframe,
        "currency": "USD",
        "data": data
    }
    
    return result
