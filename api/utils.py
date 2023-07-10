from pathlib import Path
import datetime
from werkzeug.datastructures.file_storage import FileStorage
from db.orm import DB, User, Upload
from .request_status_enum import RequestStatusEnum
import json


ALLOWED_EXTENSIONS = {'pptx'}


def allowed_file(filename: str) -> bool:
    """
    Returns whether the file is within allowed types.
    :param filename: str file name.
    :return:
    """
    return '.' in filename and \
           get_file_extension(filename).lower() in ALLOWED_EXTENSIONS


def get_file_extension(filename: str) -> str:
    """
    Given a file name, returns the extension of the file (pptx, pdf, etc.)
    :param filename: str file name
    :return: str file's extension
    """
    return filename.rsplit('.', 1)[1]


def save_file(file: FileStorage, filename: str, uid: str, directory_path: Path):
    """
    Saves the file in the received directory path
    :param file: FileStorage file
    :param filename: str file name
    :param uid: str unique id
    :param directory_path: Path to directory to save the file
    """
    filename = uid + '.' + get_file_extension(filename)
    file.save(directory_path / filename)


def insert_upload(uid: str, file_name: str, email: str):
    """
    Insert new upload to the db. The upload can be associated to a registered user or a new user.
    :param uid: str unique id of the upload
    :param file_name: str file name
    :param email: user email
    """
    db = DB()
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
            status=RequestStatusEnum.PENDING,
            user_id=user.id if user else None,
            user=user
        )
        if user:
            user.uploads.append(upload)
            session.add(user)
        else:
            session.add(upload)
        session.commit()


def get_upload(uid=None, filename=None, email=None):
    """
    Given data about, returns the relevant upload.
    :param uid: str unique id of the upload
    :param filename: str file name
    :param email:  user email
    :return: the upload from the database
    """
    db = DB()
    with db.session() as session:
        if uid:
            user_upload = session.query(Upload).filter(Upload.uid == uid).first()
        elif email and filename:
            user = session.query(User).filter(User.email == email).first()
            user_upload = session.query(Upload). \
                filter(Upload.filename == filename, Upload.user_id == user.id). \
                order_by(Upload.id.desc()).first()  # most recent upload
        else:
            return None
        return user_upload


def get_explanation(uid: str, output_directory: Path):
    """
    Checks if there is a json file whose name is the given uid, and returns its content.
    :param uid:  str unique id of the upload
    :param output_directory: Path to the output directory
    :return: the explanation in the json file if exists, None otherwise.
    """
    explanation = None
    output_file_path = next(output_directory.glob(f"{uid}.json"), None)
    if output_file_path:
        with open(output_file_path, 'r') as f:
            explanation = json.loads(f.read())
    return explanation
