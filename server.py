import socket
import logging
from typing import List

from redistoken import tokenize
from serialize import Command
from processor import Processor
from deserialize import deserialize

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)


class Server:
    host: str
    port: int
    processor: Processor

    def __init__(self, host: str = "127.0.0.1", port: int = 6379):
        self.host = host
        self.port = port
        self.processor = Processor()

    def run(self):
        logging.warning(f"Starting server on {self.host}:{self.port}")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            while True:
                conn, addr = s.accept()

                logging.info(f"Connection from {addr[0]}:{addr[1]}")
                with conn:
                    while True:
                        try:
                            buffer = ""
                            argc = 0
                            while True:
                                data = conn.recv(1024).decode()
                                if not data:
                                    break

                                logging.info(f"recv: {data}")

                                if not argc:
                                    argc = self._get_argc(data) * 2

                                buffer += data

                                if len(buffer.splitlines()) >= argc:
                                    result = self._process(buffer)
                                    conn.sendall(result.encode())
                                    buffer = ""
                                    argc = 0
                        except Exception as e:
                            logging.error(e, exc_info=True)
                            break
                        finally:
                            conn.close()

    def _get_argc(self, cmd: str) -> int:
        if cmd.startswith("*"):
            result = 0
            for i in range(1, len(cmd)):
                if cmd[i].isdigit():
                    result = result * 10 + int(cmd[i])

            return result

        return 0

    def _process(self, arg: str) -> str:
        try:
            logging.debug(f"arg: {arg}")
            token = tokenize(arg)
            cmd = Command(token)

            logging.debug(f"cmd: {cmd.cmd}")

            result = self.processor.process(cmd)

            return deserialize(
                [result] if not isinstance(result, List) else result,
                argc=1 if not isinstance(result, List) else len(result),
            )
        except Exception as e:
            return deserialize([str(e)], argc=1, is_error=True)
