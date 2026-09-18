import re

from src.ollama_client import generate_ollama_response
from src.database import get_database_schema


def generate_update_sql(question):
    schema = get_database_schema()

    # Build schema text for the LLM
    schema_text = ""

    for table, columns in schema.items():
        schema_text += f"{table}(\n"
        schema_text += "    " + ", ".join(columns) + "\n"
        schema_text += ")\n"

    question_lower = question.lower().strip()

    # ---------------------------------------------------------
    # Handle specific record updates deterministically
    # Example:
    # Update customer 3 city to Mumbai
    # ---------------------------------------------------------

    specific_match = re.match(
        r"^(?:update|change)\s+"
        r"(customer|employee|product|order)\s+"
        r"(\d+)\s+"
        r"(.+)$",
        question.strip(),
        re.IGNORECASE
    )

    if specific_match:
        entity = specific_match.group(1).lower()
        record_id = specific_match.group(2)
        update_request = specific_match.group(3).strip()

        table_map = {
            "customer": ("customers", "customer_id"),
            "employee": ("employees", "employee_id"),
            "product": ("products", "product_id"),
            "order": ("orders", "order_id")
        }

        if entity not in table_map:
            raise ValueError(f"Unsupported entity: {entity}")

        table_name, id_column = table_map[entity]

        # Ask Qwen only for the SET expression.
        prompt = f"""
You are an expert SQLite SQL assistant.

The user wants to update ONE specific record.

Database schema:

{schema_text}

User request:
{question}

Target table:
{table_name}

Target ID column:
{id_column}

Record ID:
{record_id}

Update instruction:
{update_request}

Your task:

Return ONLY the column assignment.

Examples:

Input:
Update customer 3 city to Mumbai

Output:
city = 'Mumbai'

Input:
Update customer 5 name to Rahul

Output:
name = 'Rahul'

Input:
Update product 2 price to 500

Output:
price = 500

Rules:

1. Return ONLY:
   column = value

2. Do NOT return UPDATE.
3. Do NOT return SET.
4. Do NOT return WHERE.
5. Use only columns that exist in the target table.
6. Properly quote TEXT values with single quotes.
7. Keep numeric values unquoted.
8. Do not include explanations.
9. Do not use markdown code fences.

Return ONLY the assignment.
"""

        response = generate_ollama_response(prompt).strip()

        # Remove markdown fences if Qwen accidentally adds them
        response = response.replace("```sql", "").replace("```", "").strip()

        # Remove accidental SET prefix
        response = re.sub(
            r"^\s*set\s+",
            "",
            response,
            flags=re.IGNORECASE
        ).strip()

        # Reject accidental WHERE clause
        if re.search(r"\bwhere\b", response, re.IGNORECASE):
            raise ValueError(
                "The AI generated an unexpected WHERE clause."
            )

        # Make sure we actually received an assignment
        if "=" not in response:
            raise ValueError(
                "The AI could not determine which column should be updated."
            )

        return (
            f"UPDATE {table_name} "
            f"SET {response} "
            f"WHERE {id_column} = {record_id};"
        )

    # ---------------------------------------------------------
    # General UPDATE handling
    # ---------------------------------------------------------

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
4. Do not invent tables or columns.
5. Generate only UPDATE statements.
6. Use valid SQLite syntax.
7. Properly quote TEXT values using single quotes.
8. ALWAYS include a WHERE clause.
9. NEVER generate UPDATE without a WHERE clause.
10. Do not update records that the user did not ask to update.
11. Do not include explanations.
12. Do not use WHERE 1, WHERE 1=1, TRUE, or another condition
    that intentionally affects every row.
13. If the user explicitly asks to update ALL records, generate
    a condition that will be rejected by the safety checker.

Return ONLY the SQL query.
"""

    response = generate_ollama_response(prompt).strip()

    # Remove markdown fences
    if response.startswith("```sql"):
        response = response[6:]
    elif response.startswith("```"):
        response = response[3:]

    if response.endswith("```"):
        response = response[:-3]

    response = response.strip()

    # Prevent accidental duplicate SET
    response = re.sub(
        r"\bSET\s+SET\b",
        "SET",
        response,
        flags=re.IGNORECASE
    )

    return response