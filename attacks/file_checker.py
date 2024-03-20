import os
import hashlib
import csv


def calculate_sha256(data):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(data.encode('utf-8'))
    return sha256_hash.hexdigest()

def check_integrity(file_path):
    calculated_hash_all = []
    if not os.path.exists(file_path):
        print(f"File '{file_path}' does not exist.")
        return None
    with open(file_path, 'r', newline='') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            username, password, email = row
            calculated_hash = calculate_sha256(f"{username},{password},{email}")
            # print(f"Username: {username}, Password: {password}, Email: {email}, Hash: {calculated_hash}")
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
