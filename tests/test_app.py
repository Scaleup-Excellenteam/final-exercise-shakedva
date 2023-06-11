import pytest
import subprocess
from api.request_status_enum import RequestStatusEnum
from client.client import Client
import sys
from pathlib import Path
import time

URL = "http://localhost:5000"
FILE_NAME = "sample_presentation.pptx"
SLEEP_DURATION = 200


@pytest.fixture(scope='session')
def server_process():
    process = subprocess.Popen([
        sys.executable,
        '-m',
        'api.app'
    ])
    yield process
    process.kill()


@pytest.fixture(scope='session')
def checker_process():
    process = subprocess.Popen([
            sys.executable,
            '-m',
            'explainer.gpt_explainer_checker'
    ])
    yield process
    process.kill()


def test_system(server_process, checker_process):
    """
    System test that starts the server and the explainer.
    Uploads a sample presentation and checks the status after few minutes.
    :param server_process: Fixture that runs the flask app
    :param checker_process: Fixture that runs the explainer
    """
    client = Client(URL)
    uid = client.upload(str(Path(Path.cwd() / FILE_NAME)))
    time.sleep(3)
    s = client.status(uid)
    assert s.status == RequestStatusEnum.PENDING
    time.sleep(SLEEP_DURATION)
    s = client.status(uid)
    assert s.is_done

