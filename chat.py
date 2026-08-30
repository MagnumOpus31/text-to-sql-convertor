from src.clarification import check_ambiguity, resolve_question
from src.sql_generator import generate_sql
from src.database import execute_query, execute_schema_query
from src.sql_corrector import correct_sql
from src.sql_validator import validate_sql
from src.local_typo_corrector import correct_typos
from src.intent_detector import detect_intent
from src.schema_generator import generate_create_table_sql
from src.schema_validator import validate_create_table_sql
from src.insert_generator import generate_insert_sql
from src.insert_validator import validate_insert_sql


def main():

    # ============================================================
    # 1. Get user question
    # ============================================================

    question = input("Ask a question: ")

    # ============================================================
    # 2. Local typo correction
    # ============================================================

    corrected_question = correct_typos(question)

    if corrected_question != question:
        print("\nCorrected question:")
        print(corrected_question)

    question = corrected_question

    # ============================================================
    # 3. Detect intent
    # ============================================================

    intent_result = detect_intent(question)
    intent = intent_result["intent"]

    print("\nDetected intent:")
    print(intent)

    # ============================================================
    # CREATE TABLE PIPELINE
    # ============================================================

    if intent == "CREATE_TABLE":

        print("\nResolved question:")
        print(question)

        print("\nGenerating CREATE TABLE SQL...")

        sql = generate_create_table_sql(question)

        print("\nGenerated SQL:")
        print(sql)

        # --------------------------------------------------------
        # Validate CREATE TABLE SQL
        # --------------------------------------------------------

        valid, message = validate_create_table_sql(sql)

        print("\nSchema Validation:")
        print(message)

        if not valid:
            print("\nCREATE TABLE SQL is invalid.")
            return

        # --------------------------------------------------------
        # Ask for confirmation
        # --------------------------------------------------------

        print("\nWARNING:")
        print("This operation will modify your database.")

        confirmation = input(
            "\nDo you want to execute this SQL? (yes/no): "
        ).strip().lower()

        if confirmation not in ["yes", "y"]:

            print("\nOperation cancelled.")
            return

        # --------------------------------------------------------
        # Execute CREATE TABLE
        # --------------------------------------------------------

        try:

            execute_schema_query(sql)

            print("\nTable created successfully!")

        except Exception as error:

            print("\nDatabase Execution Error:")
            print(error)

        return

    # ============================================================
    # INSERT PIPELINE
    # ============================================================

    if intent == "INSERT":

        print("\nResolved question:")
        print(question)

        print("\nGenerating INSERT SQL...")

        sql = generate_insert_sql(question)

        print("\nGenerated SQL:")
        print(sql)

        # --------------------------------------------------------
        # Validate INSERT SQL
        # --------------------------------------------------------

        valid, message = validate_insert_sql(sql)

        print("\nINSERT Validation:")
        print(message)

        if not valid:

            print("\nINSERT SQL is invalid.")
            return

        # --------------------------------------------------------
        # Ask for confirmation
        # --------------------------------------------------------

        print("\nWARNING:")
        print("This operation will modify your database.")

        confirmation = input(
            "\nDo you want to execute this SQL? (yes/no): "
        ).strip().lower()

        if confirmation not in ["yes", "y"]:

            print("\nOperation cancelled.")
            return

        # --------------------------------------------------------
        # Execute INSERT
        # --------------------------------------------------------

        try:

            execute_schema_query(sql)

            print("\nRecord inserted successfully!")

        except Exception as error:

            print("\nDatabase Execution Error:")
            print(error)

        return

    # ============================================================
    # READ PIPELINE
    # ============================================================

    # ------------------------------------------------------------
    # 4. Clarification
    # ------------------------------------------------------------

    clarification = check_ambiguity(question)

    if clarification["ambiguous"]:

        print("\nClarification:")
        print(clarification["question"])

        answer = input("\nYour answer: ")

        question = resolve_question(
            question,
            clarification["question"],
            answer
        )

    # ------------------------------------------------------------
    # 5. Resolved question
    # ------------------------------------------------------------

    print("\nResolved question:")
    print(question)

    # ------------------------------------------------------------
    # 6. Generate SQL
    # ------------------------------------------------------------

    sql = generate_sql(question)

    print("\nGenerated SQL:")
    print(sql)

    # ------------------------------------------------------------
    # 7. Basic SQL validation
    # ------------------------------------------------------------

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

        valid, message = validate_sql(corrected_sql)

        print("\nCorrected SQL Validation:")
        print(message)

        if not valid:

            print("\nCorrected SQL is still invalid.")
            return

        sql = corrected_sql

    else:

        print("\nSQL Validation:")
        print(message)

    # ============================================================
    # 8. Execute READ query
    # ============================================================

    try:

        columns, results = execute_query(sql)

    except Exception as error:

        print("\nDatabase Execution Error:")
        print(error)

        print("\nAttempting SQL correction...")

        corrected_sql = correct_sql(
            question,
            sql,
            str(error)
        )

        print("\nCorrected SQL:")
        print(corrected_sql)

        # --------------------------------------------------------
        # Validate corrected SQL
        # --------------------------------------------------------

        valid, message = validate_sql(corrected_sql)

        print("\nCorrected SQL Validation:")
        print(message)

        if not valid:

            print("\nCorrected SQL is still invalid.")
            return

        sql = corrected_sql

        # --------------------------------------------------------
        # Try executing corrected SQL
        # --------------------------------------------------------

        try:

            columns, results = execute_query(sql)

        except Exception as error:

            print("\nCorrected SQL execution failed:")
            print(error)
            return

    # ============================================================
    # 9. Display results
    # ============================================================

    print("\nResults:")

    print(columns)

    for row in results:
        print(row)


if __name__ == "__main__":
    main()