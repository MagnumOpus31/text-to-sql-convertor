import os

from dotenv import load_dotenv
from google import genai


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found in the .env file.")

client = genai.Client(api_key=api_key)


def check_ambiguity(question):
    schema = """
    customers(
        customer_id,
        name,
        city
    )

    orders(
        order_id,
        customer_id,
        order_date,
        total_amount
    )

    products(
        product_id,
        product_name,
        category,
        price
    )

    order_items(
        order_id,
        product_id,
        quantity,
        unit_price
    )
    """

    prompt = f"""
You are a clarification engine for a Text-to-SQL system.

Your job is to determine whether the user's question contains
enough information to generate a reliable SQLite SQL query.

Database schema:
{schema}

User question:
{question}

Determine whether the question is ambiguous.

If the question is clear, return exactly:

CLEAR

If the question is ambiguous, return a concise clarification
question that asks for the missing information.

Examples:

User: Show me the top customers
Response:
Would you like to rank the customers by total spending or number of orders?

User: Show me customers from Mumbai
Response:
CLEAR

User: Show me the highest selling products
Response:
Do you want to rank products by quantity sold or total sales revenue?

User: How many customers do we have?
Response:
CLEAR

Return ONLY either:
CLEAR

or the clarification question.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    result = response.text.strip()

    if result == "CLEAR":
        return {
            "ambiguous": False,
            "question": None
        }

    return {
        "ambiguous": True,
        "question": result
    }
def resolve_question(original_question, clarification_question, user_answer):
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

Return ONLY the rewritten question.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text.strip()