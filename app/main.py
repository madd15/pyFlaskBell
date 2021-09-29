from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from . import db
from .models import Setting

main = Blueprint('main', __name__)


@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    return redirect(url_for('auth.login'))


@main.route('/home')
@login_required
def home():
    settings = Setting.query.filter_by(setting='override_bell').first()
    return render_template('home.html', settings=settings)


@main.route('/home', methods=['POST'])
@login_required
def home_post():
    disableBell = False
    if request.form.get('disableBells'):
        disableBell = True
    settingID = request.form.get('settingID')
    if disableBell:
        setting = Setting.query.get(settingID)
        setting.setting_value = 1
    else:
        setting = Setting.query.get(settingID)
        setting.setting_value = 0
        msg = 'Bells are now enabled'
        flag = 'success'
        flash(msg, flag)
    
    db.session.commit()
    return redirect(url_for('main.home'))
