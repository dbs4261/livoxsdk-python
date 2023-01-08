import ctypes
import typing

import livoxsdk
from livoxsdk.structs.structure_type import StructureType


class LidarErrorCode(StructureType):
    # Note: ctypes.sizeof(LidarErrorCode) == ctypes.sizeof(ctypes.c_uint32)
    temp_status: typing.Annotated[int, ctypes.c_int32, livoxsdk.annotations.BitField(2)]
    volt_status: typing.Annotated[int, ctypes.c_int32, livoxsdk.annotations.BitField(2)]
    motor_status: typing.Annotated[int, ctypes.c_int32, livoxsdk.annotations.BitField(2)]
    dirty_warn: typing.Annotated[int, ctypes.c_int32, livoxsdk.annotations.BitField(2)]
    firmware_err: typing.Annotated[int, ctypes.c_int32, livoxsdk.annotations.BitField(1)]
    pps_status: typing.Annotated[int, ctypes.c_int32, livoxsdk.annotations.BitField(1)]
    device_status: typing.Annotated[int, ctypes.c_int32, livoxsdk.annotations.BitField(1)]
    fan_status: typing.Annotated[int, ctypes.c_int32, livoxsdk.annotations.BitField(1)]
    self_heating: typing.Annotated[int, ctypes.c_int32, livoxsdk.annotations.BitField(1)]
    ptp_status: typing.Annotated[int, ctypes.c_int32, livoxsdk.annotations.BitField(1)]
    ...
    system_status: typing.Annotated[int, ctypes.c_int32, livoxsdk.annotations.BitField(2)]

    @property
    def time_sync_status(self) -> livoxsdk.enums.devices.TimeSync: ...

    @time_sync_status.setter
    def time_sync_status(self, val: livoxsdk.enums.devices.TimeSync) -> None: ...


class HubErrorCode(StructureType):
    ...
    temp_status: typing.Annotated[int, ctypes.c_uint32, livoxsdk.annotations.BitField(2)]
    lidar_status: typing.Annotated[int, ctypes.c_uint32, livoxsdk.annotations.BitField(1)]
    lidar_link_status: typing.Annotated[int, ctypes.c_uint32, livoxsdk.annotations.BitField(1)]
    firmware_err: typing.Annotated[int, ctypes.c_uint32, livoxsdk.annotations.BitField(1)]
    ...
    system_status: typing.Annotated[int, ctypes.c_uint32, livoxsdk.annotations.BitField(2)]

    @property
    def sync_status(self) -> livoxsdk.enums.devices.TimeSync: ...

    @sync_status.setter
    def sync_status(self, val: livoxsdk.enums.devices.TimeSync) -> None: ...

    @property
    def time_sync_status(self) -> livoxsdk.enums.devices.TimeSync: ...

    @time_sync_status.setter
    def time_sync_status(self, val: livoxsdk.enums.devices.TimeSync) -> None: ...


class ErrorMessage(ctypes.Union):
    error_code: typing.Annotated[int, ctypes.c_uint32]
    lidar_error_code: LidarErrorCode
    hub_error_code: HubErrorCode

    def typed_get(self, device_type: typing.Optional[livoxsdk.enums.devices.DeviceType] = None): ...


class StatusUnion(ctypes.Union):
    progress: typing.Annotated[int, ctypes.c_uint32]
    error_code: typing.Annotated[int, ctypes.c_uint32]
    lidar_error_code: LidarErrorCode
    hub_error_code: HubErrorCode

    def typed_get(self, device_type: typing.Union[
        None, typing.Literal["progress", "error_code"], livoxsdk.enums.devices.DeviceType] = None): ...
