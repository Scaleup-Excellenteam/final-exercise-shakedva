from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime

UPLOAD_FOLDER = "upload"
ALLOWED_EXTENSIONS = {'pptx'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename: str):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_file(file, file_name, uid):
    data = (datetime.today().strftime('%Y-%m-%d'), uid, file_name)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], '_'.join(data)))


@app.route('/', methods=['POST'])
def upload_file():
    # todo handle no files and empty files.
    if 'file' not in request.files:
        return "No file"
    file = request.files['file']
    if file.filename == '':
        return "file is empty"

    if file and allowed_file(file.filename):
        file_name = secure_filename(file.filename)
        uid = str(uuid.uuid1())
        save_file(file, file_name, uid)
        return jsonify(uid=uid)
