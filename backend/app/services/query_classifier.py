"""
Query classification service to determine query type and intent.
"""

import re
from typing import Dict, Any, Optional
from app.models.schemas import QueryType


class QueryClassifier:
    """Service for classifying user queries."""
    
    # Keywords for different query types
    EARNINGS_KEYWORDS = [
        "earn", "earning", "earnings", "yield", "apr", "apy", "return", "returns",
        "profit", "income", "interest", "reward", "rewards", "make money",
        "how much", "calculate", "calculator"
    ]
    
    RISK_KEYWORDS = [
        "risk", "risks", "risky", "safe", "safety", "secure", "security",
        "danger", "dangerous", "lose", "loss", "losses", "audit", "audited",
        "hack", "hacked", "exploit", "vulnerability", "insurance"
    ]
    
    TECHNICAL_KEYWORDS = [
        "how to", "how do i", "tutorial", "guide", "step", "steps",
        "deposit", "withdraw", "connect", "wallet", "transaction",
        "metamask", "phantom", "solana", "blockchain"
    ]
    
    def classify(self, query: str, pool_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Classify query type and extract relevant information.
        
        Args:
            query: User's query text
            pool_id: Optional pool ID from request
            
        Returns:
            Dictionary with classification results
        """
        query_lower = query.lower()
        
        # Determine query type
        query_type = self._determine_type(query_lower)
        
        # Extract entities
        extracted_pool = self._extract_pool_id(query_lower) if not pool_id else pool_id
        extracted_amount = self._extract_amount(query_lower)
        extracted_currency = self._extract_currency(query_lower)
        
        # Calculate confidence
        confidence = self._calculate_confidence(query_lower, query_type)
        
        return {
            "query_type": query_type,
            "pool_id": extracted_pool,
            "amount": extracted_amount,
            "currency": extracted_currency,
            "confidence": confidence,
            "requires_apr": query_type == QueryType.EARNINGS,
        }
    
    def _determine_type(self, query: str) -> str:
        """Determine the type of query."""
        # Check for earnings queries
        if any(keyword in query for keyword in self.EARNINGS_KEYWORDS):
            return QueryType.EARNINGS
        
        # Check for risk queries
        if any(keyword in query for keyword in self.RISK_KEYWORDS):
            return QueryType.RISK
        
        # Check for technical/how-to queries
        if any(keyword in query for keyword in self.TECHNICAL_KEYWORDS):
            return QueryType.TECHNICAL
        
        # Default to general
        return QueryType.GENERAL
    
    def _extract_pool_id(self, query: str) -> Optional[str]:
        """Extract pool ID from query text."""
        # Common pool patterns
        pool_patterns = [
            r"allez[- ]?usdc",
            r"main[- ]?usdc",
            r"jito[- ]?sol",
            r"usdt[- ]?main",
        ]
        
        for pattern in pool_patterns:
            match = re.search(pattern, query)
            if match:
                # Normalize to hyphenated format
                pool_name = match.group(0).replace(" ", "-").lower()
                return pool_name
        
        return None
    
    def _extract_amount(self, query: str) -> Optional[float]:
        """Extract amount from query text."""
        # Patterns for amounts
        patterns = [
            r"(\d+(?:,\d{3})*(?:\.\d+)?)\s*(?:usdc|usdt|usd|dollars?)",
            r"\$\s*(\d+(?:,\d{3})*(?:\.\d+)?)",
            r"(\d+(?:,\d{3})*(?:\.\d+)?)\s+(?:in|on|with)",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, query)
            if match:
                amount_str = match.group(1).replace(",", "")
                try:
                    return float(amount_str)
                except ValueError:
                    continue
        
        return None
    
    def _extract_currency(self, query: str) -> Optional[str]:
        """Extract currency from query text."""
        currencies = ["usdc", "usdt", "usd", "sol", "eth", "btc"]
        
        for currency in currencies:
            if currency in query:
                return currency.upper()
        
        return None
    
    def _calculate_confidence(self, query: str, query_type: str) -> float:
        """Calculate confidence score for classification."""
        confidence = 0.5  # Base confidence
        
        # Increase confidence based on keyword matches
        if query_type == QueryType.EARNINGS:
            matches = sum(1 for kw in self.EARNINGS_KEYWORDS if kw in query)
            confidence += min(matches * 0.1, 0.4)
        
        elif query_type == QueryType.RISK:
            matches = sum(1 for kw in self.RISK_KEYWORDS if kw in query)
            confidence += min(matches * 0.1, 0.4)
        
        elif query_type == QueryType.TECHNICAL:
            matches = sum(1 for kw in self.TECHNICAL_KEYWORDS if kw in query)
            confidence += min(matches * 0.1, 0.4)
        
        # Increase confidence if specific entities are found
        if self._extract_pool_id(query):
            confidence += 0.1
        if self._extract_amount(query):
            confidence += 0.1
        
        return min(confidence, 1.0)


# Global instance
def get_query_classifier() -> QueryClassifier:
    """Get QueryClassifier instance."""
    return QueryClassifier()
