import json
import asyncio
import websockets

from pyunreal.utils import *
from pyunreal.config import *
from pyunreal.logger import UnrealLogging

logger = UnrealLogging.get_logger(__name__)


class Connection:
    def __init__(self, host: str = DEFAULT_HOST, port: int = DEFAULT_PORT_WEBSOCKET, timeout=None):
        self.host = host
        self.port = port
        self.uri = f"ws://{host}:{port}"
        self.timeout = timeout
        self.websocket = None

    async def __aenter__(self):
        return self

    # close context manager
    async def __aexit__(self, type, value, traceback):
        logger.debug("Closing from context manager")
        await self.close()

    async def connect(self):
        logger.debug(f"Connect to Unreal Engine server - {self.host}:{self.port}")

        try:
            if self.timeout:
                self.websocket = await asyncio.wait_for(websockets.connect(self.uri), self.timeout)
            else:
                self.websocket = await websockets.connect(self.uri)
        except (OSError, asyncio.TimeoutError) as e:
            raise RuntimeError(
                f"ERROR: connecting to {self.host}:{self.port} {e}."
                f"\nIs unreal websocket server running on your computer?")

        latency = await asyncio.wait_for(self.ping(), timeout=5.0)

        try:
            float(latency)
            logger.info(f"Connected...")
            logger.debug(f"Latency: {round(latency, 4)}")
        except ValueError:
            logger.error(f"Couldn't establish connection...")

        return self

    async def ping(self):
        pong_waiter = await self.websocket.ping()
        latency = await pong_waiter

        return latency

    async def close(self):
        if self.websocket:
            await self.websocket.close()
        self.websocket = None
        logger.info("Connection closed...")

    ##############################################################################################################
    #
    # Send command & Receive result
    #
    ##############################################################################################################
    async def _recv(self):
        return await asyncio.wait_for(self.websocket.recv(), self.timeout)

    async def _send(self, data):
        await self.websocket.send(json.dumps(data))

    async def receive(self):
        result = json.loads(await self._recv())
        logger.debug(f"Response code: {result['ResponseCode']}")
        return result

    async def send(self, msg):
        logger.debug(f"Send to server: {msg}")
        await self._send(msg)
