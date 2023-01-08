__version__ = "0.0.1"

import typing
import ctypes

endianness: typing.Literal["little", "big"] = "little"
Port: typing.Annotated[typing.Type["Port"], ctypes.c_uint16] = typing.NewType("Port", int)
scan_port: typing.Final[Port] = Port(55000)
data_transmit_port: typing.Final[Port] = Port(65000)
control_receive_port: typing.Final[Port] = Port(65000)
_default_command_port: typing.Final[Port] = Port(55001)
_default_data_port: typing.Final[Port] = Port(65001)
_default_sensor_port: typing.Final[Port] = Port(60001)

from . import logging_helpers
from . import errors
from . import crc
from . import enums
from . import utilities
from .utilities import annotations
from .binary_serializable import BinarySerializable, BinaryMappable
from .atomic_counter import AtomicCounter
from . import structs
from .structs import BroadcastCode, ControlPacketHeader, DataPacketHeader, DataPacket
from . import payloads
from .payloads import FirmwareVersion
from .port_scanner import scan_for_devices
from .broadcast_protocol import BroadcastProtocol
from .command_protocol import CommandProtocol
from .data_protocol import DataProtocol
from .sensor_protocol import SensorProtocol
from .device import Device
from .lidar import Lidar
# from .context import Context
# from .commander import Commander
# from .port_scanner import NoDevicesDetectedError, scan_for_devices, DeviceConnectionInfo
