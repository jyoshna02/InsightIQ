import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai

# Find the main Insight IQ folder
BASE_DIR = Path(__file__).resolve().parents[2]

# Load the .env file from the project folder
load_dotenv(BASE_DIR / ".env")

# Read the API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "Gemini API key not found. Check your .env file."
    )

# Connect to Gemini
client = genai.Client(api_key=api_key)


def ask_gemini(prompt):
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )
    return response.text


if __name__ == "__main__":
    answer = ask_gemini("Introduce yourself in one sentence.")
    print("Gemini Response:")
    print(answer)