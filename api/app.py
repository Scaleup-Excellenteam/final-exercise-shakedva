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
# db.drop_all_rows_tables()


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


def get_upload(session, uid=None, filename=None, email=None):
    if uid:
        user_upload = session.query(Upload).filter(Upload.uid == uid).first()
    elif email and filename:
        user = session.query(User).filter(User.email == email).first()
        # todo: check which one to return(first.. last..)
        user_upload = session.query(Upload).filter(Upload.filename == filename, Upload.user_id == user.id).first()
    else:
        return None
    return user_upload


def get_explanation(uid: str):
    explanation = None
    output_file_path = next(app.config[APP_OUTPUTS_DIR_KEY].glob(f"{uid}.json"), None)
    if output_file_path:
        with open(output_file_path, 'r') as f:
            explanation = json.loads(f.read())
    return explanation


@app.route('/status', methods=['GET'])
def status():
    response = {
        'explanation': None,
        'uid': None,
        'filename': None,
        'finish_time': None,
        'status': RequestStatusEnum.NOT_FOUND
    }
    with db.session() as session:
        user_upload = get_upload(
            session,
            request.args.get('uid'),
            request.args.get('filename'),
            request.args.get('email')
        )
        if user_upload:
            response['explanation'] = get_explanation(user_upload.uid)
            if response['explanation']:
                user_upload.status = RequestStatusEnum.DONE
                session.commit()
            response["uid"] = user_upload.uid
            response["filename"] = user_upload.filename
            response["finish_time"] = user_upload.finish_time
            response["status"] = user_upload.status

    return jsonify(response)


if __name__ == "__main__":
    app.run()
