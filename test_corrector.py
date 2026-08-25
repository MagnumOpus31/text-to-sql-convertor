from src.sql_corrector import correct_sql


question = "Show me customers from Mumbai"

bad_sql = """
SELECT * FROM customers
WHERE city_name = 'Mumbai';
"""

error_message = "no such column: city_name"


corrected_sql = correct_sql(
    question,
    bad_sql,
    error_message
)

print("\nOriginal SQL:")
print(bad_sql)

print("\nCorrected SQL:")
print(corrected_sql)