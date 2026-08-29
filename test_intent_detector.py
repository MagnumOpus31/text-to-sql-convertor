from src.intent_detector import detect_intent


questions = [
    "Show me all customers",
    "How many products are there?",
    "Show me customers from Mumbai",
    "Which customer spent the most?",
    "Create a table called employees",
    "Create an employees table with id, name and salary"
]


for question in questions:

    print("\nQuestion:", question)

    result = detect_intent(question)

    print("Intent:", result["intent"])