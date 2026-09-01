from src.operation_safety import check_operation_safety


queries = [

    # Safe UPDATE
    """
    UPDATE employees
    SET salary = 80000
    WHERE employee_id = 1;
    """,

    # Safe DELETE
    """
    DELETE FROM employees
    WHERE employee_id = 1;
    """,

    # Dangerous UPDATE - no WHERE
    """
    UPDATE employees
    SET salary = 80000;
    """,

    # Dangerous DELETE - no WHERE
    """
    DELETE FROM employees;
    """,

    # Dangerous - affects everything
    """
    DELETE FROM employees
    WHERE 1=1;
    """,

    # Potentially multiple rows
    """
    DELETE FROM employees
    WHERE department IN ('HR', 'Engineering');
    """,

    # READ - should not require safety check
    """
    SELECT * FROM employees;
    """
]


for sql in queries:

    print("\nSQL:")
    print(sql)

    result = check_operation_safety(sql)

    print("Safe:", result["safe"])
    print("Affected rows:", result["affected_rows"])
    print("Message:", result["message"])