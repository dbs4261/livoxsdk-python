import ctypes
import typing

endianness: typing.Literal["little", "big"] = "little"
Port = typing.NewType("Port", int)
scan_port: typing.Final[Port] = Port(55000)
control_port: typing.Final[Port] = Port(65000)

BroadcastCode: typing.TypeAlias = ctypes.c_char * 16
BroadcastCodeSize: typing.Final[int] = ctypes.sizeof(BroadcastCode)

from . import logging_helpers
from . import errors
from . import crc
from . import enums
from . import utilities
from .binary_serializable import BinarySerializable, BinaryMappable
from . import structs
from .structs import BroadcastCode
from . import payloads
from .payloads import FirmwareVersion
from . import port_scanner
from .command_protocol import CommandProtocol
from .data_protocol import DataProtocol
from .sensor_protocol import SensorProtocol
from .device import Device
# from .context import Context
# from .commander import Commander
# from .port_scanner import NoDevicesDetectedError, scan_for_devices, DeviceConnectionInfo
