from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user, login_required
from .models import Pattern

main = Blueprint('main', __name__)


@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    return redirect(url_for('auth.login'))


@main.route('/home')
@login_required
def home():
    patterns = Pattern.query.all()
    return render_template('home.html', patterns=patterns)
