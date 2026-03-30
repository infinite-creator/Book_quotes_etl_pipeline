import json

def load_raw_data_to_json(raw_quotes, json_path):
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(raw_quotes, f, ensure_ascii=False, indent=2)

