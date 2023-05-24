from pyunreal.command import Command
class Host(Command):
    def _execute_cmd(self, cmd, with_response=True):
        with self.create_connection() as conn:
            raise NotImplementedError


    def presets(self, state=None):
        raise NotImplementedError

    def version(self):
        return 1