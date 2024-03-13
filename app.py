import smtplib
from flask import (
    Flask,
    render_template,
    render_template_string,
    request,
    redirect,
    url_for,
    session,
    flash,
)
import html
import argparse
import pyotp
from email.header import Header
from email.mime.text import MIMEText
from pynput import keyboard
import scapy.all as scapy
import re
import pandas as pd
from file_checker import check_integrity
import os
from func.database import get_data_from_mysql
from func.keyPressed import keyPressed

# employee_records = pd.read_csv("data/data/employees.csv").to_dict(orient='records')
# checkin_records = pd.read_csv("data/data/checkIn.csv").to_dict(orient='records')
# salary_records = pd.read_csv("data/data/salary.csv").to_dict(orient='records')
# holidays_records = pd.read_csv("data/data/holidays.csv").to_dict(orient='records')
employee_records, checkin_records, salary_records, holidays_records = (
    get_data_from_mysql()
)

current_dir = os.path.dirname(__file__)
account_file_path = os.path.join(current_dir, "files/account.csv")


app = Flask(__name__)
app.secret_key = "1"
app.config["XSS_ENABLED"] = False
app.config["KEYLOGGER_ENABLED"] = False
app.config["FILECHECK_ENABLED"] = False
app.config["WIFISCANNER_ENABLED"] = False


@app.route("/")
def index():
    session.clear()
    return redirect(url_for("login"))


key = (
    pyotp.random_base32()
)  # same key create same password, no one else can get the key
# print(key)
totp = pyotp.TOTP(key)


@app.route("/pythonlogin/", methods=["GET", "POST"])
def login():
    # Check if "username" and "password" POST requests exist (user submitted form)
    print(request.method)
    if (
        request.method == "POST"
        and "username" in request.form
        and "password" in request.form
    ):
        username = request.form["username"]
        password = request.form["password"]
        if os.path.exists(account_file_path) and os.path.getsize(account_file_path) > 0:
            df_accounts = pd.read_csv(account_file_path)
            df_accounts = df_accounts.astype(str)
        else:
            flash("No accounts found. Please register first.", "warning")
            return redirect(url_for("register"))
        user = df_accounts[
            (df_accounts["username"] == username)
            & (df_accounts["password"] == password)
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
    if request.method == "POST" and "vercode" in request.form:
        vercode = request.form["vercode"]
        if vercode == session["vercode"]:
            # 2FA email verification
            session["loggedin"] = True
            return redirect(url_for("home"))
        else:
            session.pop("username", None)
            flash("Incorrect verification code!", "warning")
    return render_template("auth/verify.html", title="Verify")


@app.route("/pythonlogin/register", methods=["GET", "POST"])
def register():
    if (
        request.method == "POST"
        and "username" in request.form
        and "password" in request.form
        and "email" in request.form
    ):
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        if os.path.exists(account_file_path) and os.path.getsize(account_file_path) > 0:
            df_accounts = pd.read_csv(account_file_path)
            df_accounts = df_accounts.astype(str)
        else:
            df_accounts = pd.DataFrame(columns=["username", "password", "email"])

        if username in df_accounts["username"].values:
            flash("Account already exists!", "warning")
        else:
            new_user_df = pd.DataFrame(
                [{"username": username, "password": password, "email": email}]
            )
            df_accounts = pd.concat([df_accounts, new_user_df], ignore_index=True)
            df_accounts.to_csv(account_file_path, index=False)
            return redirect(url_for("login"))
    return render_template("auth/register.html", title="Register")


@app.route("/home")
def home():

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
    if "loggedin" in session and session["loggedin"] == True:
        username = html.escape(session["username"])
        records = checkin_records
        return render_template(
            "home/checkin.html", username=username, records=records, title="checkin"
        )
    return redirect(url_for("login"))


@app.route("/holidays")
def holidays():
    if "loggedin" in session and session["loggedin"] == True:
        username = html.escape(session["username"])
        records = holidays_records
        return render_template(
            "home/holidays.html", username=username, records=records, title="holidays"
        )
    return redirect(url_for("login"))


@app.route("/salary")
def salary():
    if "loggedin" in session and session["loggedin"] == True:
        username = html.escape(session["username"])
        records = salary_records
        return render_template(
            "home/salary.html", username=username, records=records, title="salary"
        )
    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.pop("loggedin", None)
    session.pop("id", None)
    session.pop("username", None)
    return redirect(url_for("login"))


@app.route("/change_password", methods=["GET", "POST"])
def change_password():
    if "loggedin" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        current_password = request.form["current_password"]
        new_password = request.form["new_password"]
        repeat_new_password = request.form["repeat_new_password"]
        username = session["username"]
        accounts_df = pd.read_csv(account_file_path)
        accounts_df = accounts_df.astype(str)
        user_row = accounts_df.loc[accounts_df["username"] == username]

        if not user_row.empty and user_row.iloc[0]["password"] == current_password:
            if new_password == repeat_new_password:
                accounts_df.loc[accounts_df["username"] == username, "password"] = (
                    new_password
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
    elif args.filecheck == True:
        directory_to_check = input("Enter directory path to check integrity:")
        original_all = check_integrity(directory_to_check)
        if str(input("Check the integrity of the files?")) == "Y":
            new_all = check_integrity(directory_to_check)
        flag = True
        for index, i in enumerate(original_all):
            if i != new_all[index]:
                flag = False
                break
        if flag == False:
            print(f"The integrity of file {index} is impaired.")
        else:
            print("All files are integral.")

    else:
        if args.keylogger == True:
            listener = keyboard.Listener(
                on_press=keyPressed
            )  # everytime the key is pressed, passed information to keypressed function
            listener.start()
    app.config["XSS_ENABLED"] = args.xss
    app.config["KEYLOGGER_ENABLED"] = args.keylogger
    app.config["FILECHECK_ENABLED"] = args.filecheck
    app.config["WIFISCANNER_ENABLED"] = args.wifiscanner
    app.run(debug=True)


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
