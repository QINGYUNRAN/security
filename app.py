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

parser = argparse.ArgumentParser(description="Argparse")
parser.add_argument("--xss", default=False, type=bool, help="whether set xss attacks")
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


@app.route("/pythonlogin/", methods=["GET", "POST"])
def login():
    # Check if "username" and "password" POST requests exist (user submitted form)
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
            session["loggedin"] = True
            session["username"] = username
            print(session)
            return redirect(url_for("home"))
        else:
            flash("Incorrect username/password!", "danger")
    return render_template("auth/login.html", title="Login")


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
            flash("You have successfully registered!", "success")
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


if __name__ == "__main__":
    app.run(debug=True)
