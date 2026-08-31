from src.update_validator import validate_update_sql


queries = [

    # Valid
    """
    UPDATE employees
    SET salary = 80000
    WHERE employee_id = 1;
    """,

    # Valid
    """
    UPDATE employees
    SET department = 'HR'
    WHERE name = 'Rahul';
    """,

    # Invalid - no WHERE
    """
    UPDATE employees
    SET salary = 80000;
    """,

    # Invalid - wrong column
    """
    UPDATE employees
    SET salary_amount = 80000
    WHERE employee_id = 1;
    """,

    # Invalid - wrong table
    """
    UPDATE unknown_table
    SET salary = 80000
    WHERE id = 1;
    """
]


for sql in queries:

    valid, message = validate_update_sql(sql)

    print("\nSQL:")
    print(sql)

    print("Valid:", valid)
    print("Message:", message)