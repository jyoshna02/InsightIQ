
import duckdb
from pathlib import Path

# Locate the database file
BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "data" / "insightiq.duckdb"

# Connect to DuckDB
conn = duckdb.connect(str(DB_PATH))

# Check total records
result = conn.execute(
    "SELECT COUNT(*) FROM uploaded_data"
).fetchone()

print("Total records:", result[0])

# Display first five records
data = conn.execute(
    "SELECT * FROM uploaded_data LIMIT 5"
).fetchdf()

print(data)

conn.close()
