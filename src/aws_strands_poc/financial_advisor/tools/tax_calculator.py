"""
Tax Calculator Tool - Calculates estimated taxes based on income and deductions.
"""

from strands import tool

@tool
def tax_calculator(income: float, deductions: float = 0, filing_status: str = "single") -> dict:
    """
    Calculate estimated taxes based on income and deductions.
    
    Args:
        income: Annual income amount
        deductions: Total deductions amount
        filing_status: Tax filing status (single, married, head_of_household)
    
    Returns:
        Dictionary with calculated tax amounts in different brackets
    """
    # Verify inputs
    if income < 0:
        return {"error": "Income cannot be negative"}
    
    if deductions < 0:
        return {"error": "Deductions cannot be negative"}
    
    filing_status = filing_status.lower()
    if filing_status not in ["single", "married", "head_of_household"]:
        return {"error": "Filing status must be 'single', 'married', or 'head_of_household'"}
    
    # 2024 tax brackets (simplified for POC)
    tax_brackets = {
        "single": [
            {"rate": 0.10, "min": 0, "max": 11600},
            {"rate": 0.12, "min": 11601, "max": 47150},
            {"rate": 0.22, "min": 47151, "max": 100525},
            {"rate": 0.24, "min": 100526, "max": 191950},
            {"rate": 0.32, "min": 191951, "max": 243725},
            {"rate": 0.35, "min": 243726, "max": 609350},
            {"rate": 0.37, "min": 609351, "max": float('inf')}
        ],
        "married": [
            {"rate": 0.10, "min": 0, "max": 23200},
            {"rate": 0.12, "min": 23201, "max": 94300},
            {"rate": 0.22, "min": 94301, "max": 201050},
            {"rate": 0.24, "min": 201051, "max": 383900},
            {"rate": 0.32, "min": 383901, "max": 487450},
            {"rate": 0.35, "min": 487451, "max": 731200},
            {"rate": 0.37, "min": 731201, "max": float('inf')}
        ],
        "head_of_household": [
            {"rate": 0.10, "min": 0, "max": 16550},
            {"rate": 0.12, "min": 16551, "max": 63100},
            {"rate": 0.22, "min": 63101, "max": 100500},
            {"rate": 0.24, "min": 100501, "max": 191950},
            {"rate": 0.32, "min": 191951, "max": 243700},
            {"rate": 0.35, "min": 243701, "max": 609350},
            {"rate": 0.37, "min": 609351, "max": float('inf')}
        ]
    }
    
    # Standard deduction based on filing status
    standard_deductions = {
        "single": 14600,
        "married": 29200,
        "head_of_household": 21900
    }
    
    # Use the higher of standard deduction or itemized deductions
    effective_deduction = max(standard_deductions[filing_status], deductions)
    
    # Calculate taxable income
    taxable_income = max(0, income - effective_deduction)
    
    # Calculate tax by bracket
    brackets_used = tax_brackets[filing_status]
    tax_by_bracket = []
    total_tax = 0
    
    for bracket in brackets_used:
        if taxable_income > bracket["min"]:
            bracket_income = min(taxable_income, bracket["max"]) - bracket["min"]
            bracket_tax = bracket_income * bracket["rate"]
            total_tax += bracket_tax
            
            tax_by_bracket.append({
                "bracket_rate": f"{bracket['rate']*100:.1f}%",
                "income_in_bracket": round(bracket_income, 2),
                "tax_amount": round(bracket_tax, 2)
            })
    
    # Calculate effective tax rate
    effective_tax_rate = total_tax / income if income > 0 else 0
    
    result = {
        "income": income,
        "deductions": {
            "itemized": deductions,
            "standard": standard_deductions[filing_status],
            "effective": effective_deduction
        },
        "taxable_income": taxable_income,
        "tax_by_bracket": tax_by_bracket,
        "total_tax": round(total_tax, 2),
        "effective_tax_rate": f"{effective_tax_rate*100:.2f}%"
    }
    
    return result
