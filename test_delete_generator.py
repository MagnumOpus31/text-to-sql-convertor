from src.delete_generator import generate_delete_sql


questions = [
    "Delete employee 1",
    "Remove Rahul from employees",
    "Delete the employee named Priya",
    "Delete all products in the Electronics category"
]


for question in questions:

    print("\nQuestion:")
    print(question)

    sql = generate_delete_sql(question)

    print("\nGenerated SQL:")
    print(sql)