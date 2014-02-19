import os
import sys
import requests

UPLOAD_URL = "http://localhost:5010/upload"

def upload(path):
    abspath = os.path.abspath(path)
    with open(abspath, 'rb') as fd:
        r = requests.post(UPLOAD_URL, files={'file': fd})
        print r.content

if __name__ == '__main__':

    upload(sys.argv[1])