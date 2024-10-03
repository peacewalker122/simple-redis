from enum import Enum, auto
from typing import List, Tuple
from unittest import result


class TokenType(Enum):
    BULK_STRING = 1
    ARRAY = 2
    INTEGER = 3
    SIMPLE_STRING = 4
    ERROR = 5
    UNKNOWN = auto()


class Token:
    token_type: TokenType
    argc: int
    argv: List[str]

    def __init__(self):
        self.argc = 0
        self.argv = []


def atoi(val: str, index: int = 0) -> Tuple[int, int]:
    result = 0

    while index < len(val) and val[index].isdigit():
        result = result * 10 + int(val[index])
        index += 1

    return result, index


def tokenize(val: str) -> Token:
    index = 0
    result: Token = Token()

    if val[index] != "*":
        raise Exception("Invalid token")
    index += 1

    (elements, index) = atoi(val, index)
    result.argc = elements
    index += 2  # jump over \r\n

    for _ in range(0, elements):
        if val[index] == "$":
            index += 1
            result.token_type = TokenType.BULK_STRING
            (length, index) = atoi(val, index)
            index += 2
            result.argv.append(val[index : index + length])
            index += length + 2

    return result
