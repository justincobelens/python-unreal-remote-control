from dataclasses import dataclass

from pyunreal.command import Command
from pyunreal.logger import UnrealLogging

logger = UnrealLogging.get_logger(__name__)


@dataclass
class PresetGroup:
    name: str
    properties: dict
    functions: dict
    actors: dict
    preset_name: str

    def get_property(self):
        raise NotImplementedError

    def get_function(self):
        raise NotImplementedError

    def get_actor(self):
        raise NotImplementedError