from app.auth import login
from flask.blueprints import Blueprint
from app.models import specialDay


from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required
from . import db
from .models import Pattern, specialDay, specialDayTime

specialDays = Blueprint('specialDays', __name__)

@specialDays.route('/specday')
@login_required
def view():
    return render_template('specialDays.html')
