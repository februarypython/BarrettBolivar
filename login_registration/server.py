# doesn't work desperately need help
from flask import Flask, request, redirect, render_template, session, flash, url_for
from mysqlconnection import MySQLConnector
import re
import md5
app = Flask(__name__)
mysql = MySQLConnector(app,'logreg')
app.secret_key = 'soooosecret'

emailRegex = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
passwordRegex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$')

def validate():
    failPass = 0
    if request.form['fname'] == '':
        flash('Name cannot be empty', 'first_nameError')
        failPass += 1
        pass
    elif any(char.isdigit() for char in request.form['fname']) == True:
        flash('No numbers in name', 'first_nameError')
        failPass += 1
        pass
    else:
        session['fname'] = request.form['fname']
    if request.form['lname'] == '':
        flash('Last name cannot be blank', 'lastNameError')
        failPass += 1
        pass
    elif any(char.isdigit() for char in request.form['lname']) == True:
        flash('Last name cannot have numbers', 'lastNameError')
        failPass += 1
        pass
    else:
        session['lname'] = request.form['lname']
    if request.form['email'] == '':
        flash('Email cannot be blank', 'emailError')
        failPass += 1
        pass
    elif not emailRegex.match(request.form['email']):
        flash('Invalid email address', 'emailError')
        failPass += 1
        pass
    else:
        session['email'] = request.form['email']
    if request.form['password'] == '':
        flash('Password cannot be blank', 'passwordError')
        failPass += 1
        pass
    elif len(request.form['password']) < 8:
        flash('Password must be greater than 8 characters', 'passwordError')
        failPass += 1
        pass
    elif not passwordRegex.match(request.form['password']):
        flash('Password must contain one lowercase, one uppercase letter, one digit', 'passwordError')
        failPass += 1
        pass
    else:
        session['password'] = request.form['password']
    if request.form['cpassword'] == '':
        flash('Need to confirm password', 'confirmPasswordError')
        failPass += 1
        pass
    elif request.form['cpassword'] != request.form['password']:
        flash('Passwords do not match', 'confirmPasswordError')
        failPass += 1
    else:
        session['cpassword'] = request.form['cpassword']
    if failPass > 0:
        session['password'] = '' #reset passwords
        session['cpassword'] = ''
        return False
    else:
        return True

def validateLogin():
    failPass = 0
    if request.form['email'] == '':
        flash('Email cannot be blank', 'emailError')
        failPass += 1
        pass
    elif not emailRegex.match(request.form['email']):
        flash('Email address not found', 'emailError')
        failPass += 1
        pass
    else:
        session['email'] = request.form['email']
    if request.form['password'] == '':
        flash('Password is blank', 'passwordError')
        failPass += 1
        pass
    elif len(request.form['password']) < 8:
        flash('Need more than 8 characters in password', 'passwordError')
        failPass += 1
        pass
    elif not passwordRegex.match(request.form['password']):
        flash('Password must contain at least one lowercase letter, one uppercase letter, one digit', 'passwordError')
        failPass += 1
        pass
    else:
        session['password'] = request.form['password']
    if failPass > 0:
        session['password'] = '' #reset password
        session['cpassword'] = ''
        return False
    else:
        return True

#start of application 
@app.route('/', methods=['POST'])
def index():
    return render_template('index.html')

@app.route('/success', methods=['GET', 'POST'])
def create():
    if validate() == False:
        return redirect('/')
    else:
        password1 = request.form['password']
        hashed_password = md5.new(password1).hexdigest()
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (:first_name, :last_name, :email, :hashed_password, NOW(), NOW())"
        data = {
                'first_name': request.form['first_name'],
                'last_name': request.form['last_name'],
                'email': request.form['email'],
                'password': request.form['password']
                }
        mysql.query_db(query, data)
        return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login():
    if validateLogin() == False:
        return redirect('/')
    else:
        userInfo = mysql.fetch("SELECT * FROM users WHERE users.email = :email LIMIT 1")
        inputPassword = request.form['password']
        inputPasswordHashed = md5.new(inputPassword).hexdigest()
        if inputPasswordHashed == userInfo[0]['password']:
            return redirect('/')
        else:
            flash('Incorrect password', 'passwordError')
    return render_template('index.html')

@app.route('/logout', methods=['POST'])
def clear():
    session['firstName'] = ''
    session['lname'] = ''
    session['email'] = ''
    session['password'] = ''
    session['cpassword'] = ''
    session['userid'] = ''

    return render_template('index.html')


app.run(debug=True)