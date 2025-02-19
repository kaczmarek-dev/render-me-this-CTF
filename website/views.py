from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Report
from . import db
from werkzeug.utils import secure_filename
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 

        title = request.form.get('title')
        report = request.form.get('report')#Gets the report from the HTML 
        file = request.files.get('file')

        if len(report) < 1:
            flash('Report is too short!', category='error') 
        elif len(title) < 1:
            flash('Title is too short!', category='error')
        else:
            filename = secure_filename(file.filename)
            mimetype = file.mimetype

            new_report = Report(title=title,
                                data=report, 
                                img=file.read(), 
                                filename=filename, 
                                mimetype=mimetype, 
                                user_id=current_user.id)  #providing the schema for the report 
            db.session.add(new_report) #adding the report to the database 
            db.session.commit()
            flash('Report added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-report', methods=['POST'])
def delete_report():  
    report = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    reportId = report['reportId']
    report = Report.query.get(reportId)
    if report:
        if report.user_id == current_user.id:
            db.session.delete(report)
            db.session.commit()

    return jsonify({})

@views.route('/admin', methods=['GET'])
@login_required
def admin():
    return render_template("admin.html", user=current_user)