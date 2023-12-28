import os
import shutil

def create_adware1_folder(src_folder, dest_folder):
    # Kiểm tra xem thư mục nguồn có tồn tại không
    if not os.path.exists(src_folder):
        print(f"Thư mục nguồn {src_folder} không tồn tại.")
        return
    
    # Tạo thư mục mới (Adware1)
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
        print(f"Đã tạo thư mục {dest_folder}")
    
    # Lặp qua các thư mục con trong thư mục nguồn
    for subfolder in os.listdir(src_folder):
        subfolder_path = os.path.join(src_folder, subfolder)
        
        # Kiểm tra xem đối tượng có phải là thư mục không
        if os.path.isdir(subfolder_path):
            # Tìm file JSON trong thư mục con
            json_file = os.path.join(subfolder_path, f"{subfolder}.json")
            
            # Kiểm tra xem file JSON có tồn tại không
            if os.path.exists(json_file):
                # Di chuyển file JSON vào thư mục mới (Adware1)
                shutil.copy(json_file, dest_folder)
                print(f"Đã di chuyển file {json_file} vào {dest_folder}")

# Đường dẫn của thư mục Adware
adware_folder = r"D:/CreateDatasets/malware_data2/Worms/"

# Đường dẫn của thư mục Adware mới
adware1_folder = r"D:/CreateDatasets/new_datasets/HKS/all/Worms/"

# Gọi hàm để tạo thư mục Adware mới và di chuyển file JSON
create_adware1_folder(adware_folder, adware1_folder)