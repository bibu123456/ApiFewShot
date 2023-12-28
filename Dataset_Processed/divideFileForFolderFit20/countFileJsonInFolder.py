import os

def count_json_files(directory):
    # Duyệt qua tất cả các thư mục con trong thư mục 'all'
    for folder in os.listdir(directory):
        folder_path = os.path.join(directory, folder)
        
        # Kiểm tra xem đối tượng có phải là thư mục không
        if os.path.isdir(folder_path):
            # Sử dụng list comprehension để đếm số lượng file JSON trong thư mục con
            json_files = [file for file in os.listdir(folder_path) if file.endswith('.json')]
            
            # In ra số lượng file JSON trong thư mục con
            print(f"Thư mục '{folder}' có {len(json_files)} file JSON.")

# Đường dẫn đến thư mục 'all'
all_folder_path = r"D:/CreateDatasets/HKS/all/"

# Gọi hàm để đếm số lượng file JSON trong mỗi thư mục con
count_json_files(all_folder_path)
