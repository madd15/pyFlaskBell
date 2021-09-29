from datetime import datetime, time

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required
from . import db
from .models import specialDay, specialDayTime

specialDays = Blueprint('specialDays', __name__)


@specialDays.route('/specday')
@login_required
def view():
    edit = request.args.get('edit')
    add = request.args.get('add')
    delete = request.args.get('delete')
    if add:
        title = "Add Special Day"
        return render_template('editSP.html', title=title)
    elif edit:
        editSP = specialDay.query.get(edit)
        title = " Edit SpecialDay - %s" % editSP.name
        return render_template('editSP.html', title=title, sdId=edit, sdName=editSP.name, sDate=editSP.sdate)
    elif delete:
        specialDay.query.filter(specialDay.id == delete).delete()
        specialDayTime.query.filter(specialDayTime.day == delete).delete()
        db.session.commit()
        msg = 'Special Day with ID %s has been deleted!' % delete
        flash(msg, 'danger')
        return redirect(url_for('specialDays.view'))
    else:
        specialDays = specialDay.query.all()
        return render_template('specialDays.html', specialDays=specialDays)


@specialDays.route('/specday', methods=['POST'])
@login_required
def post():
    edit = request.args.get('edit')
    add = request.args.get('add')
    if add:
        sdName = request.form.get('sdName')
        sDate = datetime.strptime(
            request.form.get('sDate'), "%Y-%m-%d")
        newSD = specialDay(name=sdName, sdate=sDate)
        db.session.add(newSD)
        db.session.commit()
        msg = 'Special Day with ID %s has been added!' % newSD.id
        flash(msg, 'success')
        return redirect(url_for('specialDays.view'))
    elif edit:
        sdName = request.form.get('sdName')
        sDate = datetime.strptime(request.form.get('sDate'), "%Y-%m-%d")
        editSD = specialDay.query.get(edit)
        editSD.name = sdName
        editSD.sdate = sDate
        db.session.commit()
        msg = 'Special Day with ID %s has been updated!' % editSD.id
        flash(msg, 'success')
        return redirect(url_for('specialDays.view'))
    else:
        return redirect(url_for('specialDays.view'))


@specialDays.route('/specday/times')
@login_required
def times_view():
    edit = request.args.get('edit')
    add = request.args.get('add')
    delete = request.args.get('delete')
    times = request.args.get('id')
    specDay = request.args.get('t')
    if times:
        getDay = specialDay.query.get(times)
        getTimes = specialDayTime.query.filter_by(
            day=times).order_by(specialDayTime.time).all()
        timeData = []
        for t in getTimes:
            id = t.id
            time = t.time.strftime("%H:%M")
            timeData.append([id, time])
        return render_template('sdtimes.html', tid=times, times=timeData, dayName=getDay.name)
    elif add:
        title = "Add Time"
        return render_template('editsdtime.html', title=title, sdID=add)
    elif edit:
        getTime = specialDayTime.query.get(edit)
        time = getTime.time.strftime("%H:%M")
        title = "Edit Time"
        return render_template('editsdtime.html', title=title, sdID=specDay, timeId=edit, time=time)
    elif delete:
        dayID = request.args.get('t')
        specialDayTime.query.filter(specialDayTime.id == delete).delete()
        db.session.commit()
        msg = 'Time with ID %s has been deleted!' % delete
        flash(msg, 'danger')
        return redirect(url_for('specialDays.times_view', id=dayID))
    else:
        return redirect(url_for('specialDays.view'))


@specialDays.route('/specday/times', methods=['POST'])
@login_required
def times_post():
    edit = request.args.get('edit')
    add = request.args.get('add')
    specDay = request.args.get('t')
    if add:
        time = datetime.strptime(request.form.get('time'), '%H:%M').time()
        dayID = add
        newTime = specialDayTime(day=dayID, time=time)
        db.session.add(newTime)
        db.session.commit()
        msg = 'Time with ID %s has been added!' % newTime.id
        flash(msg, 'success')
        return redirect(url_for('specialDays.times_view', id=dayID))
    elif edit:
        time = datetime.strptime(request.form.get('time'), '%H:%M').time()
        editTime = specialDayTime.query.get(edit)
        editTime.time = time
        db.session.commit()
        msg = 'Time with ID %s has been updated!' % editTime.id
        flash(msg, 'success')
        return redirect(url_for('specialDays.times_view', id=specDay))
    else:
        return redirect(url_for('specialDays.times_view', id=specDay))
