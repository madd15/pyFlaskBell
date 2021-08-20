from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required

from . import db
from .models import Break

breaks = Blueprint('breaks', __name__)


@breaks.route('/breaks')
@login_required
def breaks_view():
    updated = request.args.get('updated')
    deleted = request.args.get('deleted')
    added = request.args.get('added')
    edit = request.args.get('edit')
    add = request.args.get('add')
    delete = request.args.get('delete')
    if add:
        title = "Add Break"
        return render_template('editbreak.html', title=title)
    elif edit:
        editBreak = Break.query.get(edit)
        title = " Edit Break - %s" % editBreak.name
        return render_template('editbreak.html', title=title, breakId=edit, breakName=editBreak.name, startDate=editBreak.startDate, endDate=editBreak.endDate)
    elif delete:
        qry = Break.query.get(delete)
        db.session.delete(qry)
        db.session.commit()
        msg = 'Break with ID %s has been deleted!' % delete
        flash(msg, 'danger')
        return redirect(url_for('breaks.breaks_view'))
    else:
        breaks = Break.query.all()
        return render_template('breaks.html', breaks=breaks, updated=updated, deleted=deleted, added=added)


@breaks.route('/breaks', methods=['POST'])
@login_required
def breaks_post():
    edit = request.args.get('edit')
    add = request.args.get('add')
    if add:
        breakName = request.form.get('breakName')
        startDate = datetime.strptime(
            request.form.get('startDate'), "%Y-%m-%d")
        endDate = datetime.strptime(request.form.get('endDate'), "%Y-%m-%d")
        newBreak = Break(name=breakName, startDate=startDate, endDate=endDate)
        db.session.add(newBreak)
        db.session.commit()
        msg = 'Break with ID %s has been updated!' % newBreak.id
        flash(msg, 'success')
        return redirect(url_for('breaks.breaks_view'))
    elif edit:
        breakName = request.form.get('breakName')
        startDate = datetime.strptime(
            request.form.get('startDate'), "%Y-%m-%d")
        endDate = datetime.strptime(request.form.get('endDate'), "%Y-%m-%d")
        editBreak = Break.query.get(edit)
        editBreak.name = breakName
        editBreak.startDate = startDate
        editBreak.endDate = endDate
        db.session.commit()
        msg = 'Break with ID %s has been edited!' % editBreak.id
        flash(msg, 'success')
        return redirect(url_for('breaks.breaks_view'))
    else:
        return redirect(url_for('breaks.breaks_view'))
