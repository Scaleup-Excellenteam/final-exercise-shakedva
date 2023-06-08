from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime
from pathlib import Path
from enum import Enum
import json
UPLOAD_DIR_NAME = "upload"
ALLOWED_EXTENSIONS = {'pptx'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER_PATH'] = Path(Path.cwd() / UPLOAD_DIR_NAME)


def allowed_file(filename: str):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_file(file, file_name, uid):
    directory_path = app.config['UPLOAD_FOLDER_PATH'] / uid
    directory_path.mkdir(exist_ok=True)

    data = (datetime.now().strftime('%Y-%m-%d-%H-%M-%S'), uid, file_name)
    file_name = '_'.join(data)
    file.save(directory_path / file_name)


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


class Status(str, Enum):
    DONE = 'done'
    PENDING = 'pending'
    NOT_FOUND = 'not found'


@app.route('/<uid>', methods=['GET'])
def status(uid):
    response = {
        'explanation': None
    }

    output_dir = app.config['UPLOAD_FOLDER_PATH'] / uid
    if output_dir.is_dir():
        output_dir_files = list(output_dir.glob("*.json"))

        if output_dir_files:
            response['status'] = Status.DONE
            with open(output_dir_files[0], 'r') as f:
                response['explanation'] = json.loads(f.read())
        else:
            response['status'] = Status.PENDING

        file_name = next(output_dir.glob("*.pptx"))
        if file_name:
            timestamp, _, original_file_name = file_name.name.split('_', 2)
            response['filename'] = original_file_name
            response['timestamp'] = timestamp
    else:
        response['status'] = Status.NOT_FOUND
    return jsonify(response)
