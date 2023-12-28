import os
import json
import csv

# Đọc dữ liệu từ file CSV
csv_file_path = 'VirusShare.csv'  # Thay đổi đường dẫn đến file CSV của bạn
with open(csv_file_path, 'r', encoding='utf-8-sig') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    # Dùng một từ điển để theo dõi các hàm theo class
    functions_by_class = {}

    for row in csv_reader:
        class_name = row.get('class')
        function_name = row.get('name')
        api_list = row.get('api').split(',')
        # Tạo hoặc cập nhật danh sách hàm cho class
        if class_name not in functions_by_class:
            functions_by_class[class_name] = []

        functions_by_class[class_name].append({'name': function_name, 'api': api_list})

    # Lặp qua từ điển và tạo các tệp JSON
    for class_name, functions in functions_by_class.items():
        # Tạo thư mục nếu chưa tồn tại
        os.makedirs(class_name, exist_ok=True)

        # Tạo tên tệp JSON dựa trên tên thư mục và ghi danh sách hàm vào tệp JSON
        json_file_path = os.path.join(class_name, f'{class_name}.json')
        with open(json_file_path, 'w') as json_file:
            json.dump(functions, json_file, indent=4)

print("Quá trình tạo thư mục và file JSON đã hoàn tất.")
