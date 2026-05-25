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

# Query the schema of the mutation
query = """
query {
  __type(name: "Mutation") {
    fields {
      name
      args {
        name
        type {
          name
          kind
          ofType {
            name
            kind
          }
        }
      }
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
    fields = data.get("data", {}).get("__type", {}).get("fields", [])
    for field in fields:
        if "status" in field["name"].lower() or "column" in field["name"].lower():
            print(f"Mutation Field: {field['name']}")
            print("Arguments:")
            for arg in field.get("args", []):
                arg_type = arg["type"]["name"] or (arg["type"]["ofType"]["name"] if arg["type"]["ofType"] else "N/A")
                print(f"  - {arg['name']}: {arg_type} ({arg['type']['kind']})")
            print("-" * 50)
else:
    print(f"Falha: {response.status_code}")
