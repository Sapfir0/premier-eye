
from http.server import BaseHTTPRequestHandler, HTTPServer
PORT = 8010
paramChanged = False


class TestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        global paramChanged
        content_len = int(self.headers.get('Content-Length'))
        post_body: bytes = self.rfile.read(content_len)
        print(post_body.decode())
        paramChanged = True
        #self.send_response(200, "It's ok".encode())
        self.wfile.write("sd".encode())  # не робит тоже


async def startServer():
    myServer = HTTPServer(("localhost", PORT), TestHandler)
    myServer.serve_forever()


startServer()