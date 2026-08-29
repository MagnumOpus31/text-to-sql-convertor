import os

from dotenv import load_dotenv
from google import genai

from src.database import get_database_schema


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found in the .env file.")

client = genai.Client(api_key=api_key)


def check_ambiguity(question):

    # --------------------------------
    # Get current database schema
    # --------------------------------

    schema = get_database_schema()

    schema_text = ""

    for table, columns in schema.items():
        schema_text += f"{table}(\n"
        schema_text += "    " + ", ".join(columns) + "\n"
        schema_text += ")\n"

    # --------------------------------
    # Clarification prompt
    # --------------------------------

    prompt = f"""
You are a clarification engine for a Text-to-SQL system.

Your job is to determine whether the user's question contains
enough information to generate a reliable SQLite SQL query.

Database schema:
{schema_text}

User question:
{question}

Determine whether the question is ambiguous.

If the question is clear, return exactly:

CLEAR

If the question is ambiguous, return a concise clarification
question that asks for the missing information.

Important rules:

1. Use the database schema above to understand what tables
   and columns actually exist.

2. Do NOT claim that a table does not exist if it is present
   in the database schema.

3. Only ask for clarification when the user's request is
   genuinely ambiguous.

4. Do not ask unnecessary clarification questions.

Examples:

User: Show me the top customers
Response:
Would you like to rank the customers by total spending or number of orders?

User: Show me customers from Mumbai
Response:
CLEAR

User: Show me the highest selling products
Response:
Do you want to rank products by total quantity sold or total sales revenue?

User: How many customers do we have?
Response:
CLEAR

User: Show me all employees
Response:
CLEAR

Return ONLY either:

CLEAR

or the clarification question.
"""

    # --------------------------------
    # Call Gemini
    # --------------------------------

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    result = response.text.strip()

    # --------------------------------
    # Process result
    # --------------------------------

    if result == "CLEAR":
        return {
            "ambiguous": False,
            "question": None
        }

    return {
        "ambiguous": True,
        "question": result
    }


def resolve_question(
    original_question,
    clarification_question,
    user_answer
):

    prompt = f"""
You are resolving a user's ambiguous question.

Original question:
{original_question}

Clarification question:
{clarification_question}

User's clarification:
{user_answer}

Rewrite the original question by incorporating the user's
clarification.

The result must be a single, clear natural-language question
that contains all the information needed to generate SQL.

Do not add unnecessary information.

Return ONLY the rewritten question.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text.strip()