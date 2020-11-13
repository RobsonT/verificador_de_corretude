import json

def fileHandle(data):
    with open('./files/response.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
