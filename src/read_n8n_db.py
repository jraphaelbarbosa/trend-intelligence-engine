import json

def unflatted(data):
    if not isinstance(data, list):
        return data
        
    # Reconstruct flatted structure
    # We will build a memoized mapping of indices to resolved objects
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
            resolved[idx] = res # Circular reference protection
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
            resolved[idx] = res # Circular reference protection
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

    # The root is the first element (index 0) or the element referenced by index 0 if index 0 is a digit string.
    # In n8n execution data, the first element is usually the root dictionary.
    return resolve("0")

# Test with our n8n db
import sqlite3
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

db_path = os.path.expanduser("~/.n8n/database.sqlite")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    cursor.execute("""
        SELECT e.id, e.status, e.workflowId, d.data 
        FROM execution_entity e
        JOIN execution_data d ON e.id = d.executionId
        WHERE e.status='error' 
        ORDER BY e.id DESC LIMIT 1;
    """)
    row = cursor.fetchone()
    if row:
        exec_id, status, wf_id, data_str = row
        data_json = json.loads(data_str)
        
        print("Unflating...")
        unflated_data = unflatted(data_json)
        
        print("Unflated type:", type(unflated_data))
        if isinstance(unflated_data, dict):
            print("Unflated keys:", list(unflated_data.keys()))
            
            # Let's save the unflated JSON
            with open("execution_error_unflated.json", "w", encoding="utf-8") as f:
                json.dump(unflated_data, f, indent=2, ensure_ascii=False)
            print("Wrote execution_error_unflated.json")
            
            # Look at resultData or executionData
            result_data = unflated_data.get("resultData", {})
            run_data = result_data.get("runData", {})
            print("Nodes in runData:", list(run_data.keys()))
            
            # Let's look for error in Monday.com or other nodes
            for node_name, runs in run_data.items():
                for i, r in enumerate(runs):
                    if r.get("error"):
                        print(f"\nNode '{node_name}' Run {i} Error:")
                        print(json.dumps(r["error"], indent=2, ensure_ascii=False))
                        
except Exception as e:
    import traceback
    print("Error:", e)
    traceback.print_exc()

conn.close()
