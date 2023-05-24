from pyunreal.config import DEFAULT_HOST, DEFAULT_PORT_WEBSOCKET
from pyunreal.command.host import Host
from pyunreal.connection import Connection

class Client(Host):
    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT_WEBSOCKET):
        self.host = host
        self.port = port

    def create_connection(self, timeout=None):
        conn = Connection(self.host, self.port, timeout)
        conn.connect()
        return conn

    def preset(self, serial):
        presets = self.presets()

        for preset in presets:
            if preset.serial == serial:
                return preset
        return None