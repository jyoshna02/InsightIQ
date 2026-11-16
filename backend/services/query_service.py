
import duckdb
from pathlib import Path
from sql_validator import validate_sql

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "data" / "insightiq.duckdb"


def execute_query(sql_query):

    # Validate SQL before execution
    safe_query = validate_sql(sql_query)

    conn = duckdb.connect(str(DB_PATH), read_only=True)

    try:
        result = conn.execute(safe_query).fetchdf()
        return result

    finally:
        conn.close()


if __name__ == "__main__":

    query = "SELECT SUM(Sales) AS Total_Sales FROM uploaded_data"

    try:
        result = execute_query(query)

        print("SQL VALIDATION: PASSED")
        print("QUERY RESULT:")
        print(result)

    except Exception as error:
        print("ERROR:", error)
