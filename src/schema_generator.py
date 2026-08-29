import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found in the .env file.")

client = genai.Client(api_key=api_key)


def generate_create_table_sql(question):

    prompt = f"""
You are an expert SQLite database engineer.

Convert the user's request into a CREATE TABLE SQL statement.

User request:
{question}

Rules:

1. Generate ONLY a CREATE TABLE statement.
2. Always use CREATE TABLE IF NOT EXISTS.
3. Use SQLite-compatible SQL.
4. Do not generate INSERT, UPDATE, DELETE, DROP or ALTER statements.
5. Infer appropriate SQLite data types.
6. If the user provides an id column, make it INTEGER PRIMARY KEY when appropriate.
7. Do not use markdown code fences.
8. Do not include explanations.

Return only the SQL statement.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    sql = response.text.strip()

    # Remove markdown fences if Gemini adds them
    if sql.startswith("```sql"):
        sql = sql[6:]

    if sql.startswith("```"):
        sql = sql[3:]

    if sql.endswith("```"):
        sql = sql[:-3]

    return sql.strip()