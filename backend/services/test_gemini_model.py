
from llm_service import client

try:
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents="Say hello to InsightIQ in one sentence."
    )

    print("\nGEMINI TEST SUCCESSFUL!")
    print(response.text)

except Exception as error:
    print("\nGEMINI TEST FAILED!")
    print(error)
