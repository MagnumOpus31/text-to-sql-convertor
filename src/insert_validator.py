from src.database import get_database_schema


def validate_insert_sql(sql):

    sql_clean = sql.strip()

    # --------------------------------
    # Only allow INSERT
    # --------------------------------

    if not sql_clean.lower().startswith("insert"):
        return False, "Only INSERT statements are allowed."

    # --------------------------------
    # Block dangerous operations
    # --------------------------------

    forbidden_keywords = [
        "drop",
        "alter",
        "create",
        "delete",
        "update",
        "replace"
    ]

    sql_lower = sql_clean.lower()

    for keyword in forbidden_keywords:

        if keyword in sql_lower:
            return False, f"Forbidden SQL operation detected: {keyword}"

    # --------------------------------
    # Basic INSERT structure
    # --------------------------------

    if "into" not in sql_lower:
        return False, "INSERT statement must contain INTO."

    if "values" not in sql_lower:
        return False, "INSERT statement must contain VALUES."

    # --------------------------------
    # Get current database schema
    # --------------------------------

    schema = get_database_schema()

    # --------------------------------
    # Extract table name
    # --------------------------------

    try:

        after_into = sql_lower.split("into", 1)[1].strip()

        table_name = after_into.split("(", 1)[0].strip()

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
    # Extract column list
    # --------------------------------

    try:

        columns_part = after_into.split("(", 1)[1]
        columns_part = columns_part.split(")", 1)[0]

        columns = [
            column.strip()
            for column in columns_part.split(",")
        ]

    except Exception:

        return False, "Could not determine INSERT columns."

    # --------------------------------
    # Check columns exist
    # --------------------------------

    valid_columns = [
        column.lower()
        for column in schema[table_name]
    ]

    for column in columns:

        if column.lower() not in valid_columns:

            return False, (
                f"Column '{column}' does not exist "
                f"in table '{table_name}'."
            )

    return True, "INSERT SQL is valid."