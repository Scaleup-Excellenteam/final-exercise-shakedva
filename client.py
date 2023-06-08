import sys
import requests


def send_pptx_file(url: str, pptx_file_path: str):
    files = {'file': open(pptx_file_path, 'rb')}
    response = requests.post(url, files=files)
    return response


def main():
    url = 'http://localhost:5000'
    pptx_file_path = sys.argv[1]
    response = send_pptx_file(url, pptx_file_path)
    print(response.status_code)
    print(response.text)


if __name__ == '__main__':
    main()

