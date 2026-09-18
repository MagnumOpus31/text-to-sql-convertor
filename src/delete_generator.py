from src.ollama_client import generate_ollama_response
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
12. If the user asks to delete ALL records, do NOT use a condition such as WHERE 1, WHERE 1=1, or another condition that matches every row.
13. For requests to delete ALL records, generate a condition that will be rejected by the safety checker rather than attempting to bypass it.

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

    response = generate_ollama_response(prompt).strip()

    # Remove markdown code fences if the model adds them
    if response.startswith("```sql"):
        response = response[6:]

    elif response.startswith("```"):
        response = response[3:]

    if response.endswith("```"):
        response = response[:-3]

    return response.strip()