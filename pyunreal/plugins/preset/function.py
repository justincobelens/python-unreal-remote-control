from dataclasses import dataclass

from pyunreal.logger import UnrealLogging

logger = UnrealLogging.get_logger(__name__)


@dataclass
class PresetFunction:
    ID: str
    display_name: str
    underlying_function: dict
    owners: list
    preset_name: str
    group: str


