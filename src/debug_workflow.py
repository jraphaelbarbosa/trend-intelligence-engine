import sys
import requests
import json

sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzMzE4NzVkMC1jMDVkLTQ5MzMtYjZjMy02MGNjYTQ2MjIwMjgiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwianRpIjoiOWNhOTc0ODQtY2RkMi00MjQxLTg4OTctNGYzYjliYmNjYjRlIiwiaWF0IjoxNzc5MjMwNTY3fQ.wrSKDghTa2WFLWREbiQFy16Rb58-2mBBk5at8Hgx4bA"
BASE_URL = "http://localhost:5678/api/v1"
HEADERS = {"X-N8N-API-KEY": API_KEY}

# Fetch last executions for our workflow
workflow_id = "LybzRfkuflg218jx"
url = f"{BASE_URL}/executions?workflowId={workflow_id}&limit=1&status=error"

response = requests.get(url, headers=HEADERS)
if response.status_code == 200:
    data = response.json()
    executions = data.get("data", [])
    if executions:
        exec_id = executions[0]["id"]
        print(f"Last failed execution ID: {exec_id}")
        
        # Fetch full execution details
        exec_url = f"{BASE_URL}/executions/{exec_id}"
        exec_resp = requests.get(exec_url, headers=HEADERS)
        if exec_resp.status_code == 200:
            exec_data = exec_resp.json()
            
            # Look at the Monday.com node result
            result_data = exec_data.get("data", {}).get("resultData", {})
            run_data = result_data.get("runData", {})
            
            # Print Monday.com node execution data
            for node_name in ["6. Monday.com", "5. Loop de Vídeos", "5. Parse JSON"]:
                if node_name in run_data:
                    node_runs = run_data[node_name]
                    print(f"\n=== {node_name} - Execution Data ===")
                    for i, run in enumerate(node_runs):
                        print(f"\n--- Run {i} ---")
                        # Show error if any
                        if run.get("error"):
                            print(f"ERROR: {json.dumps(run['error'], indent=2, ensure_ascii=False)}")
                        
                        # Show input data (first item only)
                        input_data = run.get("data", {}).get("main", [[]])
                        if input_data and input_data[0]:
                            items = input_data[0]
                            if items:
                                print(f"Output items count: {len(items)}")
                                # Print first item
                                if len(items) > 0:
                                    first_item = items[0].get("json", {})
                                    print(f"First item keys: {list(first_item.keys())}")
                                    # Print a few key fields
                                    for key in ["content_title", "public_sentiment", "algorithm_relevance_score", "video_tone", "analysis_id"]:
                                        if key in first_item:
                                            val = first_item[key]
                                            if isinstance(val, str) and len(val) > 80:
                                                val = val[:80] + "..."
                                            print(f"  {key}: {val}")
                        
            # Also print error message
            error = result_data.get("error", {})
            if error:
                print(f"\n=== GLOBAL EXECUTION ERROR ===")
                print(json.dumps(error, indent=2, ensure_ascii=False))
        else:
            print(f"Error fetching execution: {exec_resp.status_code}")
    else:
        print("No failed executions found")
else:
    print(f"Error: {response.status_code} - {response.text}")
