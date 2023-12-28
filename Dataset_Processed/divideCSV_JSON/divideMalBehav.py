import csv
import json
import os

def create_folders_and_json(data_file):
    # Đọc file CSV
    with open(data_file, 'r', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        header = next(reader)  # Lấy header

        # Tìm vị trí của cột sha256 và labels trong header
        sha256_column = header.index('sha256')
        labels_column = header.index('labels')

        # Tạo thư mục chính
        main_folder = 'malware_data1'
        os.makedirs(main_folder, exist_ok=True)

        # Đọc từng dòng của file CSV và tổ chức dữ liệu
        for row in reader:
            sha256_value = row[sha256_column]
            labels_value = row[labels_column]

            # Tạo thư mục cho loại malware nếu chưa tồn tại
            malware_folder = os.path.join(main_folder, f'malware_{labels_value}')
            os.makedirs(malware_folder, exist_ok=True)

            # Lọc ra các giá trị API không trống
            api_values = [api for api in row[2:] if api.strip()]

            # Kiểm tra xem có ít nhất 1 giá trị API không trống
            if api_values:
                json_data = {
                    'name': sha256_value,
                    'apis': api_values
                }

                # Tạo tên file và đường dẫn
                json_file_name = f'{sha256_value}.json'
                json_file_path = os.path.join(malware_folder, json_file_name)

                # Ghi dữ liệu vào file JSON
                with open(json_file_path, 'w') as json_file:
                    json.dump(json_data, json_file, indent=2)

if __name__ == "__main__":
    data_file = 'MalBehavD-V1-dataset.csv'
    create_folders_and_json(data_file)
