
import sys
from pathlib import Path

SERVICES_DIR = Path(__file__).resolve().parent

if str(SERVICES_DIR) not in sys.path:
    sys.path.insert(0, str(SERVICES_DIR))

from llm_service import ask_gemini


def fix_sql_error(question, sql_query, error, schema):

    prompt = f"""
You are an expert DuckDB SQL developer.

The following SQL query produced an error.

User question:
{question}

Dataset schema:
{schema}

Incorrect SQL:
{sql_query}

Error message:
{error}

Instructions:
1. Understand the original user question.
2. Fix the SQL query using the provided schema.
3. Use only the uploaded_data table.
4. Generate only SELECT queries.
5. Do not use INSERT, UPDATE, DELETE or DROP.
6. Use exact column names from the schema.
7. Return only the corrected SQL query.
8. Do not include Markdown or explanations.
"""

    corrected_sql = ask_gemini(prompt)

    return (
        corrected_sql
        .strip()
        .replace("```sql", "")
        .replace("```", "")
        .strip()
    )


if __name__ == "__main__":

    question = "Which movie has the highest IMDb rating?"

    incorrect_sql = """
    SELECT Movie, MAX(Rating)
    FROM uploaded_data
    GROUP BY Movie
    """

    error = "Column Movie does not exist"

    schema = """
    Table: uploaded_data
    Columns:
    - Series_Title (VARCHAR)
    - IMDB_Rating (DOUBLE)
    - Director (VARCHAR)
    """

    corrected_sql = fix_sql_error(
        question,
        incorrect_sql,
        error,
        schema
    )

    print("CORRECTED SQL:")
    print(corrected_sql)
