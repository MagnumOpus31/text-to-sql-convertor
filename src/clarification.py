from src.ollama_client import generate_ollama_response


def check_ambiguity(question):
    question_lower = question.lower().strip()

    # ---------------------------------------------------------
    # UPDATE requests
    # ---------------------------------------------------------
    # A request such as:
    # "Update customer 3"
    #
    # identifies the record but does NOT specify what to change.
    # Therefore clarification is required.
    #
    # A request such as:
    # "Update customer 3 city to Mumbai"
    #
    # contains both the record and the requested modification,
    # so it is clear.
    # ---------------------------------------------------------

    update_specific_match = None

    update_specific_patterns = [
        r"^(?:update|change)\s+"
        r"(customer|employee|product|order)\s+"
        r"(\d+)(?:\s+(.*))?$"
    ]

    import re

    for pattern in update_specific_patterns:
        update_specific_match = re.match(
            pattern,
            question_lower,
            re.IGNORECASE
        )

        if update_specific_match:
            break

    if update_specific_match:
        entity = update_specific_match.group(1)
        record_id = update_specific_match.group(2)
        update_details = update_specific_match.group(3)

        # No field/value was provided.
        if not update_details or not update_details.strip():
            return {
                "ambiguous": True,
                "question": (
                    f"What would you like to update for "
                    f"{entity} {record_id}?"
                )
            }

        # An update instruction was provided.
        return {
            "ambiguous": False,
            "question": None
        }

    # ---------------------------------------------------------
    # Specific DELETE requests
    # ---------------------------------------------------------

    specific_delete_patterns = [
        "delete customer ",
        "delete employee ",
        "delete product ",
        "delete order ",
        "remove customer ",
        "remove employee ",
        "remove product ",
        "remove order "
    ]

    if any(
        question_lower.startswith(pattern)
        for pattern in specific_delete_patterns
    ):
        return {
            "ambiguous": False,
            "question": None
        }

    # ---------------------------------------------------------
    # Explicit ALL operations
    # ---------------------------------------------------------

    explicit_scope_patterns = [
        "delete all ",
        "delete every ",
        "remove all ",
        "remove every ",
        "update all ",
        "update every "
    ]

    if any(
        pattern in question_lower
        for pattern in explicit_scope_patterns
    ):
        return {
            "ambiguous": False,
            "question": None
        }

    # ---------------------------------------------------------
    # Clear read queries
    # ---------------------------------------------------------

    clear_read_patterns = [
        "show me all ",
        "show all ",
        "list all ",
        "list ",
        "show ",
        "get all ",
        "get ",
        "find all ",
        "find "
    ]

    ranking_indicators = [
        "top ",
        "highest ",
        "lowest ",
        "best ",
        "worst "
    ]

    ranking_metrics = [
        "total spending",
        "total sales",
        "number of orders",
        "orders",
        "revenue",
        "quantity sold",
        "total quantity",
        "price",
        "salary"
    ]

    has_read_pattern = any(
        question_lower.startswith(pattern)
        for pattern in clear_read_patterns
    )

    has_ranking = any(
        indicator in question_lower
        for indicator in ranking_indicators
    )

    has_metric = any(
        metric in question_lower
        for metric in ranking_metrics
    )

    if has_read_pattern and has_ranking and has_metric:
        return {
            "ambiguous": False,
            "question": None
        }

    # ---------------------------------------------------------
    # Clear filtered read queries
    # ---------------------------------------------------------

    filter_indicators = [
        "from ",
        "where ",
        "in ",
        "with ",
        "whose ",
        "having "
    ]

    if has_read_pattern and any(
        indicator in question_lower
        for indicator in filter_indicators
    ):
        return {
            "ambiguous": False,
            "question": None
        }

    # ---------------------------------------------------------
    # LLM-based ambiguity detection
    # ---------------------------------------------------------

    prompt = f"""
You are an SQL query clarification assistant.

Determine whether the user's question is ambiguous or whether there is
enough information to generate SQL.

User question:
{question}

Rules:

1. Return exactly CLEAR if the question is specific enough to generate SQL.
2. If clarification is genuinely required, return ONLY one concise
   clarification question.
3. Do not rewrite or repeat the user's question.
4. Do not ask for confirmation.
5. Do not treat DELETE, UPDATE, INSERT, or CREATE TABLE as ambiguous
   merely because they modify the database.
6. If the user explicitly specifies "all", "every", or an equivalent
   phrase, the scope is clear.
7. "Delete all customers" is CLEAR.
8. "Delete customer 3" is CLEAR.
9. "Delete Rahul from employees" is CLEAR.
10. "Update customer 3" is NOT clear because the user has not specified
    what should be changed.
11. For "Update customer 3", ask:
    What would you like to update for customer 3?
12. "Update customer 3 city to Mumbai" is CLEAR.
13. "Show me all customers" is CLEAR.
14. "Show me customers from Mumbai" is CLEAR.
15. "Show me the top 3 customers by total spending" is CLEAR.
16. "Show me the top 5 products by quantity sold" is CLEAR.
17. "Show me the top customers" is ambiguous because the ranking
    metric is not specified.
18. "Show me sales" may require clarification if the requested metric
    or grouping is unclear.

Return ONLY:

CLEAR

or one concise clarification question.
"""

    result = generate_ollama_response(prompt).strip()

    normalized = result.upper()

    clear_indicators = [
        "CLEAR",
        "IS CLEAR",
        "ENOUGH INFORMATION",
        "ENOUGH INFORMATION TO GENERATE",
        "NO CLARIFICATION",
        "NO NEED FOR CLARIFICATION"
    ]

    if any(
        indicator in normalized
        for indicator in clear_indicators
    ):
        return {
            "ambiguous": False,
            "question": None
        }

    return {
        "ambiguous": True,
        "question": result
    }


def resolve_question(question):
    return check_ambiguity(question)