from src.insert_generator import generate_insert_sql


questions = [
    "Add an employee named Rahul with employee_id 1, department Engineering and salary 75000",
    "Add an employee named Priya with employee_id 2, department HR and salary 60000"
]


for question in questions:

    print("\nQuestion:")
    print(question)

    sql = generate_insert_sql(question)

    print("\nGenerated SQL:")
    print(sql)