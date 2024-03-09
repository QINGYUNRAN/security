from flask import Flask, render_template, request, redirect, url_for, session, flash
import re
import pandas as pd
app = Flask(__name__)
app.secret_key = '1'

account = {'username1': {'username': 'username1', 'password': 'password1', 'email': 'email1@example.com'},
        'username2': {'username': 'username2', 'password': 'password2', 'email': 'email2@example.com'},
        'ran':{'username': 'ran', 'password': '123', 'email': '123@mail.com'},
    }
employee_records = pd.read_csv("data/data/employees.csv").to_dict(orient='records')
checkin_records = pd.read_csv("data/data/checkIn.csv").to_dict(orient='records')
salary_records = pd.read_csv("data/data/salary.csv").to_dict(orient='records')
holidays_records = pd.read_csv("data/data/holidays.csv").to_dict(orient='records')

@app.route('/')
def index():
    session.clear()
    return redirect(url_for('login'))


@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        user = account.get(username)
        print(user, username)
        if user and user['password'] == password:
            session['loggedin'] = True
            session['username'] = username
            print(session)
            return redirect(url_for('home'))
        else:
            flash("Incorrect username/password!", "danger")
    return render_template('auth/login.html', title="Login")


@app.route('/pythonlogin/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if username in account:
            flash("Account already exists!", "danger")
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash("Invalid email address!", "danger")
        elif not re.match(r'[A-Za-z0-9]+', username):
            flash("Username must contain only characters and numbers!", "danger")
        else:
            account[username] = {'username': username, 'password': password, 'email': email}
            flash("You have successfully registered!", "success")
            return redirect(url_for('login'))
    return render_template('auth/register.html',title="Register")


@app.route('/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session and session['loggedin'] == True:
        username = session['username']
        records = employee_records
        return render_template('home/home.html', username=username, records=records, title="Home")

    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session and session['loggedin'] == True:
        # User is loggedin show them the home page
        return render_template('auth/profile.html', account=account[session['username']], title="Profile")
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/checkin')
def checkin():
    # Check if user is loggedin
    if 'loggedin' in session and session['loggedin'] == True:
        records = checkin_records
        return render_template('home/checkin.html', records=records, title="Checkin")
    return redirect(url_for('login'))

@app.route('/salary')
def salary():
    # Check if user is loggedin
    if 'loggedin' in session and session['loggedin'] == True:
        records = salary_records
        return render_template('home/salary.html', records=records, title="Salary")
    return redirect(url_for('login'))

@app.route('/holidays')
def holidays():
    # Check if user is loggedin
    if 'loggedin' in session and session['loggedin'] == True:
        records = holidays_records
        return render_template('home/holidays.html', records=records, title="Holidays")
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        repeat_new_password = request.form['repeat_new_password']
        username = session['username']
        user = account.get(username)
        if user and user['password'] == current_password:
            if new_password == repeat_new_password:
                account[username]['password'] = new_password
                flash('Password has been updated.', 'success')
                return redirect(url_for('profile'))
            else:
                flash('New passwords do not match.', 'danger')
        else:
            flash('Current password is incorrect.', 'danger')

    return render_template('home/change_password.html')

if __name__ == '__main__':
    app.run(debug=True)
