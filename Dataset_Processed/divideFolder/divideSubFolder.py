import os
import shutil

def split_folder(input_folder, output_folder, num_splits):
    # Kiểm tra và tạo thư mục đầu ra nếu chưa tồn tại
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Lấy danh sách các file trong thư mục đầu vào
    files = os.listdir(input_folder)
    num_files = len(files)

    # Tính số lượng file trong mỗi folder
    files_per_folder = num_files // num_splits

    # Lặp qua từng folder đầu ra
    for i in range(num_splits):
        # Tạo thư mục con
        subfolder = os.path.join(output_folder, f"Adware_{i + 1}")
        os.makedirs(subfolder)

        # Chọn các file cho thư mục con hiện tại
        start_idx = i * files_per_folder
        end_idx = start_idx + files_per_folder
        selected_files = files[start_idx:end_idx]

        # Di chuyển các file vào thư mục con
        for file_name in selected_files:
            file_path = os.path.join(input_folder, file_name)
            shutil.move(file_path, subfolder)

if __name__ == "__main__":
    # Thực hiện chia folder
    input_folder = "D:/CreateDatasets/new_datasets/HKS/all/Adware/"
    output_folder = "malware_0_split"
    num_splits = 30

    split_folder(input_folder, output_folder, num_splits)
