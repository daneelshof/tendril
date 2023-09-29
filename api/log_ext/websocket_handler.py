from logging import StreamHandler
from websocket import create_connection


class WebSocketHandler(StreamHandler):

    def __init__(self, ws_url):
        StreamHandler.__init__(self)
        self.ws_server = ws_url

    def emit(self, record):
        log_message = self.format(record)
        websocket = create_connection(self.ws_server)
        websocket.send(log_message)
        websocket.close()
