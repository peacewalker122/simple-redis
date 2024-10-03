from redistoken import TokenType, tokenize, Token
from serialize import command, Command

import unittest


class TestTokenize(unittest.TestCase):
    def test_elements(self):
        token: Token = tokenize(
            "*5\r\n$3\r\nSET\r\n$3\r\nkey\r\n$5\r\nvalue\r\n$2\r\nEX\r\n$2\r\n10\r\n"
        )
        self.assertEqual(token.token_type, TokenType.BULK_STRING)
        self.assertEqual(token.argc, 5)
        self.assertEqual(token.argv[0], "SET")
        self.assertEqual(token.argv[1], "key")
        self.assertEqual(token.argv[2], "value")
        self.assertEqual(token.argv[3], "EX")
        self.assertEqual(token.argv[4], "10")

        cmd: Command = Command(token)
        self.assertEqual(cmd.cmd, command.SET)
        self.assertEqual(cmd.key, "key")
        self.assertEqual(cmd.value, "value")
        self.assertEqual(cmd.ex, 10)


if __name__ == "__main__":
    unittest.main()
