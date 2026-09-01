import re

from src.database import get_database_schema


def validate_delete_sql(sql):

    sql_clean = sql.strip()
    sql_lower = sql_clean.lower()

    # --------------------------------
    # Only allow DELETE
    # --------------------------------

    if not sql_lower.startswith("delete"):
        return False, "Only DELETE statements are allowed."

    # --------------------------------
    # Block dangerous operations
    # --------------------------------

    forbidden_keywords = [
        "drop",
        "alter",
        "create",
        "insert",
        "update",
        "replace"
    ]

    for keyword in forbidden_keywords:

        if re.search(r"\b" + keyword + r"\b", sql_lower):

            return False, (
                f"Forbidden SQL operation detected: {keyword}"
            )

    # --------------------------------
    # DELETE must contain FROM
    # --------------------------------

    if "from" not in sql_lower:

        return False, "DELETE statement must contain FROM."

    # --------------------------------
    # WHERE clause is mandatory
    # --------------------------------

    if "where" not in sql_lower:

        return False, (
            "DELETE statements must contain a WHERE clause."
        )

    # --------------------------------
    # Get database schema
    # --------------------------------

    schema = get_database_schema()

    # --------------------------------
    # Extract table name
    # --------------------------------

    match = re.search(
        r"\bdelete\s+from\s+([a-zA-Z_][a-zA-Z0-9_]*)",
        sql_lower
    )

    if not match:

        return False, "Could not determine the target table."

    table_name = match.group(1)

    # --------------------------------
    # Check table exists
    # --------------------------------

    if table_name not in schema:

        return False, (
            f"Table '{table_name}' does not exist "
            "in the database."
        )

    return True, "DELETE SQL is valid."