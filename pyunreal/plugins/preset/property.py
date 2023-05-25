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
    group: str
    client: any

    async def value(self):
        cmd = {
            "MessageName": "http",
            "Parameters": {
                "Url": f"/remote/preset/{self.preset_name}/property/{self.display_name}",
                "Verb": "GET"
            }}
        result = await self.client._execute_cmd(cmd)
        return result['ResponseBody']['PropertyValues'][0]['PropertyValue']

    async def set(self, **kwargs):
        cmd = {
            "MessageName": "http",
            "Parameters": {
                "Url": f"/remote/preset/{self.preset_name}/property/{self.display_name}",
                "Verb": "PUT",
                "Body": {
                    "PropertyValue": kwargs
                }
            }}
        await self.client._execute_cmd(cmd)
