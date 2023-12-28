import json

def load_json_file(file_path):
    with open(file_path, 'r') as file_path:
        data = json.load(file_path)
    return data

def filter_sequences(data, min_apis_count):
    filtered_sequences = [sequence for sequence in data if len(sequence['apis'].split(',')) >= min_apis_count]
    return filtered_sequences

def save_filtered_json(filtered_data, output_file_path):
    with open(output_file_path, 'w') as output_file:
        json.dump(filtered_data, output_file, indent=2)

# Thay đổi đường dẫn của file JSON và số lượng APIs tối thiểu ở đây
json_file_path = 'VirusShare.json'
min_apis_count = 10

# Load dữ liệu từ file JSON
data = load_json_file(json_file_path)

# Lọc ra các sequence thỏa mãn điều kiện
filtered_sequences = filter_sequences(data, min_apis_count)

# Lưu kết quả vào một file JSON mới (nếu cần)
output_file_path = 'VirusShareDrop.json'
save_filtered_json(filtered_sequences, output_file_path)
