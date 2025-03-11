from flask import Blueprint, render_template, request, flash, jsonify, session, current_app
from flask.sessions import SecureCookieSessionInterface
from flask_login import login_required, current_user
from .models import Report, User
from . import db
from werkzeug.utils import secure_filename
import json
from .utils import admin_required, user_required
from .upload_check import upload_check
import base64
from flask import Response
from .bot.admin_bot import visit_with_cookies_time_limit, visit_with_cookies, get_session_cookie
import threading
import os
from flask import current_app

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if(current_user.role == 0):
        return render_template("report_submition_admin.html", user=current_user)
    else:
        if request.method == 'POST': 

            title = request.form.get('title')
            report = request.form.get('report')
            file = request.files['file']
            img = base64.b64encode(file.read())
            filename = secure_filename(file.filename)

            new_report = Report(title=title,
                                data=report, 
                                img=img.decode("utf-8"), 
                                filename=filename, 
                                mimetype=file.mimetype, 
                                user_id=current_user.id)
            
            file.stream.seek(0)
            file.save(os.path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'], filename))
            
            if upload_check(new_report) == True:
                db.session.add(new_report)
                db.session.commit()
                flash('Report added!', category='success')
                visit_with_cookies(
                    page_to_load=f'http://127.0.0.1:5000/static/images/{filename}', 
                    session_cookie=get_session_cookie("127.0.0.1:5000", "admin", "admin")
                )

        return render_template("report_submition.html", user=current_user)


@views.route('/reports', methods=['GET'])
@login_required
@user_required
def reports():
    session_serializer = SecureCookieSessionInterface().get_signing_serializer(current_app)
    session_cookie = session_serializer.dumps(dict(session))
    print(session_cookie)
    return render_template("reports.html", user=current_user)


@views.route('/report/<report_id>', methods=['GET'])
@login_required
# @admin_required
def report(report_id):
    print(report_id)
    report = Report.query.get(report_id)
    print(report)
    if report is None:
        return Response(status=404)
    return render_template("report.html", user=current_user, report=report)


@views.route('/delete-report', methods=['POST'])
def delete_report():  
    report = json.loads(request.data)
    reportId = report['reportId']
    report = Report.query.get(reportId)
    if report:
        if report.user_id == current_user.id:
            db.session.delete(report)
            db.session.commit()

    return jsonify({})


@views.route('/admin', methods=['GET'])
@login_required
@admin_required
def admin():
    session_tmp = session
    print(session_tmp)
    userList = User.query.all()
    return render_template("admin.html", user=current_user, user_list=userList)