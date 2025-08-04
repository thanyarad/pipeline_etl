from typing import Optional, Dict, Any

from langchain_openai import ChatOpenAI
# from langchain_google_genai import ChatGoogleGenerativeAI  # Commented out temporarily

from src.config.settings import (
    OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL,
    # GOOGLE_API_KEY, GOOGLE_MODEL,
    DEFAULT_LLM_PROVIDER
)

# Default LLM provider configurations
LLM_CONFIGS = {
    "openai": {
        "api_key": OPENAI_API_KEY,
        "base_url": OPENAI_BASE_URL,
        "model": OPENAI_MODEL,
        "temperature": 1
    },
    # "google": {
    #     "api_key": GOOGLE_API_KEY,
    #     "model": GOOGLE_MODEL,
    #     "temperature": 1
    # }
}

def initialize_openai_llm(config: Optional[Dict[str, Any]] = None) -> ChatOpenAI:
    """Initialize OpenAI LLM with custom or default configuration."""
    if config is None:
        config = LLM_CONFIGS["openai"]
    
    return ChatOpenAI(
        temperature=config.get("temperature", 1),
        base_url=config.get("base_url", OPENAI_BASE_URL),
        api_key=config.get("api_key", OPENAI_API_KEY),
        model=config.get("model", OPENAI_MODEL)
    )

# def initialize_google_llm(config: Optional[Dict[str, Any]] = None) -> ChatGoogleGenerativeAI:
#     """Initialize Google LLM with custom or default configuration."""
#     if config is None:
#         config = LLM_CONFIGS["google"]
#     
#     return ChatGoogleGenerativeAI(
#         temperature=config.get("temperature", 1),
#         model=config.get("model", "gemini-pro")
#     )

def get_llm_provider(provider_name: str, config: Optional[Dict[str, Any]] = None):
    """
    Get LLM instance based on provider name.
    
    Args:
        provider_name: Name of the LLM provider ("openai", "anthropic", "google", "ollama")
        config: Optional custom configuration dictionary
    
    Returns:
        LLM instance
    
    Raises:
        ValueError: If provider is not supported
    """
    provider_functions = {
        "openai": initialize_openai_llm,
        # "google": initialize_google_llm  # Commented out temporarily
    }
    
    if provider_name not in provider_functions:
        raise ValueError(f"Unsupported LLM provider: {provider_name}. "
                        f"Supported providers: {list(provider_functions.keys())}")
    
    return provider_functions[provider_name](config)

def get_available_providers() -> list:
    """Get list of available LLM providers."""
    return list(LLM_CONFIGS.keys())

def update_llm_config(provider_name: str, new_config: Dict[str, Any]) -> None:
    """
    Update configuration for a specific LLM provider.
    
    Args:
        provider_name: Name of the LLM provider
        new_config: New configuration dictionary
    """
    if provider_name not in LLM_CONFIGS:
        raise ValueError(f"Unknown provider: {provider_name}")
    
    LLM_CONFIGS[provider_name].update(new_config)

def get_default_llm():
    """
    Get the default LLM instance based on DEFAULT_LLM_PROVIDER setting.
    
    Returns:
        LLM instance
    """
    return get_llm_provider(DEFAULT_LLM_PROVIDER) 