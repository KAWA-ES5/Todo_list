import json
import os

DATA_FILE = "todos.json"

def read_data():
    if not os.path.exists(DATA_FILE):
        return [] 
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def write_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)