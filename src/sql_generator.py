import os

from dotenv import load_dotenv
from google import genai


# Find and load the .env file
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found in the .env file.")

client = genai.Client(api_key=api_key)


def generate_sql(question):
    print("User question:", question)

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=f"""
You are a SQL expert.

Convert the user's natural language question into a SQLite SQL query.

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

User question:
{question}

Return ONLY the SQL query.
"""
    )

    sql = response.text.strip()

    if sql.startswith("```sql"):
        sql = sql[6:]

    if sql.startswith("```"):   
        sql = sql[3:]

    if sql.endswith("```"):
        sql = sql[:-3]

    return sql.strip()