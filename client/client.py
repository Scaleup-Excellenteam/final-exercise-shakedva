import requests
from .status import Status


class Client:
    """
    Makes requests for the app
    """

    def __init__(self, url: str) -> None:
        """
        :param url: make requests to the url
        """
        self.url = url

    def upload(self, file_path: str) -> str:
        """
        Make a request to upload a file to the app.
        :param file_path: to a pptx file to upload.
        :return: UID from the response.
        :raise Exception: status code - when the response contains error code.
        """
        with open(file_path, 'rb') as f:
            response = requests.post(
                f"{self.url}/upload",
                files={'file': f}
            )
        if response:  # True if the status code was between 200 and 400
            return response.json()['uid']
        raise Exception(response.status_code)

    def status(self, uid: str) -> Status:
        """
        Make a request to receive the status of the output
        :param uid: str the uid received in the upload request
        :return: Status of the output
        :raise Exception: when the response contained error
        """
        response = requests.get(
            f"{self.url}/uid/{uid}"
        )
        if response:
            response_json = response.json()
            status = Status(
                response_json['status'],
                response_json['filename'],
                response_json['timestamp'],
                response_json['explanation'],
            )
            if status.not_found:
                raise Exception("UID not found")
            return status
