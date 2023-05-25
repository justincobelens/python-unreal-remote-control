from dataclasses import dataclass

from pyunreal.logger import UnrealLogging

logger = UnrealLogging.get_logger(__name__)


# TODO: change to .get(key, []) to prevent error from empty or missing keys/values

@dataclass
class PresetGroup:
    name: str
    properties: dict
    functions: dict
    actors: dict
    preset_name: str

    def get_property(self, property_name: str):
        return self.properties[property_name]

    def get_function(self, function_name):
        return self.functions[function_name]

    def get_actor(self, actor_name: str):
        return self.actors[actor_name]
