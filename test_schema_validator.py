from src.schema_validator import validate_create_table_sql


queries = [

    """
    CREATE TABLE employees (
        employee_id INTEGER PRIMARY KEY,
        name TEXT,
        department TEXT,
        salary REAL
    );
    """,

    """
    CREATE TABLE departments (
        department_id INTEGER PRIMARY KEY,
        department_name TEXT NOT NULL
    );
    """,

    """
    DROP TABLE customers;
    """
]


for sql in queries:

    print("\nSQL:")
    print(sql)

    valid, message = validate_create_table_sql(sql)

    print("Valid:", valid)
    print("Message:", message)