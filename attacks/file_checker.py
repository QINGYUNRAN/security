import os
import hashlib


def calculate_sha256(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        while True:
            data = f.read(65536)
            if not data:
                break
            sha256_hash.update(data)
    return sha256_hash.hexdigest()


def check_integrity(directory_path):
    calculated_hash_all = []
    if not os.path.exists(directory_path) or not os.path.isdir(directory_path):
        print(f"Directory '{directory_path}' does not exist.")
        return
    for root, dirs, files in os.walk(directory_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            calculated_hash = calculate_sha256(file_path)
            print(f"File: {file_path}\nSHA-256 Hash; {calculated_hash}")
            calculated_hash_all.append(calculated_hash)
    return calculated_hash_all


# if __name__ == "__main__":
#     directory_to_check = input("Enter directory path to check integrity:")
#     original_all = check_integrity(directory_to_check)
#     if str(input("Check the integrity of the files?")) == "Y":
#         new_all = check_integrity(directory_to_check)
#     flag = True
#     for index, i in enumerate(original_all):
#         if i != new_all[index]:
#             flag = False
#             break
#     print(f"The integrity of file {index} is impaired.")
