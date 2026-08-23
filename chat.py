from src.clarification import check_ambiguity
from src.sql_generator import generate_sql
from src.database import execute_query


def main():
    question = input("Ask a question: ")

    clarification = check_ambiguity(question)

    if clarification["ambiguous"]:
        print("\nClarification:", clarification["question"])

        answer = input("\nYour answer: ")

        question = question + " " + answer

    print("\nResolved question:")
    print(question)

    sql = generate_sql(question)

    print("\nGenerated SQL:")
    print(sql)

    columns, results = execute_query(sql)

    print("\nResults:")

    print(columns)

    for row in results:
        print(row)

    


if __name__ == "__main__":
    main()