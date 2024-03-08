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
import re
import html
import argparse
import time
import pyotp
from email.header import Header
from email.mime.text import MIMEText
from pynput import keyboard

from file_checker import check_integrity

parser = argparse.ArgumentParser(description="Argparse")
parser.add_argument("--xss", default=False, type=bool, help="whether set xss attacks")
parser.add_argument(
    "--keylogger", default=False, type=bool, help="whether set key logger"
)
parser.add_argument(
    "--filecheck", default=False, type=bool, help="whether check file integrity"
)
args = parser.parse_args()
app = Flask(__name__)
app.secret_key = "1"

account = {
    "username1": {
        "username": "username1",
        "password": "password1",
        "email": "email1@example.com",
    },
    "username2": {
        "username": "username2",
        "password": "password2",
        "email": "email2@example.com",
    },
    "ran": {"username": "ran", "password": "123", "email": "123@mail.com"},
}
user_info = {
    "ran": [
        {"date": "2024-02-29", "attendance": True, "reason": "Worked on project X"},
        {"date": "2024-03-01", "attendance": False, "reason": "Sick leave"},
    ],
}


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
        user = account.get(username)
        print(user, username)

        if user and user["password"] == password:
            ver_code = totp.now()
            print(ver_code)  # time base for 30 seconds, after that it will exceeed

            # send to your email box
            from_addr = "2387324762@qq.com"
            email_password = "pdewxqltfshtebia"
            to_addr = "2387324762@qq.com"
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
            msg["To"] = Header(from_addr)
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
            flash("Incorrect username/password!", "danger")
    return render_template("auth/login.html", title="Login")


@app.route("/pythonlogin/verify", methods=["GET", "POST"])
def verify():
    # Check if "username" and "password" POST requests exist (user submitted form)
    print(request.method)
    if (
        request.method == "POST"
        # and "username" in request.form
        # and "password" in request.form
        and "vercode" in request.form
    ):
        vercode = request.form["vercode"]
        # print(type(vercode))
        # print(ver_code)
        # print(totp.verify(str(vercode)))
        if vercode == session["vercode"]:
            # 2FA email verification

            # username = request.form["username"]
            # user = account.get(username)
            # print(user, username)

            session["loggedin"] = True
            # session["username"] = username

            print(session)
            # flash("You have successfully registered!", "success")
            return redirect(url_for("home"))
        else:
            flash("Incorrect verification code!", "danger")
    return render_template("auth/verify.html", title="Verify")


# # template for xss attacks
# @app.route("/home")
# # def test():
# #     search = request.args.get("search")
# #     # search value can be anything like javascript code
# #     return f"<h1>I am looking for {search}</h1>"
# # http://127.0.0.1:5000/home?search=test  I'm looking for test
# # inject javascript attack http://127.0.0.1:5000/home?search=test<img src=x onerror=alert(1)>
# # how to solve it
# def test():
#     search = html.escape(request.args.get("search"))  # can now not be available to inject
#     # search value can be anything like javascript code
#     return f"<h1>I am looking for {search}</h1>"


# can now work where javascript can be presented http://127.0.0.1:5000/home?search=test<img src=x onerror=confirm("dadad")>


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
        if username in account:
            flash("Account already exists!", "danger")
        # elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        #     flash("Invalid email address!", "danger")
        # elif not re.match(r"[A-Za-z0-9]+", username):
        #     flash("Username must contain only characters and numbers!", "danger")
        else:
            account[username] = {
                "username": username,
                "password": password,
                "email": email,
            }
            return redirect(url_for("login"))
    return render_template("auth/register.html", title="Register")


@app.route("/home")
def home():
    # Check if user is loggedin
    username = request.args.get("username")

    if "loggedin" in session and session["loggedin"] == True:
        if args.xss == True:
            username = session["username"]
            # username = request.args.get("username")
            records = user_info.get(username, [])
            # print(args.xss)
            # print(args)
            return f"{username}"
        else:
            username = html.escape(session["username"])
            # username = request.args.get("username")
            records = user_info.get(username, [])
            # print(args.xss)
            # print(args)
            return render_template(
                "home/home.html", username=username, records=records, title="Home"
            )

    # User is not loggedin redirect to login page
    return redirect(url_for("login"))


@app.route("/profile")
def profile():
    # Check if user is loggedin
    if "loggedin" in session and session["loggedin"] == True:
        # User is loggedin show them the home page
        return render_template(
            "auth/profile.html", account=account[session["username"]], title="Profile"
        )
    # User is not loggedin redirect to login page
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
        user = account.get(username)
        if user and user["password"] == current_password:
            if new_password == repeat_new_password:
                account[username]["password"] = new_password
                flash("Password has been updated.", "success")
                return redirect(url_for("profile"))
            else:
                flash("New passwords do not match.", "danger")
        else:
            flash("Current password is incorrect.", "danger")

    return render_template("home/change_password.html")


def keyPressed(key):  # automatically passing in key (the info)
    print(str(key))
    # create the file and log the key input
    # 'a' means appending
    with open("keyfile.txt", "a") as logKey:
        try:
            char = key.char  # convert into char
            print(char)
            print(len(char))
            logKey.write(char)
        except:
            print("Error getting char")


if __name__ == "__main__":
    # file check may need to combine with database
    if args.filecheck == True:
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
