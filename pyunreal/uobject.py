import json
import asyncio
import websockets

from pyunreal.utils import *
from pyunreal.config import *
from pyunreal.logger import UnrealLogging

logger = UnrealLogging.get_logger(__name__)


class UObject:
    def __init__(self):
        raise NotImplementedError
