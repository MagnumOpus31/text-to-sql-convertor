import difflib
import re


VOCABULARY = [
    "customers",
    "customer",
    "orders",
    "order",
    "products",
    "product",
    "order_items",
    "Mumbai",
    "Pune",
    "Delhi",
    "Bangalore",
    "Electronics",
    "Fashion",
    "sales",
    "spending",
    "revenue",
    "quantity",
    "price",
    "category",
    "city"
]


def correct_typos(question):

    words = re.findall(r"\b[\w]+\b", question)

    corrected_question = question

    for word in words:

        # Don't modify short words
        if len(word) < 4:
            continue

        matches = difflib.get_close_matches(
            word,
            VOCABULARY,
            n=1,
            cutoff=0.80
        )

        if matches:
            corrected_word = matches[0]

            # Preserve capitalization style
            if word.isupper():
                corrected_word = corrected_word.upper()
            elif word[0].isupper():
                corrected_word = corrected_word.capitalize()

            corrected_question = re.sub(
                rf"\b{re.escape(word)}\b",
                corrected_word,
                corrected_question
            )

    return corrected_question