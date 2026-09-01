from src.clarification import check_ambiguity, resolve_question
from src.sql_generator import generate_sql
from src.database import execute_query, execute_write_query
from src.sql_corrector import correct_sql
from src.sql_validator import validate_sql
from src.sql_semantic_validator import validate_semantics
from src.local_typo_corrector import correct_typos
from src.intent_detector import detect_intent

from src.schema_generator import generate_create_table_sql
from src.schema_validator import validate_create_table_sql

from src.insert_generator import generate_insert_sql
from src.insert_validator import validate_insert_sql

from src.update_generator import generate_update_sql
from src.update_validator import validate_update_sql

from src.delete_generator import generate_delete_sql
from src.delete_validator import validate_delete_sql

from src.operation_safety import check_operation_safety


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
    # 4. Clarification
    # ============================================================

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

    # ============================================================
    # 5. Resolved question
    # ============================================================

    print("\nResolved question:")
    print(question)

    # ============================================================
    # CREATE TABLE PIPELINE
    # ============================================================

    if intent == "CREATE_TABLE":

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
        # Confirmation
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

            execute_write_query(sql)

            print("\nTable created successfully!")

        except Exception as error:

            print("\nDatabase Execution Error:")
            print(error)

        return

    # ============================================================
    # INSERT PIPELINE
    # ============================================================

    if intent == "INSERT":

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
        # Confirmation
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

            execute_write_query(sql)

            print("\nRecord inserted successfully!")

        except Exception as error:

            print("\nDatabase Execution Error:")
            print(error)

        return

    # ============================================================
    # UPDATE PIPELINE
    # ============================================================

    if intent == "UPDATE":

        print("\nGenerating UPDATE SQL...")

        sql = generate_update_sql(question)

        print("\nGenerated SQL:")
        print(sql)

        # --------------------------------------------------------
        # Validate UPDATE SQL
        # --------------------------------------------------------

        valid, message = validate_update_sql(sql)

        print("\nUPDATE Validation:")
        print(message)

        if not valid:

            print("\nUPDATE SQL is invalid.")
            return

        # --------------------------------------------------------
        # Operation Safety Check
        # --------------------------------------------------------

        safety_result = check_operation_safety(sql)

        print("\nOperation Safety:")
        print(safety_result["message"])

        if not safety_result["safe"]:

            print("\nOperation blocked for safety.")
            return

        # --------------------------------------------------------
        # Confirmation
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
        # Execute UPDATE
        # --------------------------------------------------------

        try:

            execute_write_query(sql)

            print("\nRecord(s) updated successfully!")

        except Exception as error:

            print("\nDatabase Execution Error:")
            print(error)

        return

    # ============================================================
    # DELETE PIPELINE
    # ============================================================

    if intent == "DELETE":

        print("\nGenerating DELETE SQL...")

        sql = generate_delete_sql(question)

        print("\nGenerated SQL:")
        print(sql)

        # --------------------------------------------------------
        # Validate DELETE SQL
        # --------------------------------------------------------

        valid, message = validate_delete_sql(sql)

        print("\nDELETE Validation:")
        print(message)

        if not valid:

            print("\nDELETE SQL is invalid.")
            return

        # --------------------------------------------------------
        # Operation Safety Check
        # --------------------------------------------------------

        safety_result = check_operation_safety(sql)

        print("\nOperation Safety:")
        print(safety_result["message"])

        if not safety_result["safe"]:

            print("\nOperation blocked for safety.")
            return

        # --------------------------------------------------------
        # Strong Confirmation
        # --------------------------------------------------------

        print("\nWARNING:")
        print("This operation will permanently delete data.")

        confirmation = input(
            "\nDo you want to permanently delete this data? (yes/no): "
        ).strip().lower()

        if confirmation not in ["yes", "y"]:

            print("\nOperation cancelled.")
            return

        # --------------------------------------------------------
        # Execute DELETE
        # --------------------------------------------------------

        try:

            execute_write_query(sql)

            print("\nRecord(s) deleted successfully!")

        except Exception as error:

            print("\nDatabase Execution Error:")
            print(error)

        return

    # ============================================================
    # READ PIPELINE
    # ============================================================

    if intent == "READ":

        # --------------------------------------------------------
        # Generate SQL
        # --------------------------------------------------------

        sql = generate_sql(question)

        print("\nGenerated SQL:")
        print(sql)

        # --------------------------------------------------------
        # Basic SQL validation
        # --------------------------------------------------------

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

        # --------------------------------------------------------
        # Semantic validation
        # --------------------------------------------------------

        semantic_result = validate_semantics(
            question,
            sql
        )

        print("\nSemantic Validation:")
        print(semantic_result)

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

            # ----------------------------------------------------
            # Validate corrected SQL
            # ----------------------------------------------------

            valid, message = validate_sql(corrected_sql)

            print("\nCorrected SQL Validation:")
            print(message)

            if not valid:

                print("\nCorrected SQL is still invalid.")
                return

            # ----------------------------------------------------
            # Validate corrected SQL semantics
            # ----------------------------------------------------

            corrected_semantic = validate_semantics(
                question,
                corrected_sql
            )

            print("\nCorrected SQL Semantic Validation:")
            print(corrected_semantic)

            if not corrected_semantic["correct"]:

                print(
                    "\nCorrected SQL is still "
                    "semantically incorrect."
                )

                print(corrected_semantic["reason"])
                return

            sql = corrected_sql

        # --------------------------------------------------------
        # Execute READ query
        # --------------------------------------------------------

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

            # ----------------------------------------------------
            # Validate corrected SQL
            # ----------------------------------------------------

            valid, message = validate_sql(corrected_sql)

            print("\nCorrected SQL Validation:")
            print(message)

            if not valid:

                print("\nCorrected SQL is still invalid.")
                return

            # ----------------------------------------------------
            # Validate corrected SQL semantics
            # ----------------------------------------------------

            semantic_result = validate_semantics(
                question,
                corrected_sql
            )

            print("\nCorrected SQL Semantic Validation:")
            print(semantic_result)

            if not semantic_result["correct"]:

                print(
                    "\nCorrected SQL is still "
                    "semantically incorrect."
                )

                print(semantic_result["reason"])
                return

            sql = corrected_sql

            # ----------------------------------------------------
            # Execute corrected SQL
            # ----------------------------------------------------

            try:

                columns, results = execute_query(sql)

            except Exception as error:

                print("\nCorrected SQL execution failed:")
                print(error)
                return

        # --------------------------------------------------------
        # Display results
        # --------------------------------------------------------

        print("\nResults:")

        print(columns)

        for row in results:
            print(row)

        return

    # ============================================================
    # UNKNOWN INTENT
    # ============================================================

    print("\nUnsupported intent:")
    print(intent)


if __name__ == "__main__":
    main()