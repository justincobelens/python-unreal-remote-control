import asyncio
import websockets
import json

from pyunreal.config import DEFAULT_HOST, DEFAULT_PORT_WEBSOCKET, DEFAULT_TIMEOUT
from pyunreal.logger import UnrealLogging

logger = UnrealLogging.get_logger(__name__)


class Connection:
    _instance = None

    def __init__(self, host: str = DEFAULT_HOST, port: int = DEFAULT_PORT_WEBSOCKET, timeout=DEFAULT_TIMEOUT):
        if Connection._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.host = host
            self.port = port
            self.uri = f"ws://{host}:{port}"
            self.timeout = timeout
            self.websocket = None
            Connection._instance = self
            self.retry_attempted = False

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls()
        return cls._instance

    async def connect(self, max_retries=3):
        """
        Connect to the Unreal Engine server. If the connection fails, retry up to max_retries times with exponential backoff.
        """
        for retry in range(max_retries):
            try:
                if self.timeout:
                    self.websocket = await asyncio.wait_for(websockets.connect(self.uri), self.timeout)
                else:
                    self.websocket = await websockets.connect(self.uri)
            except (OSError, asyncio.TimeoutError) as e:
                if retry < max_retries - 1:  # If this is not the last retry
                    wait_time = (2 ** retry)  # Exponential backoff
                    logger.warning(f"Connection failed, retrying after {wait_time} seconds...")
                    await asyncio.sleep(wait_time)  # Non-blocking sleep
                else:  # If this is the last retry
                    logger.error(f"RuntimeError: connecting to {self.host}:{self.port} {e}")
                    raise RuntimeError(
                        f"ERROR: connecting to {self.host}:{self.port} {e}."
                        f"\nIs unreal websocket server running on your computer?")
            else:  # If the connection was successful
                latency = await asyncio.wait_for(self.ping(), timeout=5.0)
                try:
                    float(latency)
                    logger.info(f"Connected...")
                    logger.debug(f"Latency: {round(latency, 4)}")
                except ValueError:
                    logger.error(f"Couldn't establish connection...")
                return self  # Return the connection

    async def ping(self):
        """
        Send a ping message to the server and return the latency.
        """
        pong_waiter = await self.websocket.ping()
        latency = await pong_waiter

        return latency

    async def close(self):
        """
        Close the connection to the server.
        """
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
        """
        Receive a message from the server.
        """
        return await asyncio.wait_for(self.websocket.recv(), self.timeout)

    async def _send(self, data):
        """
        Send a message to the server.
        """
        await self.websocket.send(json.dumps(data))

    async def receive(self):
        """
        Receive a message from the server and return the result.
        """
        result = json.loads(await self._recv())
        logger.debug(f"Response code: {result['ResponseCode']}")
        return result

    async def send(self, msg):
        """
        Send a message to the server.
        """
        logger.debug(f"Send to server: {msg}")
        await self._send(msg)
