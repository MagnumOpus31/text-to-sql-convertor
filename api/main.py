from fastapi import FastAPI, HTTPException

from api.schemas import QueryRequest, QueryResponse

from src.clarification import check_ambiguity
from src.database import execute_query
from src.local_typo_corrector import correct_typos
from src.intent_detector import detect_intent

from src.sql_generator import generate_sql
from src.sql_corrector import correct_sql
from src.sql_validator import validate_sql
from src.sql_semantic_validator import validate_semantics

from src.schema_generator import generate_create_table_sql
from src.schema_validator import validate_create_table_sql

from src.insert_generator import generate_insert_sql
from src.insert_validator import validate_insert_sql

from src.update_generator import generate_update_sql
from src.update_validator import validate_update_sql

from src.delete_generator import generate_delete_sql
from src.delete_validator import validate_delete_sql

from src.operation_safety import check_operation_safety


app = FastAPI(
    title="Text-to-SQL API",
    description="AI-powered Natural Language to SQL REST API",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Text-to-SQL API is running"
    }


@app.post("/query", response_model=QueryResponse)
def process_query(request: QueryRequest):

    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    try:

        # ----------------------------------------------------
        # 1. Local typo correction
        # ----------------------------------------------------

        corrected_question = correct_typos(question)


        # ----------------------------------------------------
        # 2. Clarification
        # ----------------------------------------------------

        clarification = check_ambiguity(corrected_question)

        if clarification["ambiguous"]:

            return QueryResponse(
                status="clarification_required",
                question=question,
                corrected_question=corrected_question,
                clarification_question=clarification["question"]
            )


        # ----------------------------------------------------
        # 3. Intent detection
        # ----------------------------------------------------

        intent_result = detect_intent(corrected_question)
        intent = intent_result["intent"]


        # ----------------------------------------------------
        # 4. CREATE TABLE
        # ----------------------------------------------------

        if intent == "CREATE_TABLE":

            sql = generate_create_table_sql(
                corrected_question
            )

            valid, message = validate_create_table_sql(sql)

            if not valid:
                return QueryResponse(
                    status="validation_failed",
                    question=question,
                    corrected_question=corrected_question,
                    intent=intent,
                    sql=sql,
                    message=message
                )

            return QueryResponse(
                status="confirmation_required",
                question=question,
                corrected_question=corrected_question,
                intent=intent,
                sql=sql,
                message=message
            )


        # ----------------------------------------------------
        # 5. INSERT
        # ----------------------------------------------------

        elif intent == "INSERT":

            sql = generate_insert_sql(
                corrected_question
            )

            valid, message = validate_insert_sql(sql)

            if not valid:
                return QueryResponse(
                    status="validation_failed",
                    question=question,
                    corrected_question=corrected_question,
                    intent=intent,
                    sql=sql,
                    message=message
                )

            return QueryResponse(
                status="confirmation_required",
                question=question,
                corrected_question=corrected_question,
                intent=intent,
                sql=sql,
                message=message
            )


        # ----------------------------------------------------
        # 6. UPDATE
        # ----------------------------------------------------

        elif intent == "UPDATE":

            sql = generate_update_sql(
                corrected_question
            )

            valid, message = validate_update_sql(sql)

            if not valid:
                return QueryResponse(
                    status="validation_failed",
                    question=question,
                    corrected_question=corrected_question,
                    intent=intent,
                    sql=sql,
                    message=message
                )

            safety_result = check_operation_safety(sql)

            if not safety_result["safe"]:
                return QueryResponse(
                    status="unsafe_operation",
                    question=question,
                    corrected_question=corrected_question,
                    intent=intent,
                    sql=sql,
                    message=safety_result["message"]
                )

            return QueryResponse(
                status="confirmation_required",
                question=question,
                corrected_question=corrected_question,
                intent=intent,
                sql=sql,
                message=safety_result["message"]
            )


        # ----------------------------------------------------
        # 7. DELETE
        # ----------------------------------------------------

        elif intent == "DELETE":

            sql = generate_delete_sql(
                corrected_question
            )

            valid, message = validate_delete_sql(sql)

            if not valid:
                return QueryResponse(
                    status="validation_failed",
                    question=question,
                    corrected_question=corrected_question,
                    intent=intent,
                    sql=sql,
                    message=message
                )

            safety_result = check_operation_safety(sql)

            if not safety_result["safe"]:
                return QueryResponse(
                    status="unsafe_operation",
                    question=question,
                    corrected_question=corrected_question,
                    intent=intent,
                    sql=sql,
                    message=safety_result["message"]
                )

            return QueryResponse(
                status="confirmation_required",
                question=question,
                corrected_question=corrected_question,
                intent=intent,
                sql=sql,
                message=safety_result["message"]
            )


        # ----------------------------------------------------
        # 8. READ
        # ----------------------------------------------------

        elif intent == "READ":

            sql = generate_sql(corrected_question)


            # SQL validation
            valid, message = validate_sql(sql)

            if not valid:

                sql = correct_sql(
                    corrected_question,
                    sql,
                    message
                )

                valid, message = validate_sql(sql)

                if not valid:
                    return QueryResponse(
                        status="validation_failed",
                        question=question,
                        corrected_question=corrected_question,
                        intent=intent,
                        sql=sql,
                        message=message
                    )


            # Semantic validation
            semantic_result = validate_semantics(
                corrected_question,
                sql
            )

            if not semantic_result["correct"]:

                sql = correct_sql(
                    corrected_question,
                    sql,
                    semantic_result["reason"]
                )

                valid, message = validate_sql(sql)

                if not valid:
                    return QueryResponse(
                        status="validation_failed",
                        question=question,
                        corrected_question=corrected_question,
                        intent=intent,
                        sql=sql,
                        message=message
                    )

                corrected_semantic = validate_semantics(
                    corrected_question,
                    sql
                )

                if not corrected_semantic["correct"]:
                    return QueryResponse(
                        status="semantic_validation_failed",
                        question=question,
                        corrected_question=corrected_question,
                        intent=intent,
                        sql=sql,
                        message=corrected_semantic["reason"]
                    )


            # Database execution
            try:

                columns, results = execute_query(sql)

            except Exception as error:

                sql = correct_sql(
                    corrected_question,
                    sql,
                    str(error)
                )

                valid, message = validate_sql(sql)

                if not valid:
                    return QueryResponse(
                        status="execution_failed",
                        question=question,
                        corrected_question=corrected_question,
                        intent=intent,
                        sql=sql,
                        message=message
                    )

                semantic_result = validate_semantics(
                    corrected_question,
                    sql
                )

                if not semantic_result["correct"]:
                    return QueryResponse(
                        status="semantic_validation_failed",
                        question=question,
                        corrected_question=corrected_question,
                        intent=intent,
                        sql=sql,
                        message=semantic_result["reason"]
                    )

                try:

                    columns, results = execute_query(sql)

                except Exception as second_error:

                    return QueryResponse(
                        status="execution_failed",
                        question=question,
                        corrected_question=corrected_question,
                        intent=intent,
                        sql=sql,
                        message=str(second_error)
                    )


            # Convert SQLite result into JSON-compatible objects
            formatted_results = [
                dict(zip(columns, row))
                for row in results
            ]

            return QueryResponse(
                status="success",
                question=question,
                corrected_question=corrected_question,
                intent=intent,
                sql=sql,
                results=formatted_results,
                message="Query executed successfully."
            )


        # ----------------------------------------------------
        # Unsupported intent
        # ----------------------------------------------------

        else:

            return QueryResponse(
                status="unsupported_intent",
                question=question,
                corrected_question=corrected_question,
                intent=intent,
                message=f"Unsupported intent: {intent}"
            )


    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )