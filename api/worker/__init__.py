import os
import logging
from log_ext import WebSocketHandler


log_format = '%(asctime)s [%(levelname)s]: %(module)s#%(lineno)d - %(message)s'

logging.basicConfig(
        format=log_format,
        encoding='utf-8',
        level=logging.DEBUG
    )

ws_handler = WebSocketHandler(os.getenv('WEBSOCKET_SERVER'))
ws_handler.setLevel(logging.DEBUG)
ws_handler.setFormatter(logging.Formatter(log_format))
logging.getLogger().addHandler(ws_handler)
