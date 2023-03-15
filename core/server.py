import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from core.gamestate import GameState


class DotaGSIRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        """Send data to GameState class
        """
        length = int(self.headers["Content-length"])
        self.server.gamestate.loads(json.loads(self.rfile.read(length)))


class DotaGSIServer(HTTPServer):
    def __init__(self, *args, **kwargs):
        self.gamestate = GameState()
        super().__init__(*args, **kwargs)


def get_server(server_class=DotaGSIServer, handler_class=DotaGSIRequestHandler, server_address=("", 1417)) -> HTTPServer:
    """Returns server instance with specified parameters.

    Args:
        server_class (HTTPServer, optional): HTTP server class. Defaults to DotaGSIServer.
        handler_class (HTTPRequestHandler, optional): HTTP request handler class. Defaults to DotaGSIRequestHandler.
        server_address (tuple, optional): IP address and port in tuple. Defaults to ("", 1417).

    Returns:
        HTTPServer: HTTP server object.
    """
    httpd = server_class(server_address, handler_class)

    return httpd
