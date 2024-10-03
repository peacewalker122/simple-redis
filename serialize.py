from typing import List, Optional
from redistoken import Token, TokenType, atoi
from enum import Enum, auto


class command(Enum):
    SET = 1
    GET = 2
    UNKNOWN = auto()

    @classmethod
    def from_string(cls, cmd: str):
        cmd = cmd.lower()
        if cmd == "set":
            return cls.SET
        elif cmd == "get":
            return cls.GET
        else:
            return cls.UNKNOWN


class Command:
    argv: List[str]
    argc: int
    cmd: command

    ex: int = 0
    px: int = 0
    nx: bool = False
    xx: bool = False
    ch: bool
    ge: int
    le: int
    gt: int
    lt: int
    key: Optional[str]
    value: Optional[str]

    def __init__(self, token: Token):
        self.argc = token.argc
        self.argv = token.argv

        if token.argc < 1:
            raise Exception("Invalid command")

        self.cmd = command.from_string(self.argv[0])

        index = 1

        match self.cmd:
            case command.SET:
                self.key = self.argv[index]
                index += 1
                self.value = self.argv[index]
                index += 1

                if index < self.argc and self.argv[index] == "EX":
                    try:
                        self.ex = int(self.argv[index + 1])
                        index += 1
                    except:
                        raise Exception("Invalid command")
