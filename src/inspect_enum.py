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

# Query the schema of the ColumnProperty enum
query = """
query {
  __type(name: "ColumnProperty") {
    enumValues {
      name
      description
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
    values = data.get("data", {}).get("__type", {}).get("enumValues", [])
    print("ColumnProperty Enum Values:")
    for val in values:
        print(f"  - {val['name']}: {val['description']}")
else:
    print(f"Falha: {response.status_code}")
