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

NO_FILE_MSG = "No file"
EMPTY_FILE_MSG = "file is empty"
FILE_KEY = 'file'

@app.route('/upload', methods=['POST'])
def upload():
    """
    Handles user request to upload new file.
    The file is saved in a specific directory in a format of timestamp-uid-filename.pptx.
    :return: JSON object with the uid.
    """
    if FILE_KEY not in request.files:
        return NO_FILE_MSG
    file = request.files[FILE_KEY]
    if file.filename == '':
        return EMPTY_FILE_MSG

    if file and allowed_file(file.filename):
        file_name = secure_filename(file.filename)
        uid = str(uuid.uuid1())
        save_file(file, file_name, uid, app.config[APP_UPLOADS_DIR_KEY])
        return jsonify(uid=uid)


@app.route('/uid/<uid>', methods=['GET'])
def status(uid):
    """
     Handles user request to receive the status of the output.
    :param uid: str unique id the user got when uploading a file.
    :return: JSON with all the information about the output.
    """
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

        # check if there is output file
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
