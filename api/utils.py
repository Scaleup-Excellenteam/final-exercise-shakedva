from datetime import datetime
from pathlib import Path

from werkzeug.datastructures.file_storage import FileStorage
ALLOWED_EXTENSIONS = {'pptx'}


def allowed_file(filename: str) -> bool:
    """
    Returns whether the file is within allowed types.
    :param filename: str file name.
    :return:
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_file(file: FileStorage, file_name: str, uid: str, directory_path: Path):
    """
    Saves the file in the received directory path
    :param file: FileStorage file
    :param file_name: str file name
    :param uid: str unique id
    :param directory_path: Path to directory to save the file
    """
    data = (datetime.now().strftime('%Y-%m-%d-%H-%M-%S'), uid, file_name)
    file_name = '_'.join(data)
    file.save(directory_path / file_name)
