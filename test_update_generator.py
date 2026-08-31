from src.update_generator import generate_update_sql


questions = [
    "Update Rahul's salary to 80000",
    "Change employee 1 department to HR",
    "Update the price of the Laptop to 65000",
    "Change Priya's department to Finance"
]


for question in questions:

    print("\nQuestion:")
    print(question)

    sql = generate_update_sql(question)

    print("\nGenerated SQL:")
    print(sql)