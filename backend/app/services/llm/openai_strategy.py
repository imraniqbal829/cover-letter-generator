import os
from openai import OpenAI
from .base_strategy import LLMStrategy

# Initialize the client specific to this strategy
# This ensures that keys/configs are self-contained
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class OpenAIStrategy(LLMStrategy):
    """Concrete strategy for generating cover letters using the OpenAI API."""

    def generate(self, cv_content: str, job_description: str) -> str:
        system_prompt = (
            "You are an expert career coach and professional writer specializing in crafting "
            "compelling cover letters that land interviews. Your tone is professional, confident, and enthusiastic."
        )

        user_prompt = f"""
        Based on the following CV and Job Description, write a professional and compelling cover letter.
        Tailor the letter to highlight the most relevant skills and experiences from the CV that directly match the job requirements.
        The letter should be addressed to the "Hiring Manager" unless a name is findable.
        Structure your response into three clear parts: an introduction, a body, and a conclusion.

        --- CV CONTENT ---
        {cv_content}

        --- JOB DESCRIPTION ---
        {job_description}
        """

        try:
            response = client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4o"), # Allow model to be configured via .env
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
            )
            
            generated_text = response.choices[0].message.content.strip()
            return generated_text.replace('\n\n', '\n').replace('\n', '\n\n')

        except Exception as e:
            print(f"An error occurred with the OpenAI API: {e}")
            raise ConnectionError("Failed to generate cover letter due to an OpenAI API error.") from e
