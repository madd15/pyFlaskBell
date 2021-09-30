from time import time
from flask_login import UserMixin

from . import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    password = db.Column(db.String(100))


class Break(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    startDate = db.Column(db.Date(), nullable=False)
    endDate = db.Column(db.Date(), nullable=False)

class Time(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100), unique=True, nullable=False)
    days = db.Column(db.String(7), server_default='1111100')
    time = db.Column(db.Time(), unique=True, nullable=False)


class specialDay(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    sdate = db.Column(db.Date(), nullable=False)


class specialDayTime(db.Model):
    __table_args__ = (
        db.UniqueConstraint('day', 'time'),
    )
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Integer, nullable=False)
    time = db.Column(db.Time(), nullable=False)

class Setting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    setting = db.Column(db.String(100), unique=True, nullable=False)
    setting_value = db.Column(db.Integer, nullable=False, default=0)
