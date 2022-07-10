import ctypes

import livoxsdk
from livoxsdk.structs.structure_type import StructureType


class HeartbeatResponsePayload(StructureType):
    _pack_ = 1
    _fields_ = (
        ("ret_code", ctypes.c_uint8),
        ("state_c", ctypes.c_uint8),
        ("feature_c", ctypes.c_uint8),
        ("error_union", livoxsdk.structs.status.StatusUnion),
    )

    @property
    def state(self) -> livoxsdk.enums.devices.DeviceState:
        return livoxsdk.enums.devices.DeviceState(getattr(self, "state_c"))

    @state.setter
    def state(self, val: livoxsdk.enums.devices.DeviceState) -> None:
        setattr(self, "state_c", ctypes.c_uint8(val.value))

    @property
    def feature(self) -> livoxsdk.enums.devices.LidarFeature:
        return livoxsdk.enums.devices.LidarFeature(getattr(self, "feature_c"))

    @feature.setter
    def feature(self, val: livoxsdk.enums.devices.LidarFeature) -> None:
        setattr(self, "state_c", ctypes.c_uint8(val.value))
