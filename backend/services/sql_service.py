from llm_service import ask_gemini
from schema_service import get_schema_text


def generate_sql(question):

    schema = get_schema_text()

    prompt = f"""
You are an expert SQL developer.

Database table: uploaded_data

Dataset schema:
{schema}

User question:
{question}


Instructions:
1. Generate a DuckDB-compatible SQL query.
2. Use only the uploaded_data table.
3. Generate only SELECT queries.
4. Do not use INSERT, UPDATE, DELETE or DROP.
5. Use exact column names from the schema.
6. When comparing products, regions, or categories using
   SUM, AVG, COUNT, MIN, or MAX, include the calculated
   metric in the SELECT statement.
7. For highest or lowest questions, sort using the
   relevant metric and use LIMIT 1.
8. Return only the SQL query.
9. Do not include Markdown or explanations.

"""

    sql_query = ask_gemini(prompt)

    return sql_query.strip().replace("```sql", "").replace("```", "")


if __name__ == "__main__":

    question = "What is the total sales?"

    sql = generate_sql(question)

    print("\nUser Question:")
    print(question)

    print("\nGenerated SQL:")
    print(sql)
