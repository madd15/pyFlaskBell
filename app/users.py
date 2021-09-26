from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required
from werkzeug.security import generate_password_hash

from . import db
from .models import User

users = Blueprint("users", __name__)


@users.route("/users")
@login_required
def users_view():
    updated = request.args.get('updated')
    deleted = request.args.get('deleted')
    added = request.args.get('added')
    edit = request.args.get('edit')
    add = request.args.get('add')
    delete = request.args.get('delete')
    if add:
        title = " Add User"
        return render_template('edituser.html', title=title)
    elif edit:
        editUser = User.query.get(edit)
        title = " Edit User - %s" % editUser.username
        return render_template('edituser.html', title=title, userId=edit, username=editUser.username)
    elif delete:
        qry = User.query.get(delete)
        db.session.delete(qry)
        db.session.commit()
        msg = 'User %s has been deleted!' % qry.username
        flash(msg, 'danger')
        return redirect(url_for('users.users_view'))
    else:
        users = User.query.all()
        return render_template('users.html', users=users, updated=updated, deleted=deleted, added=added)


@users.route("/users", methods=['POST'])
@login_required
def users_post():
    edit = request.args.get('edit')
    add = request.args.get('add')
    if add:
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            flash('User already exists', 'danger')
            return redirect(url_for('users.users_view'))

        new_user = User(username=username, password=generate_password_hash(
            password, method='sha256'))

        db.session.add(new_user)
        db.session.commit()
        msg = 'User %s has been added!' % new_user.username
        flash(msg, 'success')
        return redirect(url_for('users.users_view'))

    elif edit:
        username = request.form.get('username')
        password = request.form.get('password')
        editUser = User.query.get(edit)
        editUser.username = username
        if password:
            editUser.password = generate_password_hash(
                password, method='sha256')
        db.session.commit()
        msg = 'User %s has been updated!' % editUser.username
        flash(msg, 'success')
        return redirect(url_for('users.users_view'))
    else:
        return redirect(url_for('users.users_view'))
