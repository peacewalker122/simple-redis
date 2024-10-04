from serialize import Command, command
from database import ExpiringHashMap


class Processor:
    database: ExpiringHashMap

    def __init__(self):
        self.database = ExpiringHashMap()

    def process(self, cmd: Command):
        if cmd.cmd == command.SET:
            self.database.set(cmd.key, cmd.value, cmd.ex)
            return "OK"
        elif cmd.cmd == command.GET:
            val = self.database.get(cmd.key)
            return val
        elif cmd.cmd == command.ECHO:
            return cmd.value
        elif cmd.cmd == command.PING:
            return "PONG"
