from src.schema_generator import generate_create_table_sql


questions = [
    "Create a table called employees with employee_id, name, department and salary",
    "Create a table called departments with department_id and department_name"
]


for question in questions:

    print("\nQuestion:")
    print(question)

    sql = generate_create_table_sql(question)

    print("\nGenerated SQL:")
    print(sql)