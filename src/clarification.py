def check_ambiguity(question):
    question = question.lower()

    # Customer ranking ambiguity
    if "top" in question or "best" in question:
        if "customer" in question or "customers" in question:
            return {
                "ambiguous": True,
                "question": (
                    "Would you like to rank customers by "
                    "total spending, number of orders, or another metric?"
                )
            }

    # Product ranking ambiguity
    if "highest" in question or "top" in question:
        if "product" in question or "products" in question:
            return {
                "ambiguous": True,
                "question": (
                    "Would you like to rank products by "
                    "total sales, quantity sold, or another metric?"
                )
            }

    return {
        "ambiguous": False,
        "question": None
    }