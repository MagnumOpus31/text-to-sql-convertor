import json
from src.gemini_client import generate_gemini_response




def validate_semantics(question, sql):

    prompt = f"""
You are an expert SQL query evaluator.

Determine whether the SQL query correctly answers the user's question.

User question:
{question}

Generated SQL:
{sql}

Database schema:

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

Return ONLY valid JSON in this exact format:

{{
    "correct": true,
    "reason": "brief explanation"
}}

or:

{{
    "correct": false,
    "reason": "brief explanation"
}}
"""

    response = generate_gemini_response(
        prompt,
        model="gemini-3.6-flash",
    ).strip()

    result = response

    if result.startswith("```json"):
        result = result[7:]

    if result.startswith("```"):
        result = result[3:]

    if result.endswith("```"):
        result = result[:-3]

    return json.loads(result.strip())