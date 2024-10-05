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
            return [cmd.key, val]
        elif cmd.cmd == command.ECHO:
            return cmd.value
        elif cmd.cmd == command.PING:
            return "PONG"
        elif cmd.cmd == command.CONFIG:
            return [cmd.argv[2], "900 1 300 10 60 10000"]
        elif cmd.cmd == command.INFO:
            return """
redis_version:6.2.5
redis_git_sha1:00000000
redis_git_dirty:0
redis_build_id:a1b2c3d4e5f6g7h8
redis_mode:standalone
os:Linux 4.15.0-54-generic x86_64
arch_bits:64
multiplexing_api:epoll
gcc_version:7.5.0
process_id:12345
run_id:f91e4a2f57b11234567890abcdef123456789012
tcp_port:6379
uptime_in_seconds:123456
uptime_in_days:1
hz:10
configured_hz:10
lru_clock:1234567
executable:/usr/local/bin/redis-server
config_file:/etc/redis/redis.conf
"""
