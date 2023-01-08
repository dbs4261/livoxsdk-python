import ctypes
import typing

import livoxsdk
from livoxsdk.structs.structure_type import StructureType
from livoxsdk.structs.status import StatusUnion


class DeviceInfo(StructureType):
    broadcast_code: livoxsdk.BroadcastCode
    handle: typing.Annotated[int, ctypes.c_uint8]
    slot: typing.Annotated[int, ctypes.c_uint8]
    id: typing.Annotated[int, ctypes.c_uint8]
    type: typing.Annotated[int, ctypes.c_uint8]
    data_port: typing.Annotated[livoxsdk.Port, ctypes.c_uint16]
    cmd_port: typing.Annotated[livoxsdk.Port, ctypes.c_uint16]
    sensor_port: typing.Annotated[livoxsdk.Port, ctypes.c_uint16]
    ip: typing.Annotated[int, ctypes.c_char * 16]
    status: StatusUnion
    firmware_version: livoxsdk.FirmwareVersion

    @property
    def state(self) -> livoxsdk.enums.LidarState: ...

    @state.setter
    def state(self, val: typing.Union[livoxsdk.enums.LidarState, livoxsdk.enums.LidarMode]) -> None: ...

    @property
    def feature(self) -> livoxsdk.enums.LidarFeature: ...

    @feature.setter
    def feature(self, val: livoxsdk.enums.LidarFeature) -> None: ...
