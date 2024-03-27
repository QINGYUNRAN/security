import smtplib
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    jsonify,
)
import html
import argparse
import pyotp
from email.header import Header
from email.mime.text import MIMEText
from pynput import keyboard
import scapy.all as scapy
import re
import hashlib
import pandas as pd
import os, csv
from attacks.attackpassword.meddle_password_file import meddle
from attacks.file_checker import check_integrity
from func.keyPressed import keyPressed
from func.check_ip import check_ip_limit
import time
from attacks.ml_detector.utils import load_data, process_wireshark
from attacks.ml_detector.attack_detector import AttackDetector


employee_records = pd.read_csv("data/data/employees.csv").to_dict(orient='records')
checkin_records = pd.read_csv("data/data/checkIn.csv").to_dict(orient='records')
salary_records = pd.read_csv("data/data/salary.csv").to_dict(orient='records')
holidays_records = pd.read_csv("data/data/holidays.csv").to_dict(orient='records')
# employee_records, checkin_records, salary_records, holidays_records = (
#     get_data_from_mysql()
# )

current_dir = os.path.dirname(__file__)
account_file_path = os.path.join(current_dir, "files/account.csv")


app = Flask(__name__)
app.secret_key = "1"
app.config["XSS_ENABLED"] = False
app.config["KEYLOGGER_ENABLED"] = False
app.config["FILECHECK_ENABLED"] = False
app.config["WIFISCANNER_ENABLED"] = False
app.config["MLDETECTOR_ENABLED"] = False


ip_access_records = {}
banned_ips = {}


def rate_limiter(func):
    """
       Decorator that limits the rate of requests to the decorated function based on the requester's IP address.
       If the number of requests exceeds a threshold within a certain time period, access is denied.

       Args:
           func (function): The function to be decorated and subject to rate limiting.

       Returns:
           function: A wrapper function that implements the rate limiting logic. If the request is allowed,
           it calls the original function; otherwise, it returns an error response.
    """
    def wrapper(*args, **kwargs):
        ip_address = request.remote_addr
        current_time = time.time()

        if ip_address in banned_ips and current_time < banned_ips[ip_address]:
            return jsonify({"error": "Access denied"}), 403

        record = ip_access_records.get(
            ip_address, {"last_access": 0, "attempt_count": 0}
        )
        time_since_last_access = current_time - record["last_access"]
        if time_since_last_access < 10:
            record["attempt_count"] += 1
            if record["attempt_count"] > 20:  # 超过20次尝试，禁止一个小时
                banned_ips[ip_address] = current_time + 3600  # 禁止一小时
                return (
                    jsonify({"error": "Too many requests, access denied for 1 hour"}),
                    429,
                )
            else:
                return jsonify({"error": "Too many requests"}), 429
        else:
            record["last_access"] = current_time
            record["attempt_count"] = 1

        ip_access_records[ip_address] = record
        return func(*args, **kwargs)

    return wrapper


@app.route("/")
@rate_limiter
def index():
    """
        The index route that clears the session and redirects to the login page.
        This route is protected by a rate limiter.

        Returns:
            Redirect: A redirection to the login URL.
    """
    session.clear()
    return redirect(url_for("login"))


key = (
    pyotp.random_base32()
)  # same key create same password, no one else can get the key
# print(key)
totp = pyotp.TOTP(key)


@app.route("/pythonlogin/", methods=["GET", "POST"])
def login():
    """
        The login route allows users to log in by submitting a username and password.
        It implements rate limiting based on IP address and additional logic for user authentication.
        If the credentials are correct, a verification code is sent to the user's email.

        Returns:
            RenderTemplate or Redirect: Renders the login template on a GET request or unsuccessful login attempt.
            On successful login, redirects to the verification code input page.
    """
    ip_address = request.remote_addr
    if not check_ip_limit(ip_address):
        flash("Too many login attempts. Please try again later.", "warning")
        return render_template("auth/login.html", title="Login")
    if (
        request.method == "POST"
        and "username" in request.form
        and "password" in request.form
    ):
        username = request.form["username"]
        password = request.form["password"]
        hashed_password = hashlib.md5(password.encode()).hexdigest()

        if os.path.exists(account_file_path) and os.path.getsize(account_file_path) > 0:
            df_accounts = pd.read_csv(account_file_path)
            df_accounts = df_accounts.astype(str)
        else:
            flash("No accounts found. Please register first.", "warning")
            return redirect(url_for("register"))
        user = df_accounts[
            (df_accounts["username"] == username)
            & (df_accounts["password"] == hashed_password)
        ]
        if not user.empty:
            ver_code = totp.now()
            print(ver_code)  # time base for 30 seconds, after that it will exceeed

            # send to your email box
            from_addr = "2387324762@qq.com"
            email_password = "pdewxqltfshtebia"
            # to_addr = "2387324762@qq.com"
            to_addr = user["email"].iloc[0]
            smtp_server = "smtp.qq.com"

            msg = MIMEText(
                f"Dear Sir/Madam,\n"
                + "  "
                + f"Your veification code is {ver_code}."
                + "\n"
                "\n"
                "Best regards,\n"
                "Message from ",  # company name
                "plain",
                "utf-8",
            )
            msg["From"] = Header(from_addr)
            msg["To"] = Header(to_addr)
            subject = f"Verification code message"
            msg["Subject"] = Header(subject, "utf-8")

            try:
                smtpobj = smtplib.SMTP_SSL(smtp_server)
                smtpobj.connect(smtp_server, 465)
                smtpobj.login(from_addr, email_password)
                smtpobj.sendmail(from_addr, to_addr, msg.as_string())
                print("Send successfully")
            except smtplib.SMTPException:
                print("Fail to send")
            finally:
                smtpobj.quit()
            session["username"] = username
            session["vercode"] = ver_code
            print(session)
            flash("Correct password, please input your verification code", "warning")
            return redirect(url_for("verify"))
        else:
            flash("Incorrect username/password!", "warning")
    return render_template("auth/login.html", title="Login")


@app.route("/pythonlogin/verify", methods=["GET", "POST"])
def verify():
    """
       This function processes the user's input verification code (vercode) submitted through a form.
       If the method is POST and the 'vercode' is present in the form, it checks if the provided
       verification code matches the one stored in the session ('vercode'). If they match, it sets
       the session's 'loggedin' status to True and redirects the user to the home page. If they don't
       match, or if the request method is GET, it renders the 'auth/verify.html' template. For incorrect
       codes, it flashes a warning message.

       Returns:
       - Redirects to the home page if verification code matches the session code.
       - Renders the verification page with a warning message for incorrect verification code.
   """
    if request.method == "POST" and "vercode" in request.form:
        vercode = request.form["vercode"]
        if vercode == session["vercode"]:
            # 2FA email verification
            session["loggedin"] = True
            return redirect(url_for("home"))
        else:
            session["loggedin"] = False
            flash("Incorrect verification code!", "warning")
    return render_template("auth/verify.html", title="Verify")


@app.route("/pythonlogin/register", methods=["GET", "POST"])
def register():
    """
        This function facilitates the registration of a new user. It checks if the request method is POST
        and if the required fields ('username', 'password', 'email') are provided in the form. If so, it
        hashes the password using MD5 and checks if the username already exists in the database (a CSV file
        in this context). If the username exists, it flashes a warning message. Otherwise, it adds the new user
        to the database and redirects to the login page. For GET requests or if the username already exists, it
        renders the 'auth/register.html' template.

        Returns:
        - On successful registration, redirects to the login page.
        - If the username already exists, renders the registration page with a warning message.
        - On GET request, simply renders the registration page without any message.
    """
    if (
        request.method == "POST"
        and "username" in request.form
        and "password" in request.form
        and "email" in request.form
    ):
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        # Hash the password using MD5
        hashed_password = hashlib.md5(password.encode()).hexdigest()
        if os.path.exists(account_file_path) and os.path.getsize(account_file_path) > 0:
            df_accounts = pd.read_csv(account_file_path)
            df_accounts = df_accounts.astype(str)
        else:
            df_accounts = pd.DataFrame(columns=["username", "password", "email"])

        if username in df_accounts["username"].values:
            flash("Account already exists!", "warning")
        else:
            new_user_df = pd.DataFrame(
                [{"username": username, "password": hashed_password, "email": email}]
            )
            df_accounts = pd.concat([df_accounts, new_user_df], ignore_index=True)
            df_accounts.to_csv(account_file_path, index=False)
            return redirect(url_for("login"))
    return render_template("auth/register.html", title="Register")


