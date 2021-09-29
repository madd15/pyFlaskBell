from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash

from . import db
from .models import User

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    page = request.args.get('next')
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    return render_template('login.html', page=page)


@auth.route('/login', methods=['POST'])
def login_post():
    page = request.form.get('page')
    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(username=username).first()

    if user:
        if check_password_hash(user.password, password):
            login_user(user, remember=remember)
            if page == "/times":
                return redirect(url_for('times.times_view'))
            elif page == "/breaks":
                return redirect(url_for('breaks.breaks_view'))
            elif page == "/users":
                return redirect(url_for('users.users_view'))
            else:
                return redirect(url_for('main.home'))
        else:
            flash('Incorrect password, try again.')
    else:
        flash('User does not exist')

    return render_template('login.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

# @auth.route('/signup')
# def signup():
#     if current_user.is_authenticated:
#         return redirect(url_for('main.home'))
#     return render_template('signup.html')

# @auth.route('/signup', methods=['POST'])
# def signup_post():
#     username = request.form.get('username')
#     password = request.form.get('password')

#     # if this returns a user, then the username already exists in database
#     user = User.query.filter_by(username=username).first()

#     if user:  # if a user is found, we want to redirect back to signup page so user can try again
#         flash('User already exists')
#         return redirect(url_for('auth.signup'))

#     # create a new user with the form data. Hash the password so the plaintext version isn't saved.
#     new_user = User(username=username, password=generate_password_hash(
#         password, method='sha256'))

#     # add the new user to the database
#     db.session.add(new_user)
#     db.session.commit()

#     return redirect(url_for('auth.login'))
