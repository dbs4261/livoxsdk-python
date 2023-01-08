import ctypes
import typing

import livoxsdk
from livoxsdk.structs.structure_type import StructureType
from livoxsdk.structs.status import StatusUnion
from livoxsdk.structs.broadcast_code import BroadcastCode


class DeviceInfo(StructureType):
    _pack_ = 1
    _mapped_ = (
        ("type_c", "type"),
        ("state_c", "state"),
        ("feature_c", "feature"),
    )
    _fields_ = [
        ("broadcast_code", BroadcastCode),
        ("handle", ctypes.c_uint8),
        ("slot", ctypes.c_uint8),
        ("id", ctypes.c_uint8),
        ("type_c", ctypes.c_uint8),
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
    def device_type(self) -> livoxsdk.enums.devices.DeviceType:
        return livoxsdk.enums.devices.DeviceType(getattr(self, "type_c"))

    @device_type.setter
    def device_type(self, val: livoxsdk.enums.devices.DeviceType) -> None:
        setattr(self, "type_c", ctypes.c_uint8(val.value))

    @property
    def state(self) -> livoxsdk.enums.LidarState:
        return livoxsdk.enums.LidarState(getattr(self, "state_c"))

    @state.setter
    def state(self, val: typing.Union[livoxsdk.enums.LidarState, livoxsdk.enums.LidarMode]) -> None:
        setattr(self, "state_c", val.value)

    @property
    def feature(self) -> livoxsdk.enums.LidarFeature:
        return livoxsdk.enums.LidarFeature(getattr(self, "feature_c"))

    @feature.setter
    def feature(self, val: livoxsdk.enums.LidarFeature) -> None:
        setattr(self, "feature_c", val.value)
