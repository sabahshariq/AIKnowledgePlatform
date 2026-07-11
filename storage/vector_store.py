import json

def save_embeddings(data, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def load_embeddings(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)