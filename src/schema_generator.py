from src.ollama_client import generate_ollama_response

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

    response = generate_ollama_response(
        prompt,
    ).strip()


    # Remove markdown fences if Ollama adds them
    if sql.startswith("```sql"):
        sql = sql[6:]

    if sql.startswith("```"):
        sql = sql[3:]

    if sql.endswith("```"):
        sql = sql[:-3]

    return sql.strip()