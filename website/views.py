from flask import Blueprint, render_template, request, flash, current_app, redirect, url_for
from flask_login import login_required, current_user
from .models import Report, User
from . import db
from .upload_check import upload_check
from flask import Response
# from .bot.admin_bot import visit_with_cookies, get_session_cookie
import os
from flask import current_app
import uuid
import pathlib
import datetime

views = Blueprint('views', __name__)


@views.route('/', methods=['GET'])
def home():
    if current_user.is_authenticated:
        return redirect(url_for('views.report_submition'))
    else:
        return redirect(url_for('auth.login'))
    

@views.route('/report-submition', methods=['GET', 'POST'])
@login_required
def report_submition():
    if request.method == 'POST': 
        file = request.files['file']
        file_extension = pathlib.Path(file.filename).suffix
        filename = f"{str(uuid.uuid4())}{file_extension}"

        new_report = Report(title=request.form.get('title'),
                            description=request.form.get('report'), 
                            filename=filename, 
                            mimetype=file.mimetype,
                            time_created=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            verified = False,
                            user_id=current_user.id)
        file.stream.seek(0)
        file.save(os.path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'], filename))
        
        if upload_check(new_report) == True:
            db.session.add(new_report)
            db.session.commit()
            flash('Report added!', category='success')

    return render_template("2_report_submition.html", user=current_user)


@views.route('/reports', methods=['GET'])
@login_required
def reports():
    if current_user.role == 0:
        userList = User.query.all()
    else:
        userList = [current_user]
    return render_template("2_reports.html", user=current_user, user_list=userList)


@views.route('/report/<report_id>', methods=['GET'])
@login_required
def report(report_id):
    report = Report.query.get(report_id)
    if current_user.role == 0 and report.user_id != current_user.id:
        return Response(status=403)
    if report is None:
        return Response(status=404)
    return render_template("2_report.html", user=current_user, report=report)


@views.route('/delete-report/<report_id>', methods=['DELETE'])
@login_required
def delete_report(report_id):  
    report = Report.query.get(report_id)
    if report:
        if report.user_id == current_user.id:
            os.remove(os.path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'], report.filename))
            db.session.delete(report)
            db.session.commit()
    return Response(status=201)


