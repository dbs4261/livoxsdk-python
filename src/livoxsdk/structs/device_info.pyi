import ctypes
import typing

import livoxsdk
from livoxsdk.structs.structure_type import StructureType
from livoxsdk.structs.status import StatusUnion


class DeviceInfo(StructureType):
    broadcast_code: livoxsdk.BroadcastCode
    handle: ctypes.c_uint8
    slot: ctypes.c_uint8
    id: ctypes.c_uint8
    type: ctypes.c_uint8
    data_port: livoxsdk.Port
    cmd_port: livoxsdk.Port
    sensor_port: livoxsdk.Port
    ip: ctypes.c_char * 16
    status: StatusUnion
    firmware_version: livoxsdk.FirmwareVersion

    @property
    def state(self) -> livoxsdk.enums.LidarState:
        raise NotImplementedError

    @state.setter
    def state(self, val: typing.Union[livoxsdk.enums.LidarState, livoxsdk.enums.LidarMode]) -> None:
        raise NotImplementedError

    @property
    def feature(self) -> livoxsdk.enums.LidarFeature:
        raise NotImplementedError

    @feature.setter
    def feature(self, val: livoxsdk.enums.LidarFeature) -> None:
        raise NotImplementedError
