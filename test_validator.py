from src.sql_validator import validate_sql


queries = [
    "SELECT * FROM customers;",
    "DELETE FROM customers;",
    "DROP TABLE customers;",
    "UPDATE customers SET city = 'Mumbai';"
]


for query in queries:
    valid, message = validate_sql(query)

    print("\nSQL:", query)
    print("Valid:", valid)
    print("Message:", message)