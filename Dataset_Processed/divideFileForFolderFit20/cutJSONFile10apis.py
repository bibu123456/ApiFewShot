import os
import shutil
import glob
import json

def limit_files_per_directory(directory_path, max_files_per_directory):
    # Lấy danh sách tất cả các thư mục con trong thư mục chính
    subdirectories = [d for d in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, d))]

    for subdirectory in subdirectories:
        # Tạo đường dẫn đầy đủ đến thư mục con
        subdirectory_path = os.path.join(directory_path, subdirectory)

        # Lấy danh sách tất cả các file JSON trong thư mục con
        json_files = glob.glob(os.path.join(subdirectory_path, '*.json'))

        # Tạo danh sách để lưu trữ các tệp JSON có ít hơn 10 phần tử trong mảng 'apis'
        json_files_less_than_10_apis = []

        # Lặp qua tất cả các tệp JSON và kiểm tra số phần tử trong mảng 'apis'
        for json_file in json_files:
            with open(json_file, 'r') as f:
                data = json.load(f)
                if 'apis' in data and len(data['apis']) < 10:
                    json_files_less_than_10_apis.append(json_file)

        # Nếu có tệp JSON có ít hơn 10 phần tử trong mảng 'apis', ưu tiên xóa chúng
        if json_files_less_than_10_apis:
            files_to_remove = json_files_less_than_10_apis
        else:
            # Nếu không có tệp nào ít hơn 10 phần tử, chọn tệp để xóa từ vị trí max_files_per_directory trở đi
            files_to_remove = json_files[max_files_per_directory:]

        # Xóa các tệp được chọn để duy trì không quá max_files_per_directory tệp trong thư mục con
        for file_to_remove in files_to_remove:
            os.remove(file_to_remove)

        print(f"Cắt bớt {len(files_to_remove)} file trong {subdirectory_path}")

# Thay đổi đường dẫn của bạn dưới đây
directory_path = 'D:/CreateDatasets/HKS/all/'
max_files_per_directory = 20

# Gọi hàm để cắt bớt số lượng file trong mỗi thư mục con
limit_files_per_directory(directory_path, max_files_per_directory)
