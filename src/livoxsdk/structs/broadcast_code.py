import ctypes
import typing

from livoxsdk.structs.structure_type import StructureType


serial_number_length: typing.Final[int] = 14


class BroadcastCode(StructureType):
    _pack_ = 1
    _mapped_ = (
        ("serial_c", "serial"),
        ("range_code_c", "range_code"),
        ("_null", None),
    )
    _fields_ = (
        ("serial_c", ctypes.c_char * serial_number_length),
        ("range_code_c", ctypes.c_char),
        ("_null", ctypes.c_char),
    )

    @property
    def serial(self) -> str:
        return getattr(self, "serial_c").decode("ascii")

    @serial.setter
    def serial(self, val: str) -> None:
        setattr(self, "serial_c", val.encode("ascii"))

    @property
    def range_code(self) -> int:
        return int(getattr(self, "range_code_c").decode("ascii"))

    @range_code.setter
    def range_code(self, val: int):
        if val not in [1, 2, 3]:
            raise ValueError("Range code must be either 1, 2, or 3")
        setattr(self, "range_code_c", str(val).encode("ascii"))

    def valid(self) -> bool:
        return getattr(self, "_null").decode("ascii") == chr(0)