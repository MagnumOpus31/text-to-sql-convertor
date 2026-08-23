from src.sql_generator import generate_sql


question = "Who are the top 5 customers by spending?"

sql = generate_sql(question)

print("\nGenerated SQL:")
print(sql)