from src.clarification import check_ambiguity, resolve_question
from src.sql_generator import generate_sql
from src.database import execute_query
from src.sql_corrector import correct_sql
from src.sql_validator import validate_sql
from src.sql_semantic_validator import validate_semantics
from src.typo_corrector import correct_typos


def main():

    # --------------------------------------------------
    # 1. Get user's question
    # --------------------------------------------------

    question = input("Ask a question: ")
    corrected_question=correct_typos(question)

    if corrected_question!=question:
        print("\nCorrected question")
        print(corrected_question)

    question=corrected_question
    clarification=check_ambiguity(question)


    # --------------------------------------------------
    # 2. Check for ambiguity
    # --------------------------------------------------

    clarification = check_ambiguity(question)

    if clarification["ambiguous"]:

        print("\nClarification:", clarification["question"])

        answer = input("\nYour answer: ")

        question = resolve_question(
            question,
            clarification["question"],
            answer
        )


    print("\nResolved question:")
    print(question)


    # --------------------------------------------------
    # 3. Generate SQL
    # --------------------------------------------------

    sql = generate_sql(question)

    print("\nGenerated SQL:")
    print(sql)


    # --------------------------------------------------
    # 4. SQL Validation
    # --------------------------------------------------

    valid, message = validate_sql(sql)

    if not valid:

        print("\nSQL Validation Failed:")
        print(message)

        print("\nAttempting SQL correction...")

        corrected_sql = correct_sql(
            question,
            sql,
            message
        )

        print("\nCorrected SQL:")
        print(corrected_sql)


        # Validate corrected SQL again

        valid, message = validate_sql(corrected_sql)

        print("\nCorrected SQL Validation:")
        print(message)

        if not valid:

            print("Corrected SQL is still invalid.")
            return

        # Use corrected SQL

        sql = corrected_sql

    else:

        print("\nSQL Validation:")
        print(message)


    # --------------------------------------------------
    # 5. Semantic Validation
    # --------------------------------------------------

    semantic_result = validate_semantics(
        question,
        sql
    )

    print("\nSemantic Validation:")
    print(semantic_result)


    # --------------------------------------------------
    # 6. Correct SQL if semantically incorrect
    # --------------------------------------------------

    if not semantic_result["correct"]:

        print("\nSQL is semantically incorrect.")

        print("Reason:")
        print(semantic_result["reason"])

        print("\nAttempting SQL correction...")


        corrected_sql = correct_sql(
            question,
            sql,
            semantic_result["reason"]
        )

        print("\nCorrected SQL:")
        print(corrected_sql)


        # Validate corrected SQL

        valid, message = validate_sql(corrected_sql)

        print("\nCorrected SQL Validation:")
        print(message)

        if not valid:

            print("Corrected SQL is still invalid.")
            return

        # Validate corrected SQL semantically

        corrected_semantic_result=validate_semantics(
            question,
            corrected_sql
        )
        print("\nCorrected SQL Semantic Validation")
        print(corrected_semantic_result)

        if not corrected_semantic_result["correct"]:

            print("\nCorrected SQL is still semantically incorrect.")
            print("Reason:")
            print(corrected_semantic_result["reason"])

            return

        # Everything is valid

        sql = corrected_sql


    # --------------------------------------------------
    # 7. Execute final SQL
    # --------------------------------------------------

    columns, results = execute_query(sql)


    # --------------------------------------------------
    # 8. Display results
    # --------------------------------------------------

    print("\nResults:")

    print(columns)

    for row in results:
        print(row)


# --------------------------------------------------
# Run program
# --------------------------------------------------

if __name__ == "__main__":
    main()