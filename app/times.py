from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required
from . import db
from .models import Pattern, Time

times = Blueprint('times', __name__)


@times.route('/times')
@login_required
def times_view():
    updated = request.args.get('updated')
    deleted = request.args.get('deleted')
    added = request.args.get('added')
    edit = request.args.get('edit')
    add = request.args.get('add')
    delete = request.args.get('delete')
    if add:
        title = "Add Time"
        weekData = []
        for dayNumber in range(0, 7):
            dayName = getDayName(dayNumber)
            weekData.append([dayName])
        patterns = Pattern.query.all()
        return render_template('edittime.html', title=title, patterns=patterns, weekData=weekData)
    elif edit:
        editTime = Time.query.get(edit)
        time = editTime.time
        weekData = []
        for dayNumber in range(0, 7):
            dayName = getDayName(dayNumber)
            if editTime.days[dayNumber] == '1':
                active = "1"
            else:
                active = "0"
            weekData.append([dayName, active])
        patterns = Pattern.query.all()
        title = "Edit Time - %s" % editTime.name
        return render_template('edittime.html', title=title, timeId=edit, timeName=editTime.name, weekData=weekData, ringTime=time.strftime("%H:%M"), ringPattern=editTime.pattern, patterns=patterns)
    elif delete:
        qry = Time.query.get(delete)
        db.session.delete(qry)
        db.session.commit()
        msg = 'Time with ID %s has been deleted!' % delete
        flash(msg, 'danger')
        return redirect(url_for('times.times_view'))
    else:
        times = Time.query.order_by(Time.time).all()
        timeData = []
        for t in times:
            weekData = []
            id = t.id
            name = t.name
            days = t.days
            time = t.time.strftime("%H:%M")
            pattern = t.pattern
            pattern = Pattern.query.get(pattern)
            for dayNumber in range(0, 7):
                if days[dayNumber] == '1':
                    weekData += ["1"]
                else:
                    weekData += ["0"]
            timeData.append([id, name, weekData, time, pattern.name])
        return render_template('times.html', times=timeData, updated=updated, deleted=deleted, added=added)


@times.route('/times', methods=['POST'])
@login_required
def times_post():
    edit = request.args.get('edit')
    add = request.args.get('add')
    if add:
        timeName = request.form.get('timeName')
        ringTime = datetime.strptime(
            request.form.get('ringTime'), '%H:%M').time()
        weekDays = list("0000000")
        ringPattern = request.form.get('pattern')
        for dayNumber in range(0, 7):
            formDay = request.form.get(getDayName(dayNumber))
            if formDay == "1":
                weekDays[dayNumber] = "1"
        weekDays = "".join(weekDays)
        newTime = Time(name=timeName, days=weekDays,
                       time=ringTime, pattern=ringPattern)
        db.session.add(newTime)
        db.session.commit()
        msg = 'Time with ID %s has been added!' % newTime.id
        flash(msg, 'success')
        return redirect(url_for('times.times_view'))
    elif edit:
        timeName = request.form.get('timeName')
        ringTime = datetime.strptime(
            request.form.get('ringTime'), '%H:%M').time()
        weekDays = list("0000000")
        ringPattern = request.form.get('pattern')
        for dayNumber in range(0, 7):
            formDay = request.form.get(getDayName(dayNumber))
            if formDay == "1":
                weekDays[dayNumber] = "1"
        weekDays = "".join(weekDays)
        editTime = Time.query.get(edit)
        editTime.name = timeName
        editTime.days = weekDays
        editTime.time = ringTime
        editTime.pattern = ringPattern
        db.session.commit()
        msg = 'Time with ID %s has been updated!' % editTime.id
        flash(msg, 'success')
        return redirect(url_for('times.times_view'))
    else:
        return redirect(url_for('times.times_view'))


def getDayName(weekday):
    if weekday == 0:
        return "Monday"
    if weekday == 1:
        return "Tuesday"
    if weekday == 2:
        return "Wednesday"
    if weekday == 3:
        return "Thursday"
    if weekday == 4:
        return "Friday"
    if weekday == 5:
        return "Saturday"
    if weekday == 6:
        return "Sunday"