@app.route("/home")
def home():
    """
        Renders the home page for logged-in users.

        - If XSS protection is enabled, sanitizes the username.
        - Shows employee records.
        - Redirects to login if not logged in.
    """
    if "loggedin" in session and session["loggedin"] == True:
        if app.config["XSS_ENABLED"] == True:
            username = session["username"]
            records = employee_records
            return f"{username}"
        else:
            username = html.escape(session["username"])
            records = employee_records
            return render_template(
                "home/home.html", username=username, records=records, title="Home"
            )
    return redirect(url_for("login"))


@app.route("/profile")
def profile():
    """
        Displays the user's profile page with account details for logged-in users.

        - Retrieves user account details from a CSV file.
        - Redirects to login if not logged in.
    """
    # Check if user is loggedin
    if "loggedin" in session and session["loggedin"] == True:
        df_accounts = pd.read_csv(account_file_path)
        df_accounts = df_accounts.astype(str)
        account = df_accounts[df_accounts["username"] == session["username"]]
        if not account.empty:
            account = account.iloc[0].to_dict()
            return render_template(
                "auth/profile.html", account=account, title="Profile"
            )
    return redirect(url_for("login"))


@app.route("/checkin")
def checkin():
    """
        Renders the check-in page for logged-in users.

        - Shows check-in records.
        - Redirects to login if not logged in.
    """
    if "loggedin" in session and session["loggedin"] == True:
        username = html.escape(session["username"])
        records = checkin_records
        return render_template(
            "home/checkin.html", username=username, records=records, title="checkin"
        )
    return redirect(url_for("login"))


@app.route("/holidays")
def holidays():
    """
        Displays the holidays page for logged-in users.

        - Shows holidays records.
        - Redirects to login if not logged in.
    """
    if "loggedin" in session and session["loggedin"] == True:
        username = html.escape(session["username"])
        records = holidays_records
        return render_template(
            "home/holidays.html", username=username, records=records, title="holidays"
        )
    return redirect(url_for("login"))


@app.route("/salary")
def salary():
    """
        Renders the salary page for logged-in users.

        - Shows salary records.
        - Redirects to login if not logged in.
    """
    if "loggedin" in session and session["loggedin"] == True:
        username = html.escape(session["username"])
        records = salary_records
        return render_template(
            "home/salary.html", username=username, records=records, title="salary"
        )
    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    """
        Logs out the user.

        - Clears the session.
        - Redirects to the login page.
    """
    session.pop("loggedin", None)
    session.pop("id", None)
    session.pop("username", None)
    return redirect(url_for("login"))


