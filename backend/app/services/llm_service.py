"""
Multi-LLM service supporting OpenAI, Anthropic, and Llama.
Uses adapter pattern for provider abstraction.
"""

from typing import Optional, Dict, Any, List
from abc import ABC, abstractmethod
import openai
from anthropic import AsyncAnthropic
from app.core.config import settings


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""
    
    @abstractmethod
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ) -> Dict[str, Any]:
        """
        Generate response from LLM.
        
        Args:
            prompt: User prompt
            system_prompt: System prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            
        Returns:
            Dictionary with 'content' and 'usage' keys
        """
        pass


class OpenAIProvider(LLMProvider):
    """OpenAI GPT provider."""
    
    def __init__(self, api_key: str, model: str):
        self.client = openai.AsyncOpenAI(api_key=api_key)
        self.model = model
    
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ) -> Dict[str, Any]:
        """Generate response using OpenAI API."""
        messages = []
        
        # o1 and o3 models don't support system messages
        # Prepend system prompt to user message instead
        if any(x in self.model for x in ["o1-", "o3-"]):
            if system_prompt:
                prompt = f"{system_prompt}\n\n{prompt}"
        else:
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        # Build completion parameters
        completion_params = {
            "model": self.model,
            "messages": messages,
        }
        
        # o1 and o3 models don't support temperature, top_p, or system messages
        # They also use max_completion_tokens instead of max_tokens
        if any(x in self.model for x in ["o1-", "o3-"]):
            completion_params["max_completion_tokens"] = max_tokens
            # Don't set temperature for o1/o3 models
        # GPT-5 models have restrictions: no temperature, use max_completion_tokens via extra_body
        elif "gpt-5" in self.model:
            completion_params["extra_body"] = {"max_completion_tokens": max_tokens}
            # Don't set temperature for GPT-5 models
        # Search preview models don't support temperature, use max_tokens (standard parameter)
        elif "search-preview" in self.model:
            completion_params["max_tokens"] = max_tokens
            # Don't set temperature for search-preview models
        # GPT-4o models use max_completion_tokens via extra_body
        elif "gpt-4o" in self.model:
            completion_params["extra_body"] = {"max_completion_tokens": max_tokens}
            completion_params["temperature"] = temperature
        # Older models use standard max_tokens parameter
        else:
            completion_params["max_tokens"] = max_tokens
            completion_params["temperature"] = temperature
        
        response = await self.client.chat.completions.create(**completion_params)
        
        content = response.choices[0].message.content
        
        # Log if content is empty
        if not content or content.strip() == "":
            print(f"⚠️ WARNING: GPT-5 returned empty content!")
            print(f"Model: {self.model}")
            print(f"Finish reason: {response.choices[0].finish_reason}")
            print(f"Usage: {response.usage}")
            content = "I apologize, but I couldn't generate a response. Please try rephrasing your question."
        
        return {
            "content": content,
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            },
            "model": self.model,
            "provider": "openai",
        }


class AnthropicProvider(LLMProvider):
    """Anthropic Claude provider."""
    
    def __init__(self, api_key: str, model: str):
        self.client = AsyncAnthropic(api_key=api_key)
        self.model = model
    
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ) -> Dict[str, Any]:
        """Generate response using Anthropic API."""
        response = await self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_prompt or "",
            messages=[
                {"role": "user", "content": prompt}
            ],
        )
        
        return {
            "content": response.content[0].text,
            "usage": {
                "prompt_tokens": response.usage.input_tokens,
                "completion_tokens": response.usage.output_tokens,
                "total_tokens": response.usage.input_tokens + response.usage.output_tokens,
            },
            "model": self.model,
            "provider": "anthropic",
        }


