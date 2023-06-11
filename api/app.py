from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import uuid
from pathlib import Path
import json
from .request_status_enum import RequestStatusEnum
from .utils import allowed_file, save_file

APP_UPLOADS_DIR_KEY = "UPLOAD_FOLDER_PATH"
APP_OUTPUTS_DIR_KEY = "OUTPUT_FOLDER_PATH"

app = Flask(__name__)
app.config[APP_UPLOADS_DIR_KEY] = Path(Path.cwd() / "uploads")
app.config[APP_OUTPUTS_DIR_KEY] = Path(Path.cwd() / "outputs")


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file"
    file = request.files['file']
    if file.filename == '':
        return "file is empty"

    if file and allowed_file(file.filename):
        file_name = secure_filename(file.filename)
        uid = str(uuid.uuid1())
        save_file(file, file_name, uid, app.config[APP_UPLOADS_DIR_KEY])
        return jsonify(uid=uid)


@app.route('/uid/<uid>', methods=['GET'])
def status(uid):
    response = {
        'explanation': None
    }
    input_dir_path = app.config[APP_UPLOADS_DIR_KEY]
    input_file_path = next(input_dir_path.glob(f"*{uid}*.pptx"), None)
    if not input_file_path:
        response['status'] = RequestStatusEnum.NOT_FOUND
    else:
        timestamp, _, original_file_name = input_file_path.name.split('_', 2)
        response['filename'] = original_file_name
        response['timestamp'] = timestamp

        output_file_path = next(app.config[APP_OUTPUTS_DIR_KEY].glob(f"*{uid}*.json"), None)
        if output_file_path:
            response['status'] = RequestStatusEnum.DONE
            with open(output_file_path, 'r') as f:
                response['explanation'] = json.loads(f.read())
        else:
            response['status'] = RequestStatusEnum.PENDING

    return jsonify(response)


if __name__ == "__main__":
    app.run()