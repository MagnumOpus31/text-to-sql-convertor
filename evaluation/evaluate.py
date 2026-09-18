import json
import os

from evaluation.test_cases import TEST_CASES

from src.sql_generator import generate_sql
from src.sql_validator import validate_sql
from src.database import execute_query


CACHE_FILE = "evaluation/results.json"


def load_cache():
    if not os.path.exists(CACHE_FILE):
        return {}

    with open(CACHE_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_cache(cache):
    with open(CACHE_FILE, "w", encoding="utf-8") as file:
        json.dump(cache, file, indent=4)


def normalize_results(results):
    return sorted([tuple(row) for row in results])


def execute_and_compare(generated_sql, expected_sql):
    try:
        valid, message = validate_sql(generated_sql)

        if not valid:
            return False, f"Validation failed: {message}"

        _, generated_results = execute_query(generated_sql)
        _, expected_results = execute_query(expected_sql)

        generated_results = normalize_results(generated_results)
        expected_results = normalize_results(expected_results)

        if generated_results == expected_results:
            return True, "Correct"

        return False, "Incorrect result"

    except Exception as e:
        return False, f"Execution error: {e}"


def evaluate_baseline():
    cache = load_cache()

    correct = 0
    evaluated = 0
    total = len(TEST_CASES)

    print("\n========== BASELINE ==========")

    for i, test_case in enumerate(TEST_CASES, start=1):

        question = test_case["question"]
        expected_sql = test_case["expected_sql"]

        print(f"\nTest {i}: {question}")

        # Use cached SQL if available
        if question in cache:
            generated_sql = cache[question]

            print("Using cached SQL.")

        else:
            print("Calling local Qwen via Ollama...")

            try:
                generated_sql = generate_sql(question)

                cache[question] = generated_sql
                save_cache(cache)

            except Exception as e:
                print("Ollama error:", e)
                print("Skipping this test.")
                continue

        print("\nGenerated SQL:")
        print(generated_sql)

        is_correct, message = execute_and_compare(
            generated_sql,
            expected_sql
        )

        print("\nResult:", message)

        evaluated += 1

        if is_correct:
            correct += 1

    if evaluated == 0:
        print("\nNo tests were evaluated.")
        return

    accuracy = (correct / evaluated) * 100

    print("\n========== RESULTS ==========")
    print("Correct:", correct)
    print("Evaluated:", evaluated)
    print("Total:", total)
    print("Accuracy:", f"{accuracy:.2f}%")


if __name__ == "__main__":
    evaluate_baseline()