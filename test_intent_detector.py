from src.intent_detector import detect_intent


questions = [
    # READ
    "Show me all customers",
    "How many products are there?",
    "Show me customers from Mumbai",
    "Which customer spent the most?",

    # CREATE_TABLE
    "Create a table called employees",
    "Create an employees table with id, name and salary",

    # INSERT
    "Add Rahul to employees with employee_id 1 and salary 75000",
    "Insert a new employee named Priya into employees",

    # UPDATE
    "Update Rahul's salary to 80000",
    "Change employee 1 department to HR",
    "Update the price of the Laptop to 65000"
]


for question in questions:

    print("\nQuestion:", question)

    result = detect_intent(question)

    print("Intent:", result["intent"])