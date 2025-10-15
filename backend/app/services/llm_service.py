import os
from .llm.base_strategy import LLMStrategy
from .llm.openai_strategy import OpenAIStrategy
from .llm.gemini_strategy import GeminiStrategy

def get_llm_strategy() -> LLMStrategy:
    """
    Factory function to select and instantiate the appropriate LLM strategy.
    
    Reads the 'LLM_PROVIDER' environment variable to determine which
    strategy to use. Defaults to OpenAI if not set.

    Returns:
        An instance of a class that conforms to the LLMStrategy interface.
    
    Raises:
        ValueError: If an unsupported LLM_PROVIDER is specified.
    """
    provider = os.getenv("LLM_PROVIDER", "openai").lower()
    
    if provider == "openai":
        return OpenAIStrategy()
    elif provider == "gemini":
        return GeminiStrategy()
    else:
        raise ValueError(f"Unsupported LLM provider '{provider}' specified in .env.")

def generate_cover_letter(cv_content: str, job_description: str) -> str:
    """
    Generates a professional cover letter using the configured LLM strategy.

    This function acts as the "Context" in the Strategy Pattern. It is
    closed for modification but open for extension, as new strategies can be
    added to the factory without changing this function's code.

    Args:
        cv_content: The text content of the user's CV.
        job_description: The text content of the target job description.

    Returns:
        A formatted, professional cover letter string.
    """
    # 1. Get the currently configured strategy from the factory
    strategy = get_llm_strategy()
    
    # 2. Execute the strategy's generate method
    # This function does not know or care if it's OpenAI or Gemini.
    return strategy.generate(cv_content, job_description)

