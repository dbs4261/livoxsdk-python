import ctypes

import livoxsdk
from livoxsdk.structs.structure_type import StructureType


class HeartbeatResponsePayload(StructureType):

    ret_code: ctypes.c_uint8
    error_union: livoxsdk.structs.status.StatusUnion

    @property
    def state(self) -> livoxsdk.enums.devices.DeviceState:
        raise NotImplementedError

    @state.setter
    def state(self, val: livoxsdk.enums.devices.DeviceState) -> None:
        raise NotImplementedError

    @property
    def feature(self) -> livoxsdk.enums.devices.LidarFeature:
        raise NotImplementedError

    @feature.setter
    def feature(self, val: livoxsdk.enums.devices.LidarFeature) -> None:
        raise NotImplementedError
