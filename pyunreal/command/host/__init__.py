from pyunreal.preset import Preset
from pyunreal.command import Command
from pyunreal.logger import UnrealLogging

logger = UnrealLogging.get_logger(__name__)


class Host(Command):
    async def _execute_cmd(self, cmd, with_response=True):
        conn = await self.create_connection()
        # logger.debug("Host execute command")
        await conn.send(cmd)
        if with_response:
            result = await conn.receive()
            return result

    async def info(self):
        cmd = {
            "MessageName": "http",
            "Parameters": {
                "Url": "/remote/info",
                "Verb": "GET"
            }
        }

        return await self._execute_cmd(cmd)

    async def presets(self):
        cmd = {
            "MessageName": "http",
            "Parameters": {
                "Url": "/remote/presets",
                "Verb": "GET"
            }
        }

        result = await self._execute_cmd(cmd)

        presets = []

        # TODO: Add try except incase no preset found
        for preset in result['ResponseBody']['Presets']:
            presets.append(Preset(client=self,
                                  name=preset['Name'],
                                  ID=preset['ID'],
                                  path=preset['Path']))

        if len(presets) > 0:
            logger.info(f"Presets found: [{[preset.name for preset in presets]}]")
        else:
            logger.info(f"No presets found")

        return presets



    def version(self):
        return 1

    def remote_connect(self, host, port):
        return NotImplementedError

    def remote_disconnect(self, host, port):
        return NotImplementedError

    def disconnect_all(self):
        raise NotImplementedError
