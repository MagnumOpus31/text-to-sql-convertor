import os

from dotenv import load_dotenv
from google import genai

from src.database import get_database_schema


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found in the .env file.")

client = genai.Client(api_key=api_key)


def generate_sql(question):

    print("User question:", question)

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
    # SQL generation prompt
    # --------------------------------

    prompt = f"""
You are an expert SQLite SQL generator.

Convert the user's natural-language question into a valid
SQLite SQL query.

Current database schema:
{schema_text}

User question:
{question}

Rules:

1. Generate ONLY the SQL query.
2. Do not use markdown code fences.
3. Use only tables and columns that exist in the database schema.
4. Do not invent table names or column names.
5. Use SQLite-compatible SQL.
6. For SELECT requests, generate only SELECT statements.
7. Use appropriate JOINs when information from multiple tables
   is required.
8. Use proper SQL syntax and quote string values correctly.
9. Do not include explanations.

Examples:

User:
Show me all customers

SQL:
SELECT * FROM customers;

User:
Show me customers from Mumbai

SQL:
SELECT * FROM customers WHERE city = 'Mumbai';

User:
How many customers do we have?

SQL:
SELECT COUNT(*) FROM customers;

User:
Show me all employees

SQL:
SELECT * FROM employees;

User:
How many employees are there?

SQL:
SELECT COUNT(*) FROM employees;

Return ONLY the SQL query.
"""

    # --------------------------------
    # Call Gemini
    # --------------------------------

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    sql = response.text.strip()

    # --------------------------------
    # Remove markdown code fences
    # --------------------------------

    if sql.startswith("```sql"):
        sql = sql[6:]

    elif sql.startswith("```"):
        sql = sql[3:]

    if sql.endswith("```"):
        sql = sql[:-3]

    return sql.strip()