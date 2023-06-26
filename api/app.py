from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import uuid
from pathlib import Path
from .request_status_enum import RequestStatusEnum
from .utils import allowed_file, save_file, insert_upload, get_upload, get_explanation

APP_UPLOADS_DIR_KEY = "UPLOAD_FOLDER_PATH"
APP_OUTPUTS_DIR_KEY = "OUTPUT_FOLDER_PATH"

app = Flask(__name__)
app.config[APP_UPLOADS_DIR_KEY] = Path(Path.cwd() / "uploads")
app.config[APP_OUTPUTS_DIR_KEY] = Path(Path.cwd() / "outputs")

NO_FILE_MSG = "No file"
EMPTY_FILE_MSG = "file is empty"
FILE_KEY = 'file'
EMAIL_KEY = 'email'


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
        insert_upload(uid, file_name, request.form.get(EMAIL_KEY))
        save_file(file, file_name, uid, app.config[APP_UPLOADS_DIR_KEY])
        return jsonify(uid=uid)
    return jsonify(uid=0)


@app.route('/status', methods=['GET'])
def status():
    """
    Handles user request to receive the status of an upload as a JSON file.
    :return: JSON with the relevant information about the upload.
    """
    response = {
        'explanation': None,
        'uid': None,
        'filename': None,
        'finish_time': None,
        'status': RequestStatusEnum.NOT_FOUND
    }
    user_upload = get_upload(
        request.args.get('uid'),
        request.args.get('filename'),
        request.args.get('email')
    )
    if user_upload:
        response['explanation'] = get_explanation(user_upload.uid, app.config[APP_OUTPUTS_DIR_KEY] )
        response["uid"] = user_upload.uid
        response["filename"] = user_upload.filename
        response["finish_time"] = user_upload.finish_time
        response["status"] = user_upload.status

    return jsonify(response)


if __name__ == "__main__":
    app.run()
