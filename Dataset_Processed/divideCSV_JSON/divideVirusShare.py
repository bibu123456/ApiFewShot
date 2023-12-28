import csv
import json
import os

def create_folders_and_json(data_file):
    # Đọc file CSV
    with open(data_file, 'r', encoding='utf-8-sig') as csv_file:
        reader = csv.reader(csv_file)
        header = next(reader)  # Lấy header

        print("CSV Header:", header)  # Print the header to identify column names

        # Tìm vị trí của cột sha256 và labels trong header
        name_column = next((i for i, v in enumerate(header) if v.strip().lower() == 'name'), None)
        api_column = next((i for i, v in enumerate(header) if v.strip().lower() == 'api'), None)
        class_column = next((i for i, v in enumerate(header) if v.strip().lower() == 'class'), None)

        # Kiểm tra xem có tồn tại cột cần thiết không
        if name_column is None or api_column is None or class_column is None:
            print("One or more required columns not found in the CSV file.")
            return

        # Tạo thư mục chính
        main_folder = 'malware_data3'
        os.makedirs(main_folder, exist_ok=True)

        # Đọc từng dòng của file CSV và tổ chức dữ liệu
        for row in reader:
            name_value = row[name_column]
            class_value = row[class_column]

            # Tạo thư mục cho loại malware nếu chưa tồn tại
            malware_folder = os.path.join(main_folder, f'{class_value}')
            os.makedirs(malware_folder, exist_ok=True)

            
            # Lọc ra các giá trị API không trống
            api_values = [api for api in row[api_column].split(',') if api.strip()]

            # Kiểm tra xem có ít nhất 10 giá trị API không trống
            if len(api_values) > 9 :
                json_data = {
                    'name': name_value,
                    'apis': api_values
                }

                # Tạo thư mục con theo name_value
                subfolder = os.path.join(malware_folder, f'{name_value}')
                os.makedirs(subfolder, exist_ok=True)

                # Tạo tên file và đường dẫn
                json_file_name = f'{name_value}.json'
                json_file_path = os.path.join(subfolder, json_file_name)

                # Ghi dữ liệu vào file JSON
                with open(json_file_path, 'w') as json_file:
                    json.dump(json_data, json_file, indent=2)

if __name__ == "__main__":
    data_file = 'VirusShare.csv'
    create_folders_and_json(data_file)
