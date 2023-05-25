from typing import List, Dict
from dataclasses import dataclass

from pyunreal.command import Command
from pyunreal.plugins.preset.property import PresetProperty
from pyunreal.plugins.preset.function import PresetFunction
from pyunreal.plugins.preset.group import PresetGroup
from pyunreal.plugins.preset.actor import PresetActor

from pyunreal.logger import UnrealLogging

logger = UnrealLogging.get_logger(__name__)

# TODO: change to .get(key, []) to prevent error from empty or missing keys/values


@dataclass
class PresetBase(Command):
    client: any
    name: str
    ID: str
    path: str

    async def _get_preset_info(self):
        cmd = {
            "MessageName": "http",
            "Parameters": {
                "Url": f"/remote/preset/{self.name}",
                "Verb": "GET"
            }
        }

        result = await self.client._execute_cmd(cmd)
        self._preset_info = result['ResponseBody']

    async def _setup_preset(self):
        await self._get_preset_info()

        self._groups = await self._init_group_list()
        self._actors = await self._init_actor_list()

    async def _init_property(self, group: str, info: dict) -> PresetProperty:
        prop = PresetProperty(info['ID'],
                              info['DisplayName'],
                              info['UnderlyingProperty'],
                              info['Metadata'],
                              info['OwnerObjects'],
                              self.name,
                              group)
        return prop

    async def _init_function(self, group: str, info: dict) -> PresetFunction:
        func = PresetFunction(info['ID'],
                              info['DisplayName'],
                              info['UnderlyingFunction'],
                              info['OwnerObjects'],
                              self.name,
                              group)
        return func

    async def _init_actor(self, group: str, info: dict) -> PresetActor:
        actor = PresetActor(info["ID"],
                            info["DisplayName"],
                            info["UnderlyingActor"],
                            self.name,
                            group)
        return actor

    async def _init_group(self, group_info: dict) -> PresetGroup:
        group_name = group_info['Name']
        properties = {prop['DisplayName']: await self._init_property(group_name, prop)
                      for prop in group_info.get('ExposedProperties', [])}
        functions = {func['DisplayName']: await self._init_function(group_name, func)
                     for func in group_info.get('ExposedFunctions', [])}
        actors = {act['DisplayName']: await self._init_actor(group_name, act)
                  for act in group_info.get('ExposedActors', [])}

        group = PresetGroup(name=group_name,
                            properties=properties,
                            functions=functions,
                            actors=actors,
                            preset_name=self.name)
        return group

    async def _init_group_list(self):
        return {group['Name']: await self._init_group(group) for group in self._preset_info['Preset']['Groups']}

    async def _init_actor_list(self):
        actors = {}
        for group in self._preset_info['Preset']['Groups']:
            for actor in group['ExposedActors']:
                actors[actor['DisplayName']] = await self._init_actor(group['Name'], actor)
        return actors

    async def _init_property_list(self):
        properties = {}
        for group in self._preset_info['Preset']['Groups']:
            for prop in group['ExposedProperties']:
                prop = await self._init_property(group, prop)
                properties[prop.display_name] = prop
        return properties

    async def _init_func_dict(self):
        funcs = {}
        for group in self._preset_info['Preset']['Groups']:
            for func in group['ExposedFunctions']:
                func = await self._init_function(group['Name'], func)
                funcs[func.display_name] = func
        return funcs

    async def refresh(self):
        await self._setup_preset()


# TODO: change to .get(key, []) to prevent error from empty or missing keys/values

@dataclass
class Preset(PresetBase):

    async def get_metadata(self):
        raise NotImplementedError

    async def get_all_groups(self) -> Dict[str, PresetGroup]:
        return self._groups

    async def get_group(self, group_name: str) -> PresetGroup:
        groups = await self.get_all_groups()
        return groups[group_name]

    async def get_all_actors(self) -> Dict[str, PresetActor]:
        return self._actors

    async def get_actor(self, actor_name: str) -> PresetActor:
        actors = await self.get_all_actors()
        return actors[actor_name]

    def get_all_property_names(self) -> List[str]:
        raise NotImplementedError

    def get_property(self, property_name: str) -> PresetProperty:
        raise NotImplementedError

    def get_all_function_name(self) -> List[str]:
        raise NotImplementedError

    def get_function(self, function_name: str) -> PresetFunction:
        raise NotImplementedError
