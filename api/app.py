from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import uuid
from pathlib import Path
import json
from .request_status_enum import RequestStatusEnum
from .utils import allowed_file, save_file
from db.orm import DB, User, Upload
import datetime

APP_UPLOADS_DIR_KEY = "UPLOAD_FOLDER_PATH"
APP_OUTPUTS_DIR_KEY = "OUTPUT_FOLDER_PATH"

app = Flask(__name__)
app.config[APP_UPLOADS_DIR_KEY] = Path(Path.cwd() / "uploads")
app.config[APP_OUTPUTS_DIR_KEY] = Path(Path.cwd() / "outputs")

NO_FILE_MSG = "No file"
EMPTY_FILE_MSG = "file is empty"
FILE_KEY = 'file'
EMAIL_KEY = 'email'

db = DB()
db.drop_all_rows_tables()


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
        # save_file(file, file_name, uid, app.config[APP_UPLOADS_DIR_KEY]) #TODO
        return jsonify(uid=uid)


def insert_upload(uid, file_name, email):
    with db.session() as session:
        user = None
        if email:
            # fetch the user from the db if exists
            user = session.query(User).filter(User.email == email).first()
            if not user:
                user = User(email=email)
        upload = Upload(
            uid=uid,
            filename=file_name,
            upload_time=datetime.datetime.now(),
            status='pending',
            user_id=user.id if user else None,
            user=user
        )
        if user:
            user.uploads.append(upload)
            session.add(user)
        else:
            session.add(upload)
        session.commit()


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
