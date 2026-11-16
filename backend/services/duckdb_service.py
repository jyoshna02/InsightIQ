
import duckdb
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "data" / "insightiq.duckdb"


def store_dataset(df):
    # Create a fresh database connection
    conn = duckdb.connect(str(DB_PATH))

    try:
        # Register the Pandas DataFrame
        conn.register("uploaded_df", df)

        # Create or replace the table
        conn.execute("""
            CREATE OR REPLACE TABLE uploaded_data AS
            SELECT * FROM uploaded_df
        """)

        # Verify the number of rows using a new connection
        conn.close()

        verify_conn = duckdb.connect(str(DB_PATH), read_only=True)

        try:
            total_rows = verify_conn.execute(
                "SELECT COUNT(*) FROM uploaded_data"
            ).fetchone()[0]

            return total_rows

        finally:
            verify_conn.close()

    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception:
                pass
