import os

def count_subdirectories(path):
    # Kiểm tra xem đường dẫn có tồn tại không
    if not os.path.exists(path):
        print("Đường dẫn không tồn tại.")
        return

    # Bắt đầu đếm số thư mục con
    count = 0
    for root, dirs, files in os.walk(path):
        # Thêm số lượng thư mục con
        count += len(dirs)

    return count

# Thay đổi đường dẫn này thành thư mục bạn muốn kiểm tra
directory_path = "D:/CreateDatasets/new_datasets/HKS/all/"
result = count_subdirectories(directory_path)

print(f"Số thư mục con trong '{directory_path}': {result}")
