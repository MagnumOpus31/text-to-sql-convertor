import json
import os

from evaluation.test_cases import TEST_CASES

from src.clarification import check_ambiguity
from src.sql_generator import generate_sql
from src.sql_validator import validate_sql
from src.database import execute_query


SQL_CACHE_FILE = "evaluation/with_clarification.json"
CLARIFICATION_CACHE_FILE = "evaluation/clarification_results.json"


def load_cache(file_path):
    if not os.path.exists(file_path):
        return {}

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_cache(file_path, cache):
    with open(file_path, "w", encoding="utf-8") as file:
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


def evaluate_with_clarification():

    sql_cache = load_cache(SQL_CACHE_FILE)
    clarification_cache = load_cache(CLARIFICATION_CACHE_FILE)

    correct = 0
    evaluated = 0
    total = len(TEST_CASES)

    print("\n========== WITH CLARIFICATION ==========")

    for i, test_case in enumerate(TEST_CASES, start=1):

        question = test_case["question"]
        expected_sql = test_case["expected_sql"]

        print(f"\nTest {i}: {question}")

        # ------------------------------------------------
        # STEP 1: Check clarification cache
        # ------------------------------------------------

        if question in clarification_cache:

            clarification_result = clarification_cache[question]

            print("Using cached clarification result.")

        else:

            print("Calling Gemini for clarification...")

            try:
                clarification_result = check_ambiguity(question)

                clarification_cache[question] = clarification_result

                save_cache(
                    CLARIFICATION_CACHE_FILE,
                    clarification_cache
                )

            except Exception as e:
                print("Gemini clarification error:", e)
                print("Skipping this test.")
                continue

        print("Clarification result:")
        print(clarification_result)

        # ------------------------------------------------
        # STEP 2: Resolve the question
        # ------------------------------------------------

        if clarification_result["ambiguous"]:

            clarification_answer = test_case.get(
                "clarification_answer"
            )

            if not clarification_answer:
                print("No clarification answer provided.")
                continue

            resolved_question = test_case["resolved_question"]

            print("Clarification answer:")
            print(clarification_answer)

            print("Resolved question:")
            print(resolved_question)

        else:

            resolved_question = question

            print("Question is not ambiguous.")

        # ------------------------------------------------
        # STEP 3: Generate SQL
        # ------------------------------------------------

        if resolved_question in sql_cache:

            generated_sql = sql_cache[resolved_question]

            print("\nUsing cached SQL.")

        else:

            print("\nCalling Gemini for SQL generation...")

            try:
                generated_sql = generate_sql(resolved_question)

                sql_cache[resolved_question] = generated_sql

                save_cache(
                    SQL_CACHE_FILE,
                    sql_cache
                )

            except Exception as e:
                print("Gemini SQL generation error:", e)
                print("Skipping this test.")
                continue

        # ------------------------------------------------
        # STEP 4: Evaluate SQL
        # ------------------------------------------------

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

    # ------------------------------------------------
    # FINAL RESULTS
    # ------------------------------------------------

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
    evaluate_with_clarification()