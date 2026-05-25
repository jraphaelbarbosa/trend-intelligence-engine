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

# Query all columns in board 18413482266
query = """
query {
  boards(ids: [18413482266]) {
    id
    name
    columns {
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
    if "errors" in data:
        print("Erros:", data["errors"])
    else:
        boards = data.get("data", {}).get("boards", [])
        if boards:
            board = boards[0]
            print(f"Board ID: {board['id']}")
            print(f"Board Name: {board['name']}")
            print("\n=== COLUMNS ===")
            for col in board.get("columns", []):
                print(f"ID: {col['id']}")
                print(f"Title: {col['title']}")
                print(f"Type: {col['type']}")
                print("-" * 30)
else:
    print(f"Falha: {response.status_code}")
