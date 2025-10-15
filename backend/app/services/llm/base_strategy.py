from abc import ABC, abstractmethod

class LLMStrategy(ABC):
    """
    Abstract Base Class for LLM provider strategies.
    
    This defines the common interface that all concrete LLM provider
    classes must implement, ensuring they are interchangeable.
    """

    @abstractmethod
    def generate(self, cv_content: str, job_description: str) -> str:
        """
        The core method to generate a cover letter.

        Args:
            cv_content: The text content of the user's CV.
            job_description: The text content of the target job description.

        Returns:
            A formatted, professional cover letter string.
        
        Raises:
            ConnectionError: If the API call to the LLM provider fails.
        """
        pass
