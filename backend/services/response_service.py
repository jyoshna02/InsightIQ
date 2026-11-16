
import json
from llm_service import ask_gemini


def generate_response(question, sql_query, query_result):

    prompt = f"""
You are InsightIQ, an AI data analytics assistant.

User question:
{question}

Generated SQL:
{sql_query}

Query result:
{json.dumps(query_result, default=str)}

Instructions:
1. Explain the result in simple English.
2. Highlight the most important insight.
3. Use only the given result.
4. Never invent numbers.
5. Keep the response professional and concise.
"""

    return ask_gemini(prompt)


if __name__ == "__main__":

    question = "Which product generated the highest profit?"

    sql = "SELECT Product, SUM(Profit) AS Total_Profit FROM uploaded_data GROUP BY Product ORDER BY Total_Profit DESC LIMIT 1"

    result = [
        {"Product": "Laptop", "Total_Profit": 18000}
    ]

    answer = generate_response(question, sql, result)

    print("\nINSIGHTIQ AI RESPONSE:")
    print(answer)
