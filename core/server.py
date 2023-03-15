import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from core.gamestate import GameState
from typing import Callable


class DotaGSIRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers["Content-length"])
        self.server.gamestate.loads(json.loads(self.rfile.read(length)))


class DotaGSIServer(HTTPServer):
    def __init__(self, *args, **kwargs):
        self.gamestate = GameState()
        super().__init__(*args, **kwargs)

    def run(self):
        self.serve_forever()


def get_server(server_class=DotaGSIServer, handler_class=DotaGSIRequestHandler, server_address=("", 1417)):
    httpd = server_class(server_address, handler_class)

    return httpd
