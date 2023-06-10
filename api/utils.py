from datetime import datetime

ALLOWED_EXTENSIONS = {'pptx'}


def allowed_file(filename: str):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_file(file, file_name, uid, directory_path):
    data = (datetime.now().strftime('%Y-%m-%d-%H-%M-%S'), uid, file_name)
    file_name = '_'.join(data)
    file.save(directory_path / file_name)
