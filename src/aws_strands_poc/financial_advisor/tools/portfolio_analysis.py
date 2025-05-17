"""
Portfolio Analysis Tool - Analyzes an investment portfolio for various financial metrics.
"""

from strands import tool
import math
import random  # For mock data in POC

@tool
def portfolio_analysis(portfolio: list, metrics: list = ["risk", "return", "sharpe"]) -> dict:
    """
    Analyze an investment portfolio for various financial metrics.
    
    Args:
        portfolio: List of dictionaries with ticker and allocation percentage
                  e.g., [{"ticker": "AAPL", "allocation": 20}, {"ticker": "MSFT", "allocation": 15}]
        metrics: List of metrics to calculate
    
    Returns:
        Dictionary with calculated metrics for the portfolio
    """
    # Mock stock data - in a real implementation, this would fetch actual historical data
    # and calculate real metrics
    stock_metrics = {
        "AAPL": {"annual_return": 0.15, "volatility": 0.20, "beta": 1.2, "alpha": 0.03},
        "MSFT": {"annual_return": 0.12, "volatility": 0.18, "beta": 1.1, "alpha": 0.02},
        "GOOGL": {"annual_return": 0.14, "volatility": 0.22, "beta": 1.3, "alpha": 0.025},
        "AMZN": {"annual_return": 0.16, "volatility": 0.25, "beta": 1.4, "alpha": 0.035},
        "META": {"annual_return": 0.18, "volatility": 0.28, "beta": 1.5, "alpha": 0.04},
        "TSLA": {"annual_return": 0.25, "volatility": 0.40, "beta": 2.0, "alpha": 0.05},
        "NVDA": {"annual_return": 0.30, "volatility": 0.35, "beta": 1.8, "alpha": 0.06},
        "JPM": {"annual_return": 0.10, "volatility": 0.15, "beta": 0.9, "alpha": 0.015},
        "V": {"annual_return": 0.11, "volatility": 0.14, "beta": 0.85, "alpha": 0.018},
        "WMT": {"annual_return": 0.08, "volatility": 0.12, "beta": 0.7, "alpha": 0.01}
    }
    
    # Default values for unknown stocks
    default_metrics = {"annual_return": 0.10, "volatility": 0.20, "beta": 1.0, "alpha": 0.02}
    
    # Risk-free rate for Sharpe ratio calculation
    risk_free_rate = 0.04  # 4% as an example
    
    # Verify portfolio allocations sum to approximately 100%
    total_allocation = sum(item["allocation"] for item in portfolio)
    if not (95 <= total_allocation <= 105):
        return {
            "error": f"Portfolio allocations should sum to approximately 100%. Current total: {total_allocation}%"
        }
    
    # Normalize allocations to exactly 100%
    for item in portfolio:
        item["allocation"] = item["allocation"] / total_allocation * 100
    
    # Calculate weighted metrics
    weighted_return = 0
    weighted_volatility = 0
    weighted_beta = 0
    weighted_alpha = 0
    
    for item in portfolio:
        ticker = item["ticker"].upper()
        allocation = item["allocation"] / 100  # Convert percentage to decimal
        stock_metric = stock_metrics.get(ticker, default_metrics)
        
        weighted_return += stock_metric["annual_return"] * allocation
        weighted_volatility += stock_metric["volatility"] * allocation
        weighted_beta += stock_metric["beta"] * allocation
        weighted_alpha += stock_metric["alpha"] * allocation
    
    # Calculate Sharpe ratio
    sharpe_ratio = (weighted_return - risk_free_rate) / weighted_volatility if weighted_volatility > 0 else 0
    
    # Prepare result based on requested metrics
    result = {
        "portfolio_summary": {
            "tickers": [item["ticker"].upper() for item in portfolio],
            "total_allocation": total_allocation
        }
    }
    
    if "return" in metrics:
        result["annual_return"] = round(weighted_return * 100, 2)  # Convert to percentage
    
    if "risk" in metrics:
        result["risk"] = {
            "volatility": round(weighted_volatility * 100, 2),     # Convert to percentage
            "beta": round(weighted_beta, 2)
        }
        
    if "alpha" in metrics:
        result["alpha"] = round(weighted_alpha * 100, 2)          # Convert to percentage
        
    if "sharpe" in metrics:
        result["sharpe_ratio"] = round(sharpe_ratio, 2)
    
    # Add portfolio diversification score (mock calculation)
    if "diversification" in metrics:
        industry_exposure = {
            "Technology": sum(item["allocation"] for item in portfolio 
                           if item["ticker"].upper() in ["AAPL", "MSFT", "GOOGL", "META", "NVDA"]),
            "Consumer": sum(item["allocation"] for item in portfolio 
                         if item["ticker"].upper() in ["AMZN", "WMT"]),
            "Financial": sum(item["allocation"] for item in portfolio 
                          if item["ticker"].upper() in ["JPM", "V"]),
            "Automotive": sum(item["allocation"] for item in portfolio 
                           if item["ticker"].upper() in ["TSLA"]),
            "Other": sum(item["allocation"] for item in portfolio 
                       if item["ticker"].upper() not in ["AAPL", "MSFT", "GOOGL", "META", "NVDA", 
                                                       "AMZN", "WMT", "JPM", "V", "TSLA"])
        }
        
        # Calculate a diversification score (higher is better)
        num_industries = sum(1 for exposure in industry_exposure.values() if exposure > 0)
        max_industry_exposure = max(industry_exposure.values())
        
        diversification_score = (num_industries / 5) * (1 - (max_industry_exposure / 100))
        result["diversification"] = {
            "score": round(diversification_score * 10, 1),  # Scale to 0-10
            "industry_exposure": {k: round(v, 1) for k, v in industry_exposure.items() if v > 0}
        }
    
    return result
