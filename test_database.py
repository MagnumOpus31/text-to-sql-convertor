from src.database import get_connection


connection = get_connection()
cursor = connection.cursor()

cursor.execute("""
    SELECT
        c.name,
        SUM(o.total_amount) AS total_spending
    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.name
    ORDER BY total_spending DESC
    LIMIT 5
""")

customers = cursor.fetchall()

for customer in customers:
    print(customer)

connection.close()