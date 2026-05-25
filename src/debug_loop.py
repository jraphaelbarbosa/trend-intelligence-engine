import sys
import requests
import json

sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzMzE4NzVkMC1jMDVkLTQ5MzMtYjZjMy02MGNjYTQ2MjIwMjgiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwianRpIjoiOWNhOTc0ODQtY2RkMi00MjQxLTg4OTctNGYzYjliYmNjYjRlIiwiaWF0IjoxNzc5MjMwNTY3fQ.wrSKDghTa2WFLWREbiQFy16Rb58-2mBBk5at8Hgx4bA"
BASE_URL = "http://localhost:5678/api/v1"
HEADERS = {"X-N8N-API-KEY": API_KEY}

workflow_id = "LybzRfkuflg218jx"
url = f"{BASE_URL}/workflows/{workflow_id}"

response = requests.get(url, headers=HEADERS)
if response.status_code == 200:
    wf = response.json()
    
    # Print the Loop node configuration
    for node in wf.get("nodes", []):
        if "loop" in node.get("name", "").lower():
            print("=== LOOP NODE CONFIG ===")
            print(json.dumps(node, indent=2, ensure_ascii=False))
            print("=" * 50)
            
    # Print all connections in the workflow
    print("\n=== ALL WORKFLOW CONNECTIONS ===")
    print(json.dumps(wf.get("connections", {}), indent=2))
else:
    print(f"Error: {response.status_code}")
