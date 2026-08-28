from src.sql_semantic_validator import validate_semantics


question = "Show me customers from Mumbai"

sql = """
SELECT * FROM customers
WHERE city_name = 'Mumbai';
"""


result = validate_semantics(question, sql)

print("\nQuestion:")
print(question)

print("\nSQL:")
print(sql)

print("\nSemantic Validation:")
print(result)