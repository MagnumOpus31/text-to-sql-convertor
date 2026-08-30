from src.insert_validator import validate_insert_sql


queries = [

    """
    INSERT INTO employees
    (employee_id, name, department, salary)
    VALUES (1, 'Rahul', 'Engineering', 75000);
    """,

    """
    INSERT INTO employees
    (employee_id, name, department, salary)
    VALUES (2, 'Priya', 'HR', 60000);
    """,

    """
    INSERT INTO employees
    (employee_id, wrong_column, salary)
    VALUES (3, 'Test', 50000);
    """,

    """
    INSERT INTO unknown_table
    (id, name)
    VALUES (1, 'Test');
    """
]


for sql in queries:

    valid, message = validate_insert_sql(sql)

    print("\nSQL:")
    print(sql)

    print("Valid:", valid)
    print("Message:", message)