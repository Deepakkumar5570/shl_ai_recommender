import json
from pathlib import Path

RAW_PATH = "data/raw/shl_product_catalog.json"
OUTPUT_PATH = "data/processed/processed_catalog.json"

with open(RAW_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

processed = []

for item in data:
    text = f"""
    Name: {item.get('name', '')}
    Description: {item.get('description', '')}
    Job Levels: {', '.join(item.get('job_levels', []))}
    Keys: {', '.join(item.get('keys', []))}
    Languages: {', '.join(item.get('languages', []))}
    Duration: {item.get('duration', '')}
    """

    processed.append({
        "entity_id": item.get("entity_id"),
        "name": item.get("name"),
        "url": item.get("link"),
        "test_type": item.get("keys", [""])[0],
        "job_levels": item.get("job_levels", []),
        "keys": item.get("keys", []),
        "description": item.get("description", ""),
        "search_text": text
    })

Path("data/processed").mkdir(parents=True, exist_ok=True)

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(processed, f, indent=2)

print("Catalog preprocessing complete")