class MockProvider(LLMProvider):
    """Mock LLM provider for testing without API keys."""
    
    def __init__(self):
        self.model = "mock-llm"
    
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ) -> Dict[str, Any]:
        """Generate mock response for testing."""
        # Extract query from prompt
        query_line = [line for line in prompt.split('\n') if 'question:' in line.lower()]
        query = query_line[0].split(':', 1)[1].strip() if query_line else "question"
        
        # Generate simple mock response
        if "earn" in query.lower() or "apr" in query.lower() or "yield" in query.lower():
            content = (
                "Kamino Finance offers competitive lending rates on Solana. "
                "The APR varies based on market conditions and pool utilization. "
                "You can earn passive income by depositing your assets into lending pools. "
                "Please note that rates are variable and subject to change."
            )
        elif "risk" in query.lower():
            content = (
                "Lending on Kamino involves several risks including smart contract risk, "
                "market volatility, and liquidation risk. Kamino has been audited by reputable "
                "security firms. Always do your own research and only invest what you can afford to lose."
            )
        elif "how" in query.lower() and ("deposit" in query.lower() or "use" in query.lower()):
            content = (
                "To use Kamino Finance: 1) Connect your Solana wallet (Phantom, Solflare, etc.), "
                "2) Select the asset you want to deposit, 3) Choose the lending pool, "
                "4) Approve the transaction. Your deposits will start earning interest immediately."
            )
        else:
            content = (
                "Kamino Finance is a leading DeFi protocol on Solana offering automated "
                "liquidity management and lending services. It provides users with optimized "
                "yield strategies and efficient capital deployment across various DeFi protocols."
            )
        
        return {
            "content": content,
            "usage": {
                "prompt_tokens": len(prompt.split()),
                "completion_tokens": len(content.split()),
                "total_tokens": len(prompt.split()) + len(content.split()),
            },
            "model": "mock-llm",
            "provider": "mock",
        }


