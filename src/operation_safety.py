import re

from src.database import get_database_schema


def check_operation_safety(sql):

    sql_clean = sql.strip()
    sql_lower = sql_clean.lower()

    # --------------------------------
    # Only check UPDATE and DELETE
    # --------------------------------

    if not (
        sql_lower.startswith("update")
        or sql_lower.startswith("delete")
    ):
        return {
            "safe": True,
            "affected_rows": None,
            "message": "No row-impact safety check required."
        }

    # --------------------------------
    # UPDATE
    # --------------------------------

    if sql_lower.startswith("update"):

        match = re.search(
            r"\bupdate\s+([a-zA-Z_][a-zA-Z0-9_]*)",
            sql_lower
        )

        if not match:
            return {
                "safe": False,
                "affected_rows": None,
                "message": "Could not determine the target table."
            }

        table_name = match.group(1)

    # --------------------------------
    # DELETE
    # --------------------------------

    else:

        match = re.search(
            r"\bdelete\s+from\s+([a-zA-Z_][a-zA-Z0-9_]*)",
            sql_lower
        )

        if not match:
            return {
                "safe": False,
                "affected_rows": None,
                "message": "Could not determine the target table."
            }

        table_name = match.group(1)

    # --------------------------------
    # Check WHERE clause
    # --------------------------------

    if "where" not in sql_lower:

        return {
            "safe": False,
            "affected_rows": None,
            "message": (
                "DANGEROUS OPERATION: "
                "No WHERE clause was found."
            )
        }

    # --------------------------------
    # Get schema
    # --------------------------------

    schema = get_database_schema()

    if table_name not in schema:

        return {
            "safe": False,
            "affected_rows": None,
            "message": (
                f"Table '{table_name}' does not exist."
            )
        }

    # --------------------------------
    # Extract WHERE condition
    # --------------------------------

    where_match = re.search(
        r"\bwhere\b(.+?)(?:;)?$",
        sql_clean,
        re.IGNORECASE
    )

    if not where_match:

        return {
            "safe": False,
            "affected_rows": None,
            "message": "Could not determine the WHERE condition."
        }

    where_clause = where_match.group(1).strip()

    # --------------------------------
    # Detect obviously broad conditions
    # --------------------------------

    if where_clause.lower() in ["1=1", "true", "'1'='1'"]:

        return {
            "safe": False,
            "affected_rows": None,
            "message": (
                "DANGEROUS OPERATION: "
                "The WHERE condition affects all rows."
            )
        }

    # --------------------------------
    # Basic safety classification
    # --------------------------------

    # Conditions using AND/OR or IN may affect
    # multiple records, so mark them for stronger warning.

    if (
        " or " in where_clause.lower()
        or " in " in where_clause.lower()
    ):

        return {
            "safe": False,
            "affected_rows": None,
            "message": (
                "WARNING: This operation may affect "
                "multiple records."
            )
        }

    # --------------------------------
    # Default
    # --------------------------------

    return {
        "safe": True,
        "affected_rows": None,
        "message": (
            "Operation contains a WHERE clause "
            "and passed the basic safety check."
        )
    }