from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required

from . import db
from .models import Pattern

patterns = Blueprint('patterns', __name__)


@patterns.route('/patterns')
@login_required
def patterns_view():
    updated = request.args.get('updated')
    deleted = request.args.get('deleted')
    added = request.args.get('added')
    add = request.args.get('add')
    edit = request.args.get('edit')
    delete = request.args.get('delete')
    if add:
        title = "Add Pattern"
        return render_template('editpattern.html', title=title)
    elif edit:
        editPattern = Pattern.query.get(edit)
        title = "Edit Pattern - %s" % editPattern.name
        return render_template('editpattern.html', title=title, patternId=edit, patternName=editPattern.name, pattern=editPattern.pattern)
    elif delete:
        qry = Pattern.query.get(delete)
        db.session.delete(qry)
        db.session.commit()
        msg = 'Pattern with ID %s has been deleted!' % delete
        flash(msg, 'danger')
        return redirect(url_for('patterns.patterns_view', deleted=delete))
    else:
        patterns = Pattern.query.all()
        return render_template('patterns.html', patterns=patterns, updated=updated, deleted=deleted, added=added)


@patterns.route('/patterns', methods=['POST'])
@login_required
def patterns_post():
    edit = request.args.get('edit')
    add = request.args.get('add')

    if add:
        patternName = request.form.get('patternName')
        pattern = request.form.get('pattern')
        newPattern = Pattern(name=patternName, pattern=pattern)
        db.session.add(newPattern)
        db.session.commit()
        msg = 'Pattern with ID %s has been added!' % newPattern.id
        flash(msg, 'success')
        return redirect(url_for('patterns.patterns_view'))
    elif edit:
        patternName = request.form.get('patternName')
        pattern = request.form.get('pattern')
        editPattern = Pattern.query.get(edit)
        editPattern.name = patternName
        editPattern.pattern = pattern
        db.session.commit()
        msg = 'Pattern with ID %s has been updated!' % editPattern.id
        flash(msg, 'success')
        return redirect(url_for('patterns.patterns_view'))
    else:
        return redirect(url_for('patterns.patterns_view'))
