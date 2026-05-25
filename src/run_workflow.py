import sys
import requests
import json
import time

sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzMzE4NzVkMC1jMDVkLTQ5MzMtYjZjMy02MGNjYTQ2MjIwMjgiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwianRpIjoiOWNhOTc0ODQtY2RkMi00MjQxLTg4OTctNGYzYjliYmNjYjRlIiwiaWF0IjoxNzc5MjMwNTY3fQ.wrSKDghTa2WFLWREbiQFy16Rb58-2mBBk5at8Hgx4bA"
BASE_URL = "http://localhost:5678/api/v1"
HEADERS = {"X-N8N-API-KEY": API_KEY}

workflow_id = "LybzRfkuflg218jx"
url = f"{BASE_URL}/workflows/{workflow_id}/run"

print("Triggering workflow execution manually via API...")
response = requests.post(url, headers=HEADERS)

print(f"Status Code: {response.status_code}")
if response.status_code in [200, 201]:
    data = response.json()
    print("Workflow execution started successfully!")
    print("Response keys:", list(data.keys()))
    if "executionId" in data:
        exec_id = data["executionId"]
        print(f"Execution ID: {exec_id}")
        
        # Poll execution status
        print("Monitoring execution...")
        for i in range(30):
            time.sleep(5)
            status_url = f"{BASE_URL}/executions/{exec_id}"
            status_resp = requests.get(status_url, headers=HEADERS)
            if status_resp.status_code == 200:
                status_data = status_resp.json()
                status = status_data.get("status")
                print(f"[{i*5}s] Execution Status: {status}")
                if status in ["success", "failed", "error"]:
                    print(f"Execution finished with status: {status}")
                    break
            else:
                print(f"Error checking status: {status_resp.status_code}")
else:
    print(response.text)
