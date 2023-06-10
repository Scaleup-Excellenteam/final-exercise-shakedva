import argparse
import sys
import time

import requests
from status import Status


class Client:
    def __init__(self, url: str) -> None:
        self.url = url

    def upload(self, file_path: str) -> str:
        with open(file_path, 'rb') as f:
            response = requests.post(
                f"{self.url}/upload",
                files={'file': f}
            )
        if response:  # True if the status code was between 200 and 400
            return response.json()['uid']
        raise Exception(response.status_code)

    def status(self, uid: str) -> Status:
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--url",
        type=str,
        help="API server url",
        default='http://localhost:5000'
    )
    args = parser.parse_args()
    client = Client(args.url)

    pptx_file_path = "C:\\Users\\shake\\Desktop\\College\\4th Year\\Semester B\\Excellenteam\\python\\Ex\\Tests.pptx"
    uid = client.upload(pptx_file_path)
    client.status(uid)


if __name__ == '__main__':
    main()
