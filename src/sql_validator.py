import sqlite3
from src.database import get_connection


def validate_sql(sql):
    sql = sql.strip().lower()

    if not sql.startswith("select"):
        return False, "Only SELECT queries are allowed."

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

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(sql)

        connection.close()

        return True, "SQL is valid."

    except sqlite3.Error as e:
        return False, str(e)