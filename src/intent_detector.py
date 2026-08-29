import os
from dotenv import load_dotenv
from google import genai
import json

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found in the .env file.")

client = genai.Client(api_key=api_key)


def detect_intent(question):

    prompt = f"""
You are an intent classification system for a natural-language database assistant.

Determine what the user wants to do with the database.

User question:
{question}

Possible intents:

1. READ
   The user only wants to retrieve or view information.

   Examples:
   - Show me all customers
   - How many products are there?
   - Show me customers from Mumbai
   - Which customer spent the most?

2. CREATE_TABLE
   The user explicitly wants to create a new database table.

   Examples:
   - Create a table called employees
   - Create an employees table with id, name and salary
   - Add a new table called departments

Return ONLY valid JSON in this exact format:

{{
    "intent": "READ"
}}

or:

{{
    "intent": "CREATE_TABLE"
}}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    result = response.text.strip()

    # Remove markdown code fences if Gemini adds them
    if result.startswith("```json"):
        result = result[7:]

    if result.startswith("```"):
        result = result[3:]

    if result.endswith("```"):
        result = result[:-3]

    result = result.strip()

    return json.loads(result)