class LLMService:
    """Service for managing LLM interactions with multiple providers."""
    
    def __init__(self):
        self.provider = self._initialize_provider()
    
    def _initialize_provider(self) -> LLMProvider:
        """Initialize LLM provider based on configuration."""
        provider_name = settings.llm_provider.lower()
        
        # Mock provider for testing without API keys
        if provider_name == "mock":
            return MockProvider()
        
        if provider_name == "openai":
            if not settings.openai_api_key or settings.openai_api_key.startswith("sk-your"):
                print("⚠️  OpenAI API key not configured, using mock provider")
                return MockProvider()
            return OpenAIProvider(
                api_key=settings.openai_api_key,
                model=settings.openai_model
            )
        
        elif provider_name == "anthropic":
            if not settings.anthropic_api_key or settings.anthropic_api_key.startswith("sk-ant-your"):
                print("⚠️  Anthropic API key not configured, using mock provider")
                return MockProvider()
            return AnthropicProvider(
                api_key=settings.anthropic_api_key,
                model=settings.anthropic_model
            )
        
        else:
            print(f"⚠️  Unknown LLM provider '{provider_name}', using mock provider")
            return MockProvider()
    
    async def generate_answer(
        self,
        query: str,
        context: Optional[str] = None,
        query_type: str = "general",
        dapp: str = "kamino",
        temperature: float = 0.7,
    ) -> Dict[str, Any]:
        """
        Generate answer for user query.
        
        Args:
            query: User's question
            context: Retrieved context from RAG
            query_type: Type of query (earnings, general, etc.)
            dapp: DeFi service name
            temperature: Sampling temperature
            
        Returns:
            Dictionary with answer and metadata
        """
        system_prompt = self._build_system_prompt(query_type, dapp)
        user_prompt = self._build_user_prompt(query, context, dapp)
        
        # Reasoning models (o1, o3, GPT-5) need more tokens for reasoning + output
        # Lower value = faster but may cut off response
        is_reasoning_model = any(x in self.provider.model for x in ["o1-", "o3-", "gpt-5"])
        max_tokens = 4000 if is_reasoning_model else 1500
        
        response = await self.provider.generate(
            prompt=user_prompt,
            system_prompt=system_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        
        return response
    
    def _build_system_prompt(self, query_type: str, dapp: str = "kamino") -> str:
        """Build system prompt based on query type and DeFi service."""
        # DeFi service names mapping
        dapp_names = {
            "kamino": "Kamino Finance (Solana DeFi)",
            "aave": "Aave (Multi-chain DeFi)",
            "compound": "Compound Finance (Ethereum DeFi)",
            "marinade": "Marinade Finance (Solana Liquid Staking)",
            "lido": "Lido (Multi-chain Liquid Staking)",
            "uniswap": "Uniswap (Ethereum DEX)",
            "curve": "Curve Finance (Multi-chain Stableswap)",
            "convex": "Convex Finance (Curve Optimizer)",
            "yearn": "Yearn Finance (Yield Aggregator)",
            "maker": "MakerDAO (Ethereum CDP)",
            "raydium": "Raydium (Solana DEX)",
            "orca": "Orca (Solana DEX)",
            "jupiter": "Jupiter (Solana Aggregator)",
            "drift": "Drift Protocol (Solana Perpetuals)",
            "mango": "Mango Markets (Solana Trading)",
            "reflect": "Reflect >> Autonomous money designed for the stablecoin era (Solana Defi)",
        }
        
        service_name = dapp_names.get(dapp.lower(), f"{dapp} DeFi")
        
        base_prompt = (
            f"You are Chewie AI assistant embedded as a browser extension widget on the {service_name} website. "
            f"You are STRICTLY LIMITED to answering questions about {service_name} ONLY.\n\n"
            
            "CRITICAL RULES - FOLLOW EXACTLY:\n\n"
            
            f"1. PROTOCOL RESTRICTION:\n"
            f"   - You can ONLY discuss {service_name}\n"
            f"   - If the question mentions ANY other DeFi protocol name (Aave, Compound, Uniswap, Hyperliquid, etc.), "
            f"you MUST refuse to answer\n"
            f"   - If asked about another protocol, respond EXACTLY:\n"
            f"   \"I can only answer questions about {service_name}, as I'm the assistant widget on their page. "
            "For information about other protocols, please visit their official website.\"\n\n"
            
            "2. NON-DEFI TOPICS:\n"
            "   - If the question is about weather, sports, politics, or any non-DeFi topic, respond:\n"
            "   \"I'm a DeFi assistant and can only help with questions about decentralized finance. "
            "Please ask me about DeFi topics.\"\n\n"
            
            f"3. VALID QUESTIONS (about {service_name} only):\n"
            "   - Provide concise, accurate answers (2-3 paragraphs max)\n"
            "   - Use simple language and cite sources when available\n"
            f"   - Focus exclusively on {service_name} features, yields, and risks\n"
            "   - NEVER mention, compare, or recommend other protocols\n\n"
            
            f"REMEMBER: You are on the {service_name} website. Do NOT provide information about any other protocol."
        )
        
        if query_type == "earnings":
            base_prompt += (
                "\nFor earnings queries:\n"
                "- Clearly state the APR and calculated earnings\n"
                "- Mention that rates are variable and subject to change\n"
                "- Briefly note key risks (smart contract, market volatility)\n"
            )
        elif query_type == "risk":
            base_prompt += (
                "\nFor risk queries:\n"
                "- Be transparent about risks\n"
                "- Mention smart contract audits if available\n"
                "- Explain impermanent loss, liquidation risks where relevant\n"
            )
        
        return base_prompt
    
    def _build_user_prompt(self, query: str, context: Optional[str] = None, dapp: str = "kamino") -> str:
        """Build user prompt with query and context."""
        if context:
            return (
                f"Context from {dapp} documentation:\n\n{context}\n\n"
                f"User question: {query}\n\n"
                f"Please answer based on the provided context."
            )
        else:
            return f"User question: {query}"
    
    async def generate_followup_questions(
        self,
        query: str,
        answer: str,
        count: int = 3,
    ) -> List[str]:
        """
        Generate follow-up questions based on query and answer.
        
        Args:
            query: Original query
            answer: Generated answer
            count: Number of follow-ups to generate
            
        Returns:
            List of follow-up questions
        """
        prompt = (
            f"Original question: {query}\n\n"
            f"Answer provided: {answer}\n\n"
            f"Generate {count} relevant follow-up questions that a user "
            f"might ask next. Return only the questions, one per line."
        )
        
        response = await self.provider.generate(
            prompt=prompt,
            temperature=0.8,
            max_tokens=200,
        )
        
        # Parse questions from response
        questions = [
            q.strip().lstrip("0123456789.-) ")
            for q in response["content"].split("\n")
            if q.strip()
        ]
        
        return questions[:count]


# Global instance
_llm_service: Optional[LLMService] = None


def get_llm_service() -> LLMService:
    """Get or create LLMService instance."""
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service
