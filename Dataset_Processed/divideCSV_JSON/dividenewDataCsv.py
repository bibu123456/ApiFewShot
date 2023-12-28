import csv
import json
import os

def create_folders_and_json(data_file):
    # Đọc file CSV
    with open(data_file, 'r') as csv_file:
        reader = csv.reader(csv_file)
        header = next(reader)  # Lấy header

        # Tìm vị trí của cột hash và malware trong header
        hash_column = header.index('hash')
        malware_column = header.index('malware')

        # Tạo thư mục chính
        main_folder = 'malware_data'
        os.makedirs(main_folder, exist_ok=True)

        # Đọc từng dòng của file CSV và tổ chức dữ liệu
        for row in reader:
            hash_value = row[hash_column]
            malware_type = row[malware_column]

            # Tạo thư mục cho loại malware nếu chưa tồn tại
            malware_folder = os.path.join(main_folder, f'malware_{malware_type}')
            os.makedirs(malware_folder, exist_ok=True)

            # Tạo đối tượng JSON
            api_values = [int(api) for api in row[2:151] if api.isdigit()]

            # Kiểm tra số lượng số trong api_values
            if len(api_values) >= 10:
                json_data = {
                    'name': hash_value,
                    'apis': api_values
                }

                # Tạo tên file và đường dẫn
                json_file_name = f'{hash_value}.json'
                json_file_path = os.path.join(malware_folder, json_file_name)

                # Ghi dữ liệu vào file JSON
                with open(json_file_path, 'w') as json_file:
                    json.dump(json_data, json_file, indent=2)

if __name__ == "__main__":
    data_file = 'new_dataset.csv'
    create_folders_and_json(data_file)
