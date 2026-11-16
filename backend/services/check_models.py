
from llm_service import client

print("Checking available Gemini models...\n")

try:
    for model in client.models.list():
        actions = model.supported_actions or []

        if "generateContent" in actions:
            print("Model:", model.name)
            print("Supported actions:", actions)
            print("-------------------------")

except Exception as error:
    print("ERROR:", error)
