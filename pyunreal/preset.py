from abc import ABC
from dataclasses import dataclass

from pyunreal.plugins.preset.property import PresetProperty
from pyunreal.plugins.preset.function import PresetFunction
from pyunreal.plugins.preset.group import PresetGroup
from pyunreal.plugins.preset.actor import PresetActor

from pyunreal.logger import UnrealLogging

logger = UnrealLogging.get_logger(__name__)


@dataclass
class PresetBase:
    client: any  # TODO: Fix this type hinting
    name: str
    ID: str
    path: str

    async def _create_connection(self, timeout=None):
        conn = await self.client.create_connection(timeout=timeout)
        logger.debug("Created connection from Preset class")
        return conn

    async def _execute_cmd(self, cmd, with_response=True):
        async with await self._create_connection() as conn:
            await conn.send(cmd)
            if with_response:
                result = await conn.receive()
                return result
            # else:
            # await conn.check_status()

    async def _get_preset_info(self):
        cmd = {
            "MessageName": "http",
            "Parameters": {
                "Url": f"/remote/preset/{self.name}",
                "Verb": "GET"
            }
        }

        result = await self._execute_cmd(cmd)
        self._preset_info = result['ResponseBody']

    async def _setup_preset(self):
        await self._get_preset_info()

        self._groups = await self._init_group_list()
        # self._actors = await self._init_actor_list()

    async def _init_property(self):
        raise NotImplementedError

    async def _init_function(self):
        raise NotImplementedError

    async def _init_group(self, group_info):
        group_name = group_info['Name']

        group = PresetGroup(name=group_name,
                            properties={},
                            function={},
                            actors={},
                            preset_name={})
        return

    async def _init_actor(self):
        raise NotImplementedError

    async def _init_group_list(self):
        return [self._init_group(group_info) for group_info in self._preset_info['Preset']['Groups']]

    async def _init_actor_list(self):
        raise NotImplementedError

    async def _init_property_list(self):
        raise NotImplementedError

    async def _init_func_dict(self):
        raise NotImplementedError

    async def refresh(self):
        await self._setup_preset()


@dataclass
class Preset(PresetBase):  # , Property, Function, Group, Actor, ABC
    async def get_all_groups(self):
        return self._groups


# p = Preset()
#
# p.val
