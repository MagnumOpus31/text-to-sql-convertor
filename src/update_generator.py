from src.gemini_client import generate_gemini_response

from src.database import get_database_schema


def generate_update_sql(question):

    schema = get_database_schema()

    schema_text = ""

    for table, columns in schema.items():

        schema_text += f"{table}(\n"
        schema_text += "    " + ", ".join(columns) + "\n"
        schema_text += ")\n"

    prompt = f"""
You are an expert SQLite SQL generator.

Generate an UPDATE statement based on the user's request.

Current database schema:

{schema_text}

User question:
{question}

Rules:

1. Generate ONLY the SQL query.
2. Do not use markdown code fences.
3. Use only tables and columns that exist in the schema.
4. Do not invent columns.
5. Generate only UPDATE statements.
6. Use valid SQLite syntax.
7. Properly quote TEXT values using single quotes.
8. Always include a WHERE clause.
9. Never generate an UPDATE statement without a WHERE clause.
10. Do not modify columns that the user did not ask to modify.
11. Do not include explanations.

Return ONLY the SQL query.
"""

    response = generate_gemini_response(
        prompt,
        model="gemini-3.6-flash"
    ).strip()


    if sql.startswith("```sql"):
        sql = sql[6:]

    elif sql.startswith("```"):
        sql = sql[3:]

    if sql.endswith("```"):
        sql = sql[:-3]

    return sql.strip()