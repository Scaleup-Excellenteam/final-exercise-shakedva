import requests
from .status import Status
import time


class Client:
    """
    Makes requests for the app
    """

    def __init__(self, url: str) -> None:
        """
        :param url: make requests to the url
        """
        self.url = url

    def upload(self, file_path: str, email=None) -> str:
        """
        Make a request to upload a file to the app.
        :param file_path: to a pptx file to upload.
        :param email: email address of the user.
        :return: UID from the response.
        :raise Exception: status code - when the response contains error code.
        """
        with open(file_path, 'rb') as f:
            response = requests.post(
                f"{self.url}/upload",
                files={'file': f},
                data={'email': email}
            )
        if response:  # True if the status code was between 200 and 400
            return response.json()['uid']
        raise Exception(response.status_code)

    def status(self, **request_args) -> Status:
        """
        Make a request to receive the status of the output
        :param uid: str the uid received in the upload request
        :return: Status of the output
        :raise Exception: when the response contained error
        """
        response = requests.get(
            f"{self.url}/status",
            params=request_args
        )
        if response:
            response_json = response.json()
            status = Status(
                response_json['status'],
                response_json['filename'],
                response_json['finish_time'],
                response_json['explanation'],
            )
            if status.not_found:
                raise Exception("UID not found")
            return status


def main():
    client = Client('http://localhost:5000')
    pptx_file_path = "C:\\Users\\shake\\Desktop\\College\\4th Year\\Semester B\\Excellenteam\\python\\Ex\\Tests.pptx"
    uid1 = client.upload(pptx_file_path, 'shaked@example.com')

    # pptx_file_path = "C:\\Users\\shake\\Desktop\\asyncio-intro.pptx"
    # client.upload(pptx_file_path, 'shaked@example2.com')

    # while True:
    #     time.sleep(10)
    #     try:
    #         # status = client.status(uid=uid1)
    #         status = client.status(email='shaked@example2.com', filename='asyncio-intro.pptx')
    #         if not status:
    #             raise Exception("Not done yet.")
    #         else:
    #             break
    #     except Exception as e:
    #         print(e)


if __name__ == '__main__':
    main()
