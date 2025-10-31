"""
Earnings calculator service for computing yields and returns.
"""

from typing import Dict, Any


class EarningsCalculator:
    """Service for calculating earnings from APR data."""
    
    @staticmethod
    def calculate_earnings(
        amount: float,
        apr: float,
        currency: str = "USDC"
    ) -> Dict[str, float]:
        """
        Calculate yearly and monthly earnings from APR.
        
        Args:
            amount: Principal amount
            apr: Annual Percentage Rate (as decimal, e.g., 0.124 for 12.4%)
            currency: Currency code
            
        Returns:
            Dictionary with yearly and monthly earnings
        """
        yearly = amount * apr
        monthly = yearly / 12
        
        return {
            "yearly": round(yearly, 2),
            "monthly": round(monthly, 2),
            "daily": round(yearly / 365, 2),
        }
    
    @staticmethod
    def calculate_apy_from_apr(apr: float, compound_frequency: int = 365) -> float:
        """
        Calculate APY (Annual Percentage Yield) from APR.
        
        Args:
            apr: Annual Percentage Rate (as decimal)
            compound_frequency: Number of times interest compounds per year
            
        Returns:
            APY as decimal
        """
        apy = (1 + apr / compound_frequency) ** compound_frequency - 1
        return round(apy, 6)
    
    @staticmethod
    def calculate_future_value(
        principal: float,
        apr: float,
        years: float,
        compound_frequency: int = 365
    ) -> float:
        """
        Calculate future value with compound interest.
        
        Args:
            principal: Initial amount
            apr: Annual Percentage Rate (as decimal)
            years: Number of years
            compound_frequency: Compounding frequency per year
            
        Returns:
            Future value
        """
        rate_per_period = apr / compound_frequency
        total_periods = compound_frequency * years
        
        future_value = principal * (1 + rate_per_period) ** total_periods
        return round(future_value, 2)
    
    @staticmethod
    def format_currency(amount: float, currency: str = "USD") -> str:
        """
        Format amount as currency string.
        
        Args:
            amount: Amount to format
            currency: Currency code
            
        Returns:
            Formatted string (e.g., '$1,234.56')
        """
        if currency in ["USD", "USDC", "USDT"]:
            return f"${amount:,.2f}"
        elif currency in ["EUR", "EURC"]:
            return f"€{amount:,.2f}"
        else:
            return f"{amount:,.2f} {currency}"


# Global instance
def get_earnings_calculator() -> EarningsCalculator:
    """Get EarningsCalculator instance."""
    return EarningsCalculator()
