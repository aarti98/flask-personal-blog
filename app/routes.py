from email.mime import base
import os

from flask import request, send_from_directory, url_for
from flask_ckeditor import upload_success, upload_fail

from app import app

basedir = os.path.abspath(os.path.dirname(__file__))

@app.route('/files/<path:filename>')
def uploaded_files(filename):
    path = basedir + '/static/images/'
    return send_from_directory(path, filename)

@app.route('/upload', methods=['POST'])
def upload():
    f = request.files.get('upload')
    # Add more validations here
    extension = f.filename.split('.')[-1].lower()
    if extension not in ['jpg', 'gif', 'png', 'jpeg']:
        return upload_fail(message='Image only!')
    print('os', os.path)
    f.save(os.path.join(basedir  + '/static/images', f.filename))
    url = url_for('uploaded_files', filename=f.filename)
    return upload_success(url, filename=f.filename) 