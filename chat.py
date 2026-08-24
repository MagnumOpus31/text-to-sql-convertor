from src.clarification import check_ambiguity,resolve_question
from src.sql_generator import generate_sql
from src.database import execute_query
from src.sql_validator import validate_sql


def main():
    question = input("Ask a question: ")

    clarification = check_ambiguity(question)

    if clarification["ambiguous"]:
        print("\nClarification:", clarification["question"])

        answer = input("\nYour answer: ")
        question=resolve_question(
            question,
            clarification["question"],
            answer
        )


    print("\nResolved question:")
    print(question)

    sql = generate_sql(question)

    print("\nGenerated SQL:")
    print(sql)

    valid, message=validate_sql(sql)
    if not valid:
        print("\nSQL Validation Failed:")
        print(message)
        return

    print("\nSQL Validation:")
    print(message)

    columns, results = execute_query(sql)

    print("\nResults:")

    print(columns)

    for row in results:
        print(row)

    


if __name__ == "__main__":
    main()