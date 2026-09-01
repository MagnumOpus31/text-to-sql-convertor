from src.delete_validator import validate_delete_sql


queries = [

    # Valid
    """
    DELETE FROM employees
    WHERE employee_id = 1;
    """,

    # Valid
    """
    DELETE FROM employees
    WHERE name = 'Rahul';
    """,

    # Valid
    """
    DELETE FROM products
    WHERE category = 'Electronics';
    """,

    # Invalid - no WHERE
    """
    DELETE FROM employees;
    """,

    # Invalid - wrong table
    """
    DELETE FROM unknown_table
    WHERE id = 1;
    """,

    # Invalid - wrong operation
    """
    UPDATE employees
    SET salary = 80000
    WHERE employee_id = 1;
    """
]


for sql in queries:

    valid, message = validate_delete_sql(sql)

    print("\nSQL:")
    print(sql)

    print("Valid:", valid)
    print("Message:", message)