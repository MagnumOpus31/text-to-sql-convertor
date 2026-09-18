from src.ollama_client import generate_ollama_response



def correct_sql(question, sql, error_message):

    prompt = f"""
You are an expert SQL debugger.

The user asked:

{question}

The generated SQL was:

{sql}

The SQL produced this error:

{error_message}

Correct the SQL query.

Database schema:

customers(
    customer_id,
    name,
    city
)

orders(
    order_id,
    customer_id,
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

Return ONLY the corrected SQL query.
Do not use markdown.
Do not explain anything.
"""

    response = generate_ollama_response(
        prompt,
    ).strip()


    if sql.startswith("```sql"):
        sql = sql[6:]

    if sql.startswith("```"):
        sql = sql[3:]

    if sql.endswith("```"):
        sql = sql[:-3]

    return sql.strip()