
import duckdb
from pathlib import Path

# Locate the Insight IQ project folder
BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "data" / "insightiq.duckdb"


def get_dataset_schema():

    conn = duckdb.connect(str(DB_PATH), read_only=True)

    try:
        # Read the uploaded dataset's column information
        result = conn.execute(
            "DESCRIBE uploaded_data"
        ).fetchall()

        columns = []

        for row in result:
            columns.append({
                "column_name": row[0],
                "data_type": row[1],
                "nullable": row[2]
            })

        return {
            "table_name": "uploaded_data",
            "columns": columns
        }

    finally:
        conn.close()


def get_schema_text():

    schema = get_dataset_schema()

    text = f"Table: {schema['table_name']}\n"
    text += "Columns:\n"

    for column in schema["columns"]:
        text += (
            f"- {column['column_name']} "
            f"({column['data_type']})\n"
        )

    return text


if __name__ == "__main__":
    print("INSIGHTIQ DATASET SCHEMA")
    print("-----------------------")
    print(get_schema_text())
