import os
from .base_strategy import LLMStrategy
import google.generativeai as genai

class GeminiStrategy(LLMStrategy):
    """Concrete strategy for generating cover letters using the Google Gemini API."""

    def __init__(self):
        """
        Configures the Gemini client upon initialization.
        Ensures the GEMINI_API_KEY is set in the environment variables.
        """
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not found.")
        
        genai.configure(api_key=api_key)
        
        # Allow the model to be configured via .env, defaulting to a fast and capable model
        model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        self.model = genai.GenerativeModel(model_name)

    def generate(self, cv_content: str, job_description: str) -> str:
        """
        Generates a cover letter using the configured Gemini model.
        """
        # A well-defined prompt structure is key for consistent results from any LLM.
        prompt = f"""
        **Role**: You are an expert career coach and professional writer specializing in crafting compelling cover letters that land interviews. Your tone is professional, confident, and enthusiastic.

        **Task**: Based on the provided CV and Job Description, write a professional and compelling cover letter.

        **Instructions**:
        1.  Address the letter to the "Hiring Manager".
        2.  Create a compelling introduction that grabs the reader's attention.
        3.  In the body of the letter, highlight the most relevant skills and experiences from the CV that directly match the requirements listed in the Job Description. Use specific examples.
        4.  Conclude with a strong closing paragraph that includes a clear call to action.
        5.  Ensure the final output is only the cover letter text, without any additional commentary or preamble.

        ---
        **CV CONTENT**:
        {cv_content}
        ---
        **JOB DESCRIPTION**:
        {job_description}
        ---
        **COVER LETTER**:
        """

        try:
            # Make the API call to generate the content
            response = self.model.generate_content(prompt)
            
            # The response contains the generated text.
            # We add some simple formatting for consistency.
            generated_text = response.text.strip()
            return generated_text.replace('\n\n', '\n').replace('\n', '\n\n')

        except Exception as e:
            # Catch potential API errors (e.g., authentication, network issues)
            print(f"An error occurred with the Google Gemini API: {e}")
            raise ConnectionError("Failed to generate cover letter due to a Google Gemini API error.") from e

