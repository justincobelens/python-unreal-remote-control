from dataclasses import dataclass

from pyunreal.logger import UnrealLogging

logger = UnrealLogging.get_logger(__name__)

# TODO: change to .get(key, []) to prevent error from empty or missing keys/values


@dataclass
class PresetActor:
    ID: str
    display_name: str
    underlying_actor: dict
    preset_name: str
    group: str

    @property
    def actor_path(self):
        return self.underlying_actor['path']

    @property
    def actor_class(self):
        return self.underlying_actor['Class']

    @property
    def actor_name(self):
        return self.underlying_actor['name']

