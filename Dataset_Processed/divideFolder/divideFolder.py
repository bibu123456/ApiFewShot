import os
import shutil

def split_folder(input_folder, num_splits):
    # Lấy đường dẫn tới thư mục chứa thư mục 'all'
    parent_folder = os.path.dirname(os.path.dirname(input_folder))

    # Lấy danh sách các file trong thư mục đầu vào
    files = os.listdir(input_folder)
    num_files = len(files)

    # Tính số lượng file trong mỗi folder
    files_per_folder = num_files // num_splits

    # Lặp qua từng folder đầu ra
    for i in range(num_splits):
        # Tạo thư mục con
        subfolder = os.path.join(parent_folder, f"Worms_{i + 1}")
        os.makedirs(subfolder, exist_ok=True)

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
    input_folder = "D:/CreateDatasets/new_datasets/HKS/all/Worms/"
    num_splits = 9

    split_folder(input_folder, num_splits)
