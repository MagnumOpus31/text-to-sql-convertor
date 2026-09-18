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
    # Get database schema
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
    where_lower = where_clause.lower()

    # --------------------------------
    # Detect conditions affecting all rows
    # --------------------------------

    # Examples:
    # WHERE 1
    # WHERE TRUE
    # WHERE 1=1
    # WHERE 1 = 1
    # WHERE TRUE = TRUE
    # WHERE '1'='1'

    normalized_where = re.sub(r"\s+", "", where_lower)

    if normalized_where in [
        "1",
        "true",
        "1=1",
        "true=true",
        "'1'='1'"
    ]:

        return {
            "safe": False,
            "affected_rows": None,
            "message": (
                "DANGEROUS OPERATION: "
                "The WHERE condition affects all rows."
            )
        }

    # --------------------------------
    # Block subqueries
    # --------------------------------

    if re.search(r"\bselect\b", where_lower):

        return {
            "safe": False,
            "affected_rows": None,
            "message": (
                "DANGEROUS OPERATION: "
                "Subqueries in UPDATE/DELETE conditions "
                "are not allowed because they may affect "
                "multiple records."
            )
        }

    # --------------------------------
    # Block OR conditions
    # --------------------------------

    if re.search(r"\bor\b", where_lower):

        return {
            "safe": False,
            "affected_rows": None,
            "message": (
                "WARNING: This operation may affect "
                "multiple records because it contains OR."
            )
        }

    # --------------------------------
    # Block IN conditions
    # --------------------------------

    if re.search(r"\bin\s*\(", where_lower):

        return {
            "safe": False,
            "affected_rows": None,
            "message": (
                "WARNING: This operation may affect "
                "multiple records because it contains IN."
            )
        }

    # --------------------------------
    # Block BETWEEN conditions
    # --------------------------------

    if re.search(r"\bbetween\b", where_lower):

        return {
            "safe": False,
            "affected_rows": None,
            "message": (
                "WARNING: This operation may affect "
                "multiple records because it contains BETWEEN."
            )
        }

    # --------------------------------
    # Default: condition appears specific
    # --------------------------------

    return {
        "safe": True,
        "affected_rows": None,
        "message": (
            "Operation contains a WHERE clause "
            "and passed the basic safety check."
        )
    }