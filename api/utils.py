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
           get_file_extension(filename).lower() in ALLOWED_EXTENSIONS


def get_file_extension(filename: str) -> str:
    return filename.rsplit('.', 1)[1]


def save_file(file: FileStorage, filename: str, uid: str, directory_path: Path):
    """
    Saves the file in the received directory path
    :param file: FileStorage file
    :param filename: str file name
    :param uid: str unique id
    :param directory_path: Path to directory to save the file
    """
    filename = uid + get_file_extension(filename)
    file.save(directory_path / filename)
