import struct
import websockets

from pyunreal.config import DEFAULT_HOST, DEFAULT_PORT_WEBSOCKET
from pyunreal.utils.logger import UnrealLogging


logger = UnrealLogging.get_logger(__name__)
class Connection:
    class Connection:
        def __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT_WEBSOCKET, timeout=None):
            self.host = host
            self.port = port
            self.uri = f"ws://{host}:{port}"
            self.timeout = timeout
            self.websocket = None

        # open context manager
        def __enter__(self):
            return self

        # close context manager
        def __exit__(self, type, value, traceback):
            self.close()

        def connect(self):
            logger.debug(f"Connect to Unreal Engine server - {self.host}:{self.port}")
            raise NotImplementedError

        def close(self):
            raise NotImplementedError