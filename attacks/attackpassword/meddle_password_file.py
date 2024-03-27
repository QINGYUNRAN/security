import csv
import random
import string


def meddle(file_path):
    """
        Randomly alters the password of one user in a CSV file.

        Parameters:
        - file_path (str): Path to the CSV file containing user data.

        Behavior:
        - Reads user data from the file, selects a random user, and generates a new password.
        - Overwrites the original file with the modified user data, including the new password for the selected user.
        - Prints the username of the user whose password was altered.

    """
    with open(file_path, 'r+', newline='') as file:
        reader = csv.reader(file)
        writer = csv.writer(file)
        next(reader)
        rows = list(reader)
        if rows:
            random_user_index = random.randint(0, len(rows) - 1)
            random_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            print(f"Attack User '{rows[random_user_index][0]}'.")
            rows[random_user_index][1] = random_password
            file.seek(0)
            writer.writerows([["username", "password", "email"]] + rows)
