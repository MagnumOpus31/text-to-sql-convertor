import re


def validate_create_table_sql(sql):

    sql = sql.strip()

    # Only allow CREATE TABLE statements
    if not re.match(r"^CREATE\s+TABLE\s+", sql, re.IGNORECASE):
        return False, "Only CREATE TABLE statements are allowed."

    # Block dangerous operations
    forbidden_keywords = [
        "DROP",
        "DELETE",
        "UPDATE",
        "INSERT",
        "ALTER",
        "REPLACE"
    ]

    sql_upper = sql.upper()

    for keyword in forbidden_keywords:
        if re.search(rf"\b{keyword}\b", sql_upper):
            return False, f"Forbidden SQL operation detected: {keyword}"

    # Make sure a table name exists
    match = re.match(
        r"^CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?([A-Za-z_][A-Za-z0-9_]*)",
        sql,
        re.IGNORECASE
    )

    if not match:
        return False, "Could not determine the table name."

    table_name = match.group(1)

    # Prevent creating SQLite internal tables
    if table_name.lower().startswith("sqlite_"):
        return False, "Creating SQLite internal tables is not allowed."

    return True, "CREATE TABLE SQL is valid."