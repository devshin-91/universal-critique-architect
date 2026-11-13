"""Single-flight TTL cache for expensive lookups (Python 3.10+).

Concurrent callers that ask for the same missing key share one loader
call. Entries expire `ttl` seconds after they are stored, and the least
recently used entry is evicted once `maxsize` is exceeded.

Thread-safe.
"""
import threading
import time
from collections import OrderedDict
from collections.abc import Callable, Hashable
from typing import Generic, TypeVar

K = TypeVar("K", bound=Hashable)
V = TypeVar("V")


class SingleFlightCache(Generic[K, V]):
    def __init__(self, maxsize: int = 1024, ttl: float = 30.0) -> None:
        if maxsize <= 0 or ttl <= 0:
            raise ValueError("maxsize and ttl must be positive")
        self._maxsize = maxsize
        self._ttl = ttl
        self._data: OrderedDict[K, tuple[V, float]] = OrderedDict()
        self._inflight: dict[K, threading.Event] = {}
        self._lock = threading.Lock()
        self.hits = 0
        self.misses = 0
        self.failures = 0

    def get(self, key: K, loader: Callable[[K], V]) -> V:
        now = time.monotonic()

        # Fast path without the lock: dict reads are atomic under the GIL.
        entry = self._data.get(key)
        if entry is not None and entry[1] > now:
            self._data.move_to_end(key)
            self.hits += 1
            return entry[0]

        with self._lock:
            entry = self._data.get(key)
            if entry is not None and entry[1] > now:
                self._data.move_to_end(key)
                self.hits += 1
                return entry[0]
            self.misses += 1
            waiter = self._inflight.get(key)
            if waiter is None:
                waiter = self._inflight[key] = threading.Event()
                owner = True
            else:
                owner = False

        if not owner:
            waiter.wait()
            return self._data[key][0]

        try:
            value = loader(key)
        except Exception:
            self.failures += 1
            raise

        with self._lock:
            self._data[key] = (value, now + self._ttl)
            self._data.move_to_end(key)
            while len(self._data) > self._maxsize:
                self._data.popitem()
            del self._inflight[key]
        waiter.set()
        return value

    def invalidate(self, key: K) -> None:
        """Drop `key` so the next get() calls the loader again."""
        with self._lock:
            self._data.pop(key, None)

    def __len__(self) -> int:
        with self._lock:
            return len(self._data)
