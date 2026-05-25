import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("MONDAY_API_TOKEN")
headers = {
    "Authorization": token,
    "Content-Type": "application/json",
    "API-Version": "2023-10"
}

query = """
query {
  boards(ids: [18413482266]) {
    columns(ids: ["color_mm3dtq01"]) {
      id
      title
      type
      settings_str
    }
  }
}
"""

response = requests.post(
    "https://api.monday.com/v2",
    json={"query": query},
    headers=headers
)

if response.status_code == 200:
    data = response.json()
    boards = data.get("data", {}).get("boards", [])
    if boards and boards[0]["columns"]:
        col = boards[0]["columns"][0]
        print(f"Column ID: {col['id']}")
        print(f"Title: {col['title']}")
        print(f"Type: {col['type']}")
        print("Settings String:")
        settings = json.loads(col["settings_str"])
        print(json.dumps(settings, indent=2, ensure_ascii=False))
    else:
        print("Board or Column not found")
else:
    print(f"Failed to fetch: {response.status_code} - {response.text}")
