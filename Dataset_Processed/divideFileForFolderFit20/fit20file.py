import os

def adjust_json_file_count(directory, target_mod):
    # Duyệt qua tất cả các thư mục con trong thư mục 'all'
    for folder in os.listdir(directory):
        folder_path = os.path.join(directory, folder)
        
        # Kiểm tra xem đối tượng có phải là thư mục không
        if os.path.isdir(folder_path):
            # Sử dụng list comprehension để đếm số lượng file JSON trong thư mục con
            json_files = [file for file in os.listdir(folder_path) if file.endswith('.json')]
            
            # Tính số lượng file cần giảm để chia hết cho target_mod
            reduction = len(json_files) % target_mod

            # Nếu không chia hết, giảm tỉ lệ theo số lượng file
            if reduction != 0:
                print(f"Giảm {reduction} file JSON trong thư mục '{folder}' để chia hết cho {target_mod}.")

                # Kiểm tra xem có đủ số lượng file để giảm không
                if reduction <= len(json_files):
                    # Sắp xếp danh sách file theo thời gian tạo và giữ lại (len(json_files) - reduction) file
                    json_files.sort(key=lambda x: os.path.getctime(os.path.join(folder_path, x)))
                    json_files_to_keep = json_files[reduction:]

                    # Xóa các file không cần thiết
                    for file in json_files:
                        if file not in json_files_to_keep:
                            os.remove(os.path.join(folder_path, file))

                    print(f"Số lượng file sau khi giảm: {len(os.listdir(folder_path))}")
                else:
                    print(f"Không đủ số lượng file để giảm trong thư mục '{folder}'.")
                    
                # Lặp lại quá trình nếu vẫn không chia hết cho target_mod
                while len(os.listdir(folder_path)) % target_mod != 0:
                    json_files = [file for file in os.listdir(folder_path) if file.endswith('.json')]
                    json_files.sort(key=lambda x: os.path.getctime(os.path.join(folder_path, x)))
                    os.remove(os.path.join(folder_path, json_files[0]))
                    print(f"Giảm thêm 1 file để chia hết cho {target_mod}.")

# Đường dẫn đến thư mục 'all'
all_folder_path = r"D:/CreateDatasets/new_datasets/HKS/all/"

# Gọi hàm để kiểm tra và điều chỉnh số lượng file JSON
adjust_json_file_count(all_folder_path, 20)
