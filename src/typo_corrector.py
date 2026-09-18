from src.ollama_client import generate_ollama_response


def correct_typos(question):

    prompt = f"""
Correct spelling mistakes in the following user question.

Important rules:
- Only correct obvious spelling mistakes.
- Do not change the meaning of the question.
- Do not rewrite or improve the question.
- Return ONLY the corrected question.
- If there are no spelling mistakes, return the original question unchanged.

User question:
{question}
"""

    response = generate_ollama_response(
        prompt,
    ).strip()

