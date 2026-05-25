import sys
import requests
import json

sys.stdout.reconfigure(encoding='utf-8')

workflow_id = "LybzRfkuflg218jx"

# Let's try triggering the internal frontend API of n8n
# Usually it is under /rest/workflows/{id}/run or /rest/workflows/run
urls = [
    f"http://localhost:5678/rest/workflows/{workflow_id}/run",
    f"http://localhost:5678/rest/workflows/run",
    f"http://localhost:5678/api/v1/workflows/{workflow_id}/run",
    f"http://localhost:5678/api/v1/executions"
]

headers = {
    "X-N8N-API-KEY": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzMzE4NzVkMC1jMDVkLTQ5MzMtYjZjMy02MGNjYTQ2MjIwMjgiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwianRpIjoiOWNhOTc0ODQtY2RkMi00MjQxLTg4OTctNGYzYjliYmNjYjRlIiwiaWF0IjoxNzc5MjMwNTY3fQ.wrSKDghTa2WFLWREbiQFy16Rb58-2mBBk5at8Hgx4bA"
}

for url in urls:
    try:
        print(f"Trying: {url} ...")
        # Try POST first
        res = requests.post(url, headers=headers, json={"workflowId": workflow_id} if "executions" in url else {})
        print(f"  POST Status: {res.status_code}")
        print(f"  POST Response: {res.text[:300]}")
    except Exception as e:
        print(f"  POST Failed: {e}")
