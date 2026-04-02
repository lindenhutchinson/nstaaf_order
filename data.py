import json

DATA_FILE = "fish_episode_info.json"

def load_episode_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
