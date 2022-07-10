import ctypes
import typing

endianness: typing.Literal["little", "big"] = "little"
Port = typing.NewType("Port", int)
scan_port: typing.Final[Port] = Port(55000)
control_port: typing.Final[Port] = Port(65000)

BroadcastCode: typing.TypeAlias = ctypes.c_char * 16
BroadcastCodeSize: typing.Final[int] = ctypes.sizeof(BroadcastCode)

from . import logging_helpers
from . import crc
from . import enums
from .binary_serializable import BinarySerializable, BinaryMappable
from . import structs
from . import port_scanner
