import json

def remove_duplicate_apis(data):
    seen_apis = set()
    unique_entries = []

    for entry in data:
        apis = entry["apis"].split(',')
        unique_apis = [api.strip() for api in apis if api.strip() not in seen_apis]
        
        if unique_apis:
            entry["apis"] = ','.join(unique_apis)
            seen_apis.update(unique_apis)
            unique_entries.append(entry)

    return unique_entries

def load_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def save_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

if __name__ == "__main__":
    input_file_path = "path/to/your/input/file.json"
    output_file_path = "path/to/your/output/file.json"

    # Load JSON data
    json_data = load_json(input_file_path)

    # Remove duplicate APIs, keeping the first occurrence
    unique_data = remove_duplicate_apis(json_data)

    # Save the result to a new JSON file
    save_json(output_file_path, unique_data)
