import heapq
import logging
import time

log = logging.getLogger(__name__)


class ExpiringHashMap:
    def __init__(self):
        self.map = {}
        self.expiry_heap = []  # Min-heap to track expiration times.

    def set(self, key, value, ttl):
        """
        param ttl: time in seconds
        """
        expiry_time = time.time() + ttl

        log.debug(
            f"set: {key}, {value}, {ttl}, {expiry_time}",
            extra={"key": key, "value": value, "ttl": ttl, "expiry_time": expiry_time},
        )
        self.map[key] = value
        if ttl > 0:  # if the ttl is not 0 it means save forever.
            heapq.heappush(self.expiry_heap, (expiry_time, key))

    def get(self, key):
        self.cleanup()  # Remove expired items.
        return self.map.get(key, None)

    def cleanup(self):
        """Remove all expired entries from the hashmap."""
        current_time = time.time()
        while self.expiry_heap and self.expiry_heap[0][0] <= current_time:
            expiry_time, key = heapq.heappop(self.expiry_heap)
            if key in self.map and time.time() >= expiry_time:
                log.debug(f"cleanup: {key}", extra={"key": key})
                del self.map[key]


if __name__ == "__main__":
    # Example usage:
    exp_map = ExpiringHashMap()
    exp_map.set("foo", "bar", ttl=5)
    time.sleep(6)
    print(exp_map.get("foo"))
