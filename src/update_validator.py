import re

from src.database import get_database_schema


def validate_update_sql(sql):

    sql_clean = sql.strip()

    sql_lower = sql_clean.lower()

    # --------------------------------
    # Only allow UPDATE
    # --------------------------------

    if not sql_lower.startswith("update"):
        return False, "Only UPDATE statements are allowed."

    # --------------------------------
    # Block dangerous operations
    # --------------------------------

    forbidden_keywords = [
        "drop",
        "alter",
        "create",
        "delete",
        "insert",
        "replace"
    ]

    for keyword in forbidden_keywords:

        if re.search(r"\b" + keyword + r"\b", sql_lower):

            return False, (
                f"Forbidden SQL operation detected: {keyword}"
            )

    # --------------------------------
    # Check UPDATE structure
    # --------------------------------

    if "set" not in sql_lower:

        return False, "UPDATE statement must contain SET."

    # --------------------------------
    # WHERE clause is mandatory
    # --------------------------------

    if "where" not in sql_lower:

        return False, (
            "UPDATE statements must contain a WHERE clause."
        )

    # --------------------------------
    # Get current database schema
    # --------------------------------

    schema = get_database_schema()

    # --------------------------------
    # Extract table name
    # --------------------------------

    try:

        after_update = sql_clean.split(None, 1)[1]

        table_name = after_update.split(None, 1)[0].strip()

        table_name = table_name.lower()

    except Exception:

        return False, "Could not determine the target table."

    # --------------------------------
    # Check table exists
    # --------------------------------

    if table_name not in schema:

        return False, (
            f"Table '{table_name}' does not exist "
            "in the database."
        )

    # --------------------------------
    # Extract SET section
    # --------------------------------

    try:

        set_section = re.split(
            r"\bwhere\b",
            sql_lower,
            maxsplit=1
        )[0]

        set_section = set_section.split("set", 1)[1]

    except Exception:

        return False, "Could not determine columns being updated."

    # --------------------------------
    # Extract updated columns
    # --------------------------------

    assignments = set_section.split(",")

    valid_columns = [
        column.lower()
        for column in schema[table_name]
    ]

    for assignment in assignments:

        if "=" not in assignment:

            return False, (
                "Invalid SET clause."
            )

        column = assignment.split("=", 1)[0].strip()

        if column not in valid_columns:

            return False, (
                f"Column '{column}' does not exist "
                f"in table '{table_name}'."
            )

    return True, "UPDATE SQL is valid."