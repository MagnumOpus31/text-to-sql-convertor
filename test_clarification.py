from src.clarification import check_ambiguity


questions = [
    "Show me the top customers",
    "Show me customers from Mumbai",
    "How many customers do we have?",
    "Show me the highest selling products",
    "Show me sales",
    "Show me all products",
    "Which customer spent the most?"
]


for question in questions:
    result = check_ambiguity(question)

    print("\nUser:", question)
    print("Result:", result)