"""
Financial specialist agents that provide domain-specific expertise.
"""

from aws_strands_poc.financial_advisor.specialists.market_analyst import market_analyst
from aws_strands_poc.financial_advisor.specialists.portfolio_manager import portfolio_manager
from aws_strands_poc.financial_advisor.specialists.compliance_officer import compliance_officer
from aws_strands_poc.financial_advisor.specialists.tax_specialist import tax_specialist

__all__ = [
    "market_analyst",
    "portfolio_manager",
    "compliance_officer",
    "tax_specialist",
]
