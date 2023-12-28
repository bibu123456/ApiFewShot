import os
import shutil
import glob

def limit_files_per_directory(directory_path, max_files_per_directory):
    # Lấy danh sách tất cả các thư mục con trong thư mục chính
    subdirectories = [d for d in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, d))]

    for subdirectory in subdirectories:
        # Tạo đường dẫn đầy đủ đến thư mục con
        subdirectory_path = os.path.join(directory_path, subdirectory)

        # Lấy danh sách tất cả các file JSON trong thư mục con
        json_files = glob.glob(os.path.join(subdirectory_path, '*.json'))

        # Nếu có nhiều hơn max_files_per_directory file, cắt bớt
        if len(json_files) > max_files_per_directory:
            files_to_remove = json_files[max_files_per_directory:]
            for file_to_remove in files_to_remove:
                os.remove(file_to_remove)

            print(f"Cắt bớt {len(files_to_remove)} file trong {subdirectory_path}")

# Thay đổi đường dẫn của bạn dưới đây
directory_path = 'D:/CreateDatasets/HKS/all/'
max_files_per_directory = 20

# Gọi hàm để cắt bớt số lượng file trong mỗi thư mục con
limit_files_per_directory(directory_path, max_files_per_directory)
