import sqlite3
import os
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Re-use unflatted logic to parse n8n execution data
def unflatted(data):
    if not isinstance(data, list):
        return data
    resolved = {}
    
    def resolve(idx_str):
        if not idx_str.isdigit():
            return idx_str
        idx = int(idx_str)
        if idx < 0 or idx >= len(data):
            return idx_str
        if idx in resolved:
            return resolved[idx]
        val = data[idx]
        if isinstance(val, dict):
            res = {}
            resolved[idx] = res
            for k, v in val.items():
                if isinstance(v, str) and v.isdigit():
                    res[k] = resolve(v)
                elif isinstance(v, list):
                    res[k] = [resolve(item) if isinstance(item, str) and item.isdigit() else resolve_deep(item) for item in v]
                else:
                    res[k] = resolve_deep(v)
            return res
        elif isinstance(val, list):
            res = []
            resolved[idx] = res
            for item in val:
                if isinstance(item, str) and item.isdigit():
                    res.append(resolve(item))
                else:
                    res.append(resolve_deep(item))
            return res
        else:
            resolved[idx] = val
            return val

    def resolve_deep(val):
        if isinstance(val, str) and val.isdigit():
            return resolve(val)
        elif isinstance(val, dict):
            return {k: resolve_deep(v) for k, v in val.items()}
        elif isinstance(val, list):
            return [resolve_deep(item) for item in val]
        return val

    return resolve("0")

db_path = os.path.expanduser("~/.n8n/database.sqlite")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Query the absolute latest execution with status='error'
    cursor.execute("""
        SELECT e.id, e.status, e.workflowId, d.data, e.createdAt 
        FROM execution_entity e
        JOIN execution_data d ON e.id = d.executionId
        WHERE e.status='error' 
        ORDER BY e.id DESC LIMIT 1;
    """)
    row = cursor.fetchone()
    if row:
        exec_id, status, wf_id, data_str, created_at = row
        print(f"Latest Error Execution ID: {exec_id} (Created at {created_at})")
        data_json = json.loads(data_str)
        unflated_data = unflatted(data_json)
        
        # Save to file
        with open("latest_execution_error.json", "w", encoding="utf-8") as f:
            json.dump(unflated_data, f, indent=2, ensure_ascii=False)
        print("Wrote latest_execution_error.json")
        
        # Search for errors recursively
        errors = []
        def find_errors(obj, path=""):
            if isinstance(obj, dict):
                for k in ["error", "message", "description", "stack"]:
                    if k in obj and obj[k]:
                        errors.append((f"{path}/{k}", obj[k]))
                for k, v in obj.items():
                    find_errors(v, f"{path}/{k}")
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    find_errors(item, f"{path}[{i}]")
                    
        find_errors(unflated_data)
        print(f"\nFound {len(errors)} error fields:")
        for path, err in errors:
            print(f"Path: {path}")
            print(json.dumps(err, indent=2, ensure_ascii=False)[:600])
            print("=" * 60)
            
        # Also print what n8n's internal execution state of node "6. Monday.com" looks like
        result_data = unflated_data.get("resultData", {})
        run_data = result_data.get("runData", {})
        if "6. Monday.com" in run_data:
            runs = run_data["6. Monday.com"]
            print(f"\nNode '6. Monday.com' has {len(runs)} runs")
            for idx, r in enumerate(runs):
                print(f"Run {idx} keys:", list(r.keys()))
                if r.get("error"):
                    print(f"Run {idx} Error:")
                    print(json.dumps(r["error"], indent=2, ensure_ascii=False))
                # Let's inspect the input data that was sent to the Monday node in this run
                input_data = r.get("data", {}).get("main", [[]])
                if input_data and input_data[0]:
                    print(f"Run {idx} first item keys:", list(input_data[0][0].get("json", {}).keys()))
    else:
        print("No error executions found")
except Exception as e:
    print("Error:", e)

conn.close()
