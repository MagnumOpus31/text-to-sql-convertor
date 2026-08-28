import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found in the .env file.")

client = genai.Client(api_key=api_key)


def correct_typos(question):

    prompt = f"""
Correct spelling mistakes in the following user question.

Important rules:
- Only correct obvious spelling mistakes.
- Do not change the meaning of the question.
- Do not rewrite or improve the question.
- Return ONLY the corrected question.
- If there are no spelling mistakes, return the original question unchanged.

User question:
{question}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text.strip()