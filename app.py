from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime
from pathlib import Path
from enum import Enum
import json
UPLOAD_DIR_NAME = "uploads"
OUTPUT_DIR_NAME = "outputs"
ALLOWED_EXTENSIONS = {'pptx'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER_PATH'] = Path(Path.cwd() / UPLOAD_DIR_NAME)
app.config['OUTPUT_FOLDER_PATH'] = Path(Path.cwd() / OUTPUT_DIR_NAME)


def allowed_file(filename: str):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_file(file, file_name, uid):
    directory_path = app.config['UPLOAD_FOLDER_PATH']
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
    input_dir_path = app.config['UPLOAD_FOLDER_PATH']
    input_file_path = next(input_dir_path.glob(f"*{uid}*.pptx"), None)
    if not input_file_path:
        response['status'] = Status.NOT_FOUND
    else:
        timestamp, _, original_file_name = input_file_path.name.split('_', 2)
        response['filename'] = original_file_name
        response['timestamp'] = timestamp
        output_dir_path = app.config['OUTPUT_FOLDER_PATH']

        output_file_path = next(output_dir_path.glob(f"*{uid}*.json"), None)
        if output_file_path:
            response['status'] = Status.DONE
            with open(output_file_path, 'r') as f:
                response['explanation'] = json.loads(f.read())
        else:
            response['status'] = Status.PENDING

    return jsonify(response)
