import threading
import typing


class AtomicCounter:
    def __init__(self, value: int = 0, max_val: typing.Optional[int] = None):
        self._value = int(value)
        self._max_val = max_val
        self._lock = threading.Lock()

    def postinc(self, d=1):
        with self._lock:
            out = self._value
            self._value = (self._value + int(d)) % self._max_val
            return out

    def postdec(self, d=1):
        return self.postinc(-d)

    @property
    def value(self) -> int:
        with self._lock:
            return self._value

    @value.setter
    def value(self, v) -> int:
        with self._lock:
            self._value = int(v)
            return self._value