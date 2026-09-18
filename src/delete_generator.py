from src.gemini_client import generate_gemini_response

from src.database import get_database_schema





def generate_delete_sql(question):

    schema = get_database_schema()

    schema_text = ""

    for table, columns in schema.items():

        schema_text += f"{table}(\n"
        schema_text += "    " + ", ".join(columns) + "\n"
        schema_text += ")\n"

    prompt = f"""
You are an expert SQLite SQL generator.

Generate a DELETE statement based on the user's request.

Current database schema:

{schema_text}

User question:
{question}

Rules:

1. Generate ONLY the SQL query.
2. Do not use markdown code fences.
3. Use only tables and columns that exist in the schema.
4. Do not invent tables or columns.
5. Generate only DELETE statements.
6. Use valid SQLite syntax.
7. Properly quote TEXT values using single quotes.
8. ALWAYS include a WHERE clause.
9. NEVER generate DELETE without a WHERE clause.
10. Do not delete records that the user did not ask to delete.
11. Do not include explanations.

Examples:

User:
Delete employee 1

SQL:
DELETE FROM employees WHERE employee_id = 1;

User:
Remove Rahul from employees

SQL:
DELETE FROM employees WHERE name = 'Rahul';

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