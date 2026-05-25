import sys
import requests
import json

sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzMzE4NzVkMC1jMDVkLTQ5MzMtYjZjMy02MGNjYTQ2MjIwMjgiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwianRpIjoiOWNhOTc0ODQtY2RkMi00MjQxLTg4OTctNGYzYjliYmNjYjRlIiwiaWF0IjoxNzc5MjMwNTY3fQ.wrSKDghTa2WFLWREbiQFy16Rb58-2mBBk5at8Hgx4bA"
BASE_URL = "http://localhost:5678/api/v1"
HEADERS = {"X-N8N-API-KEY": API_KEY}

exec_id = "3"
url = f"{BASE_URL}/executions/{exec_id}"

response = requests.get(url, headers=HEADERS)
print(f"Status Code: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print("Execution data keys:", list(data.keys()))
    # Let's write the entire response to a json file to inspect it
    with open("execution_3.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("Successfully wrote execution_3.json")
    
    # Check if there is an error in execution
    result_data = data.get("data", {}).get("resultData", {})
    print("Result data keys:", list(result_data.keys()))
    error = result_data.get("error", {})
    if error:
        print("Global Error:")
        print(json.dumps(error, indent=2))
        
    run_data = result_data.get("runData", {})
    print("Run data keys (nodes executed):", list(run_data.keys()))
    for node_name, runs in run_data.items():
        print(f"Node: {node_name}, runs count: {len(runs)}")
        for i, r in enumerate(runs):
            if r.get("error"):
                print(f"  Run {i} ERROR: {json.dumps(r['error'], indent=2)}")
else:
    print(response.text)
