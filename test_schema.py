from src.database import get_database_schema

schema = get_database_schema()

print("Current database schema:")

for table, columns in schema.items():
    print(f"\n{table}:")
    print(columns)