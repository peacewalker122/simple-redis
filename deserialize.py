from typing import Any, List


def deserialize(value: List[Any], is_error: bool = False, argc: int = 0) -> str:
    if argc < 1 and len(value) < 1:
        return "$-1\r\n"  # nil value

    if is_error:
        return f"-{value[0]}\r\n"

    if argc == 1 and value[0] == None:
        return "$-1\r\n"

    if isinstance(value[0], int) and argc == 1:
        return f":{value[0]}\r\n"

    if argc == 1:
        return f"+{value[0]}\r\n"

    result = f"*{argc}\r\n"

    for i in range(0, argc):
        if isinstance(value[i], int):
            result += f":{value[i]}\r\n"
        else:
            result += f"${len(value[i])}\r\n{value[i]}\r\n"
    return result
