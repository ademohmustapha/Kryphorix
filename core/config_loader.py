import json
import os

DEFAULT_CONFIG = {
    "threads": 5,
    "timeout": 5,
    "report_format": "pdf"
}

def load_config(path="config.json"):
    if not os.path.exists(path):
        print("[!] config.json not found. Using default settings.")
        return DEFAULT_CONFIG

    try:
        with open(path, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("[!] config.json is invalid. Using default settings.")
        return DEFAULT_CONFIG

