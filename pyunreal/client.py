from pyunreal.config import DEFAULT_HOST, DEFAULT_PORT_WEBSOCKET, DEFAULT_TIMEOUT
from pyunreal.command.host import Host
from pyunreal.connection import Connection
from pyunreal.logger import UnrealLogging

logger = UnrealLogging.get_logger(__name__)


class Client(Host):
    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT_WEBSOCKET):
        self.host = host
        self.port = port
        self.conn = Connection.get_instance()

    async def create_connection(self, timeout=DEFAULT_TIMEOUT):
        if self.conn.websocket is None:
            await self.conn.connect()
        return self.conn

    async def close_connection(self):
        await self.conn.close()

    async def preset(self, name):
        presets = await self.presets()

        for preset in presets:
            if preset.name == name:
                await preset.refresh()
                return preset
        return None
