
import requests
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
file_path = BASE_DIR / "data" / "sample_sales.csv"

url = "http://127.0.0.1:5000/api/upload"

print("Testing URL:", url)
print("CSV exists:", file_path.exists())

# Check Flask health
health = requests.get("http://127.0.0.1:5000/api/health")
print("Health Status:", health.status_code)
print("Health Response:", health.text)

# Upload CSV while the file is open
with open(file_path, "rb") as file:
    response = requests.post(
        url,
        files={"file": file}
    )

print("Upload Status:", response.status_code)
print("Upload Response:")
print(response.text)
