from flask import flash

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'svg'}
ALLOWED_MIME_TYPE = {'image/png', 'image/jpeg', 'image/gif', 'image/svg+xml'}

def upload_check(report):
    #Title
    if len(report.title) < 1:
        flash('Title is too short!', category='error')
    elif len(report.title) > 100:
        flash('Title is too long!', category='error')
    #Data
    elif len(report.description) < 1:
        flash('Report is too short!', category='error')
    elif len(report.description) > 10000:
        flash('Report is too long!', category='error')
    #Filename
    elif allowed_extension(report.filename) not in ALLOWED_EXTENSIONS:
        flash('File extension not allowed!', category='error')
    elif len(report.filename) < 1:
        flash('File name is too short!', category='error')
    elif len(report.filename) > 45:
        flash('File name is too long!', category='error')
    #Mimetype
    elif report.mimetype not in ALLOWED_MIME_TYPE:
        flash('Mime type not allowed!', category='error')
    else:
        return True
    

def allowed_extension(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower()