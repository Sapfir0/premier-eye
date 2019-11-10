import subprocess
from threading import Thread
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
from settings import Settings as cfg

PORT = 8010
paramChanged = False
paramValue = None
mainPID = None


class TestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        global paramChanged, paramValue
        content_len = int(self.headers.get('Content-Length'))
        post_body: bytes = self.rfile.read(content_len)
        paramChanged = True
        paramValue = post_body.decode()  # TODO тут будет записыватьт в енв файл наши измененные параметры


def startServer():
    myServer = HTTPServer(("localhost", PORT), TestHandler)
    myServer.serve_forever()


def killProcess(pid):
    subprocess.Popen('taskkill /F /PID {0}'.format(pid), shell=True)


def changeStringInFileTo():
    def detectLine():
        stringWithParam = 0
        with open(filepath, 'r') as f:
            for line in f.readlines():
                paramName = re.findall(r'\w=', paramValue)
                if paramName[0] in line:
                    break
                stringWithParam += 1
        return stringWithParam

    import re
    filepath = os.path.join(cfg.APP_PATH, ".env")

    if not paramValue:
        raise Exception("None param value")
    stringWithParam = detectLine()
    with open(filepath, 'w') as f:
        for i in range(stringWithParam):
            f.readline()
        f.writelines(paramValue)


def runProgram():
    global paramChanged, mainPID
    #while True:  # цикл №0  ломает все
    if paramChanged:
        killProcess(mainPID)
        paramChanged = False
        # изменить конфиг в енв
        changeStringInFileTo()
    else:
        path = os.path.join(cfg.APP_PATH, "mainImage.py")
        pid = subprocess.Popen(["python", path]).pid
        mainPID = pid


Thread(target=startServer).start()
Thread(target=runProgram).start()
