from src.typo_corrector import correct_typos


test_questions = [
    "Show me custmoers from Mubmai",
    "Show me all custmers",
    "Show me all prodcts",
    "Show me all ordres",
    "Show me customers from Mumbai"
]


for question in test_questions:

    corrected = correct_typos(question)

    print("\nOriginal :", question)
    print("Corrected:", corrected)