@app.route("/change_password", methods=["GET", "POST"])
def change_password():
    """
        Handles password change requests for logged-in users.

        - Validates current password and ensures new passwords match.
        - Updates the user's password in the CSV database if validations pass.
        - Redirects to the profile page on successful password change.
        - Shows warnings for incorrect current password or non-matching new passwords.
        - Redirects to login if not logged in.
    """
    if "loggedin" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        current_password = request.form["current_password"]
        new_password = request.form["new_password"]
        repeat_new_password = request.form["repeat_new_password"]
        username = session["username"]
        accounts_df = pd.read_csv(account_file_path)
        accounts_df = accounts_df.astype(str)
        hashed_current_password = hashlib.md5(current_password.encode()).hexdigest()

        user_row = accounts_df.loc[accounts_df["username"] == username]

        if not user_row.empty and user_row.iloc[0]["password"] == hashed_current_password:
            if new_password == repeat_new_password:
                hashed_new_password = hashlib.md5(new_password.encode()).hexdigest()
                accounts_df.loc[accounts_df["username"] == username, "password"] = (
                    hashed_new_password
                )
                accounts_df.to_csv(account_file_path, index=False)
                return redirect(url_for("profile"))
            else:
                flash("New passwords do not match.", "warning")
        else:
            flash("Current password is incorrect.", "warning")

    return render_template("home/change_password.html")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Argparse")
    parser.add_argument(
        "--xss", default=False, type=bool, help="whether set xss attacks"
    )
    parser.add_argument(
        "--keylogger", default=False, type=bool, help="whether set key logger"
    )
    parser.add_argument(
        "--filecheck", default=False, type=bool, help="whether check file integrity"
    )
    parser.add_argument(
        "--wifiscanner", default=False, type=bool, help="whether scan wifi network"
    )
    parser.add_argument("--mldetector", default=None, type=str, help="SVM,RF,LR,KNN")
    parser.add_argument(
        "--train", default=False, type=bool, help="whether train the model"
    )
    args = parser.parse_args()
    if args.wifiscanner == True:
        ip_add_range_pattern = re.compile("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}/[0-9]*$")
        while True:
            ip_add_range_entered = input(
                "\nPlease enter the ip address and range that you want to send the ARP request to (ex 192.168.1.0/24): "
            )
            if ip_add_range_pattern.search(ip_add_range_entered):
                print(f"{ip_add_range_entered} is a valid ip address range")
                break
        arp_result = scapy.arping(ip_add_range_entered)

    # file check may need to combine with database

    if args.filecheck == True:
        csv_file = input("Enter the path to the CSV file: ")
        original_hash_all = check_integrity(csv_file)
        if original_hash_all:
            print("Original file checked.")

        meddle_file = input("Do you want to meddle with the file? (Y/N): ")
        if meddle_file.upper() == 'Y':
            meddle(csv_file)

        with open(csv_file, 'r', newline='') as file:
            reader = csv.reader(file)
            next(reader)
            modified_hash_all = check_integrity(csv_file)
            if original_hash_all and modified_hash_all:
                for orig_hash, mod_hash, row in zip(original_hash_all, modified_hash_all, reader):
                    if orig_hash != mod_hash:
                        print(f"User '{row[0]}' with email '{row[2]}' has been modified.")

    if args.keylogger == True:
        listener = keyboard.Listener(
            on_press=keyPressed
        )  # everytime the key is pressed, passed information to keypressed function
        listener.start()
    elif args.mldetector != None:
        detector = AttackDetector(args.mldetector)
        if args.train == True:
            # data preprocessing
            X, y, preprocessor = load_data("attacks/ml_detector/network_traffic.csv")
            # train
            detector.train(X, y, preprocessor)

        # test
        for i in os.listdir("attacks/ml_detector/output"):
            print("\nReading Wireshark output file...")
            file_path = os.path.expanduser(f"attacks/ml_detector/output/{i}")
            wireshark_df = process_wireshark(file_path)
            detector.test(wireshark_df)

    app.config["XSS_ENABLED"] = args.xss
    app.config["KEYLOGGER_ENABLED"] = args.keylogger
    app.config["FILECHECK_ENABLED"] = args.filecheck
    app.config["WIFISCANNER_ENABLED"] = args.wifiscanner
    app.config["MLDETECTOR_ENABLED"] = args.mldetector
    app.run(
        ssl_context=("attacks/https_cert/cert.pem", "attacks/https_cert/key.pem"),
        debug=True,
    )  # dummy: adhoc

    # create own certificate


# # 2FA in python
# import time
# import pyotp
# key = pyotp.random_base32  # same key create same password, no one else can get the key
# print(key)
# # key = "mysuperkey" # can also generate manually
# totp = pyotp.TOTP(key)
# print(totp.now())  # time base for 30 seconds, after that it will exceeed

# time.sleep(30)
# print(totp.now())  # 30 seconds later, exceed

# input_code = input("Enter your 2FA Code.")
# print(totp.verify(input_code)) # verify whether the code is the same with the input one


# # counter based
# counter = 0
# hotp = pyotp.HOTP(key)
# print(hotp.at(0))
# print(hotp.at(1))
# print(hotp.at(2))
# print(hotp.at(3))
# print(hotp.at(4))
# # based on counter number

# for _ in range(5):
#     print(hotp.verify(input("enter code"), counter))
#     counter += 1
