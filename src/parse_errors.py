import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("execution_error_unflated.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("Root Keys:", list(data.keys()))

# Check executionData
exec_data = data.get("executionData", {})
print("\nexecutionData keys:", list(exec_data.keys()) if isinstance(exec_data, dict) else "Not a dict")
if isinstance(exec_data, dict) and "error" in exec_data:
    print("executionData.error:")
    print(json.dumps(exec_data["error"], indent=2, ensure_ascii=False))

# Recursive search for all errors/failures in the JSON
errors = []
def find_errors(obj, path=""):
    if isinstance(obj, dict):
        # Look for keys like error, message, description, stack
        for k in ["error", "message", "description", "stack", "reason", "errorMessage"]:
            if k in obj and obj[k]:
                errors.append((f"{path}/{k}", obj[k]))
        for k, v in obj.items():
            find_errors(v, f"{path}/{k}")
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            find_errors(item, f"{path}[{i}]")

find_errors(data)

print(f"\nFound {len(errors)} potential error/status fields in JSON:")
for path, err in errors:
    # Print only if it has interesting details or traceback
    err_str = str(err)
    if any(word in err_str.lower() for word in ["error", "fail", "invalid", "reject", "missing", "bad", "connect", "monday"]):
        print(f"\nPath: {path}")
        print(json.dumps(err, indent=2, ensure_ascii=False)[:1000])
        print("="*60)
    elif "message" in path or "stack" in path:
        print(f"\nPath: {path}")
        print(json.dumps(err, indent=2, ensure_ascii=False)[:1000])
        print("="*60)
