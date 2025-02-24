from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Report, User
from . import db
from werkzeug.utils import secure_filename
import json
from .utils import admin_required, user_required
from .upload_check import upload_check
from flask import Response
from .bot.admin_bot import visit_with_cookies_time_limit, visit_with_cookies
import threading


views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if(current_user.role == 0):
        return render_template("home_admin.html", user=current_user)
    else:
        if request.method == 'POST': 

            title = request.form.get('title')
            report = request.form.get('report')
            file = request.files.get('file')

            new_report = Report(title=title,
                                data=report, 
                                img=file.read(), 
                                filename=secure_filename(file.filename), 
                                mimetype=file.mimetype, 
                                user_id=current_user.id)
            
            if upload_check(new_report) == True:
                db.session.add(new_report)
                db.session.commit()
                flash('Report added!', category='success')
                visit_with_cookies(
                    page_to_load=f'http://127.0.0.1:5000/report/{new_report.id}', 
                    session_cookie='.eJwljjEOAjEMwP6SmaFp2qS5z6A0TQQS052YEH-nEqO92B-45xnXA4601xU3uD8XHJCu0a1rUatGk9hIylpCNTynrhZoVAJ71NQhLkTD0KeH8NTKXh3NJMmHNJYe0pUDpTcs1TYXVpxVcbgrJ2O4s-eO8BZNYI-8rzj_NwjfHxtBL50.Z7yOkQ.rJCDXfHQcTOdj_BXFawdRWkth34'     
                )

        return render_template("home.html", user=current_user)


@views.route('/reports', methods=['GET'])
@login_required
@user_required
def reports():
    return render_template("reports.html", user=current_user)


@views.route('/report/<report_id>', methods=['GET'])
@login_required
@admin_required
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
    userList = User.query.all()
    return render_template("admin.html", user=userList)