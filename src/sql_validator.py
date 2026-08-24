def validate_sql(sql):
    sql = sql.strip().lower()

    # Only allow SELECT queries
    if not sql.startswith("select"):
        return False, "Only SELECT queries are allowed."

    # Block dangerous SQL operations
    forbidden_keywords = [
        "insert",
        "update",
        "delete",
        "drop",
        "alter",
        "create",
        "replace"
    ]

    for keyword in forbidden_keywords:
        if keyword in sql:
            return False, f"Forbidden SQL operation detected: {keyword}"

    return True, "SQL is valid."