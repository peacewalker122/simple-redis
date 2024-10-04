import time
from redistoken import TokenType, tokenize, Token
from serialize import command, Command
from deserialize import deserialize
from processor import Processor

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

    def test_tokenize(self):
        list = [
            ("*1\r\n$4\r\nPING\r\n", ["PING"]),
            (
                "*5\r\n$3\r\nSET\r\n$3\r\nkey\r\n$5\r\nvalue\r\n$2\r\nEX\r\n$2\r\n10\r\n",
                ["SET", "key", "value", "EX", "10"],
            ),
        ]

        for item in list:
            token = tokenize(item[0])
            self.assertEqual(token.argv, item[1])

    def test_deserialize(self):
        result = deserialize(["Hello World!"], argc=1)
        self.assertEqual(result, "+Hello World!\r\n")

        result = deserialize(["Hello World!"], argc=1, is_error=True)
        self.assertEqual(result, "-Hello World!\r\n")

        result = deserialize(["TEST", "Hello World!"], argc=2)
        self.assertEqual(result, "*2\r\n$4\r\nTEST\r\n$12\r\nHello World!\r\n")

        result = deserialize(["PONG"], argc=1)
        self.assertEqual(result, "+PONG\r\n")

        result = deserialize([100], argc=1)
        self.assertEqual(result, ":100\r\n")

    def test_command(self):
        cmd = Command(
            tokenize(
                "*5\r\n$3\r\nSET\r\n$3\r\nkey\r\n$5\r\nvalue\r\n$2\r\nEX\r\n$2\r\n10\r\n"
            )
        )
        self.assertEqual(cmd.cmd, command.SET)
        self.assertEqual(cmd.key, "key")
        self.assertEqual(cmd.value, "value")
        self.assertEqual(cmd.ex, 10)

    def test_processor_set_and_get(self):
        processor = Processor()
        cmd = Command(
            tokenize(
                "*5\r\n$3\r\nSET\r\n$3\r\nkey\r\n$5\r\nvalue\r\n$2\r\nEX\r\n$2\r\n10\r\n"
            )
        )
        result = processor.process(cmd)
        self.assertEqual(result, "OK")

        cmd = Command(tokenize("*2\r\n$3\r\nGET\r\n$3\r\nkey\r\n"))
        result = processor.process(cmd)
        self.assertEqual(result, "value")

        time.sleep(10)

        result = processor.process(cmd)
        self.assertEqual(result, None)

    def test_processor_echo(self):
        processor = Processor()
        cmd = Command(tokenize("*2\r\n$4\r\nECHO\r\n$5\r\nHello\r\n"))
        result = processor.process(cmd)
        self.assertEqual(result, "Hello")

    def test_processor_ping(self):
        processor = Processor()
        cmd = Command(tokenize("*1\r\n$4\r\nPING\r\n"))
        result = processor.process(cmd)
        self.assertEqual(result, "PONG")


if __name__ == "__main__":
    unittest.main()
