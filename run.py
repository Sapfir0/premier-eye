import subprocess
from threading import Thread
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = 8010
paramChanged = False
mainPID = None

class TestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        global paramChanged
        content_len = int(self.headers.get('Content-Length'))
        post_body: bytes = self.rfile.read(content_len)
        print(post_body.decode())  # TODO тут будет записыватьт в енв файл наши измененные параметры
        paramChanged = True


def startServer():
    myServer = HTTPServer(("localhost", PORT), TestHandler)
    myServer.serve_forever()


def killProcess(pid):
    subprocess.Popen('taskkill /F /PID {0}'.format(pid), shell=True)


def runProgram():
    global paramChanged, mainPID

    if paramChanged:
        killProcess(mainPID)
        paramChanged = False
    else:
        import os
        path = os.path.join(os.path.split(__file__)[0], "mainImage.py")
        pid = subprocess.Popen(["python", path]).pid
        mainPID = pid


Thread(target=startServer).start()
Thread(target=runProgram).start()
