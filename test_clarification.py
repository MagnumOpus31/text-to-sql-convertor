from src.clarification import check_ambiguity


questions = [
    "Show me the top customers",
    "Who are the best customers?",
    "Show me the highest-selling products",
    "Show me customers from Mumbai",
    "Show me all products"
]


for question in questions:
    result = check_ambiguity(question)

    print("\nUser:", question)
    print("Result:", result)