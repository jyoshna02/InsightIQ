
from sql_service import generate_sql
from query_service import execute_query
from response_service import generate_response


def answer_question(question):

    print("\nUSER QUESTION:")
    print(question)

    # Step 1: Generate SQL
    sql_query = generate_sql(question)

    print("\nGENERATED SQL:")
    print(sql_query)

    # Step 2: Validate and execute SQL
    result = execute_query(sql_query)

    print("\nQUERY RESULT:")
    print(result)

    # Step 3: Convert query result into records
    result_records = result.to_dict(orient="records")

    # Step 4: Generate AI explanation
    ai_response = generate_response(
        question,
        sql_query,
        result_records
    )

    print("\nINSIGHTIQ AI RESPONSE:")
    print(ai_response)

    return {
        "question": question,
        "sql": sql_query,
        "result": result_records,
        "answer": ai_response
    }


if __name__ == "__main__":

    question = "Which product generated the highest profit?"

    response = answer_question(question)
