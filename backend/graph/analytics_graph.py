
import sys
from pathlib import Path
from typing import TypedDict

from langgraph.graph import StateGraph, START, END

BACKEND_DIR = Path(__file__).resolve().parents[1]
SERVICES_DIR = BACKEND_DIR / "services"

sys.path.insert(0, str(SERVICES_DIR))

from sql_service import generate_sql
from sql_validator import validate_sql
from query_service import execute_query
from response_service import generate_response
from schema_service import get_schema_text
from error_handler import fix_sql_error


class AnalyticsState(TypedDict, total=False):
    question: str
    sql_query: str
    query_result: list
    answer: str


def generate_sql_node(state):
    sql = generate_sql(state["question"])
    return {"sql_query": sql}


def validate_sql_node(state):
    safe_sql = validate_sql(state["sql_query"])
    return {"sql_query": safe_sql}


def execute_query_node(state):

    question = state["question"]
    sql_query = state["sql_query"]

    max_retries = 2

    for attempt in range(max_retries + 1):

        try:
            result = execute_query(sql_query)

            records = result.to_dict(orient="records")

            print("\nSQL EXECUTION SUCCESSFUL!")

            return {
                "sql_query": sql_query,
                "query_result": records
            }

        except Exception as error:

            print(f"\nSQL ERROR: {error}")

            if attempt == max_retries:
                raise RuntimeError(
                    "InsightIQ could not fix the SQL query "
                    "after multiple attempts."
                ) from error

            print("\nAttempting automatic SQL correction...")

            schema = get_schema_text()

            corrected_sql = fix_sql_error(
                question,
                sql_query,
                str(error),
                schema
            )

            # Validate corrected SQL before execution
            sql_query = validate_sql(corrected_sql)

            print("\nCORRECTED SQL:")
            print(sql_query)

    raise RuntimeError("SQL execution failed.")


def generate_response_node(state):

    answer = generate_response(
        state["question"],
        state["sql_query"],
        state["query_result"]
    )

    return {"answer": answer}


builder = StateGraph(AnalyticsState)

builder.add_node("generate_sql", generate_sql_node)
builder.add_node("validate_sql", validate_sql_node)
builder.add_node("execute_query", execute_query_node)
builder.add_node("generate_response", generate_response_node)

builder.add_edge(START, "generate_sql")
builder.add_edge("generate_sql", "validate_sql")
builder.add_edge("validate_sql", "execute_query")
builder.add_edge("execute_query", "generate_response")
builder.add_edge("generate_response", END)

analytics_graph = builder.compile()


if __name__ == "__main__":

    question = "Which director has the highest total votes?"

    result = analytics_graph.invoke({
        "question": question
    })

    print("\n========== INSIGHTIQ ==========")
    print("QUESTION:", result["question"])
    print("\nGENERATED SQL:", result["sql_query"])
    print("\nQUERY RESULT:", result["query_result"])
    print("\nAI INSIGHT:", result["answer"])
