TEST_CASES = [
    {
        "question": "Show me all customers",
        "ambiguous": False,
        "resolved_question": "Show me all customers",
        "expected_sql": "SELECT * FROM customers;"
    },

    {
        "question": "Show me customers from Mumbai",
        "ambiguous": False,
        "resolved_question": "Show me customers from Mumbai",
        "expected_sql": "SELECT * FROM customers WHERE city = 'Mumbai';"
    },

    {
        "question": "How many customers do we have?",
        "ambiguous": False,
        "resolved_question": "How many customers do we have?",
        "expected_sql": "SELECT COUNT(*) FROM customers;"
    },

    {
        "question": "Show me all products",
        "ambiguous": False,
        "resolved_question": "Show me all products",
        "expected_sql": "SELECT * FROM products;"
    },

    {
        "question": "Show me the top customers",
        "ambiguous": True,
        "clarification_answer": "total spending",
        "resolved_question": "Show me the top customers ranked by total spending.",
        "expected_sql": """
            SELECT c.customer_id, c.name, SUM(o.total_amount) AS total_spending
            FROM customers c
            JOIN orders o ON c.customer_id = o.customer_id
            GROUP BY c.customer_id, c.name
            ORDER BY total_spending DESC
            LIMIT 5;
        """
    },

    {
        "question": "Show me the highest selling products",
        "ambiguous": True,
        "clarification_answer": "total sales revenue",
        "resolved_question": "Show me the products ranked by total sales revenue.",
        "expected_sql": """
            SELECT p.product_id, p.product_name,
                   SUM(oi.quantity * oi.unit_price) AS total_sales
            FROM products p
            JOIN order_items oi ON p.product_id = oi.product_id
            GROUP BY p.product_id, p.product_name
            ORDER BY total_sales DESC;
        """
    },

    {
        "question": "Show me sales",
        "ambiguous": True,
        "clarification_answer": "total sales revenue",
        "resolved_question": "Show me total sales revenue.",
        "expected_sql": """
            SELECT SUM(total_amount) AS total_sales
            FROM orders;
        """
    },

    {
        "question": "Which customer spent the most?",
        "ambiguous": False,
        "resolved_question": "Which customer spent the most?",
        "expected_sql": """
            SELECT c.customer_id, c.name,
                   SUM(o.total_amount) AS total_spending
            FROM customers c
            JOIN orders o ON c.customer_id = o.customer_id
            GROUP BY c.customer_id, c.name
            ORDER BY total_spending DESC
            LIMIT 1;
        """
    },

    {
        "question": "How many products are there?",
        "ambiguous": False,
        "resolved_question": "How many products are there?",
        "expected_sql": "SELECT COUNT(*) FROM products;"
    },

    {
        "question": "Show products in the electronics category",
        "ambiguous": False,
        "resolved_question": "Show products in the electronics category.",
        "expected_sql": """
            SELECT *
            FROM products
            WHERE category = 'electronics';
        """
    }
]