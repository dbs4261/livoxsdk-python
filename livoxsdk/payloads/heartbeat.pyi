import ctypes

import livoxsdk
from livoxsdk.structs.structure_type import StructureType


class HeartbeatResponsePayload(StructureType):

    ret_code: ctypes.c_uint8
    error_union: livoxsdk.structs.status.StatusUnion

    @property
    def state(self) -> livoxsdk.enums.devices.LidarState: ...

    @state.setter
    def state(self, val: livoxsdk.enums.devices.LidarState) -> None: ...

    @property
    def feature(self) -> livoxsdk.enums.devices.LidarFeature: ...

    @feature.setter
    def feature(self, val: livoxsdk.enums.devices.LidarFeature) -> None: ...
