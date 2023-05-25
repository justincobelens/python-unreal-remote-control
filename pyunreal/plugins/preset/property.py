from dataclasses import dataclass

from pyunreal.logger import UnrealLogging

logger = UnrealLogging.get_logger(__name__)


@dataclass
class PresetProperty:
    ID: str
    display_name: str
    underlying_property: dict
    metadata: dict
    owners: list
    preset_name: str
    group: str = '1'

    def value(self):
        raise NotImplementedError

    def set(self, **kwargs):
        raise NotImplementedError
