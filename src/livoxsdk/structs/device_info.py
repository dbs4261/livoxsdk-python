import ctypes
import typing

import livoxsdk
from livoxsdk.structs.structure_type import StructureType
from livoxsdk.structs.status import StatusUnion


class DeviceInfo(StructureType):
    _pack_ = 1
    _mapped_ = (
        ("state_c", "state"),
        ("feature_c", "feature"),
    )
    _fields_ = [
        ("broadcast_code", livoxsdk.BroadcastCode),
        ("handle", ctypes.c_uint8),
        ("slot", ctypes.c_uint8),
        ("id", ctypes.c_uint8),
        ("type", ctypes.c_uint8),
        ("data_port", ctypes.c_uint16),
        ("cmd_port", ctypes.c_uint16),
        ("sensor_port", ctypes.c_uint16),
        ("ip", ctypes.c_char * 16),
        ("state_c", ctypes.c_uint32),
        ("feature_c", ctypes.c_uint32),
        ("status", StatusUnion),
        ("firmware_version", ctypes.c_uint8 * 4)
    ]

    @property
    def state(self) -> livoxsdk.enums.DeviceState:
        return livoxsdk.enums.DeviceState(getattr(self, "state_c"))

    @state.setter
    def state(self, val: typing.Union[livoxsdk.enums.DeviceState, livoxsdk.enums.LidarMode]) -> None:
        setattr(self, "state_c", val.value)

    @property
    def feature(self) -> livoxsdk.enums.LidarFeature:
        return livoxsdk.enums.LidarFeature(getattr(self, "feature_c"))

    @feature.setter
    def feature(self, val: livoxsdk.enums.LidarFeature) -> None:
        setattr(self, "feature_c", val.value)
