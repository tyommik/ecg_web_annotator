from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
# from . import db

auth = Blueprint('auth', __name__)

users = {'admin': {'password': 'admin'}, 'test': {'password': 'test'}}


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    name = request.form.get('name')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    # user = User.query.filter_by(email=email).first()
    #
    # # check if user actually exists
    # # take the user supplied password, hash it, and compare it to the hashed password in database
    # if not email in users or not check_password_hash(users.get(email)['password'], password):
    if not name in users or not password == users.get(name)['password']:
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if user doesn't exist or password is wrong, reload the page

    else:
        user = User(name, name, True)
        login_user(user, remember=remember)
    return redirect(url_for('main.index'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    # user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database
    #
    # if user: # if a user is found, we want to redirect back to signup page so user can try again
    #     return redirect(url_for('auth.signup'))
    #
    # # create new user with the form data. Hash the password so plaintext version isn't saved.
    # new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
    #
    # # add the new user to the database
    # db.session.add(new_user)
    # db.session.commit()

    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))