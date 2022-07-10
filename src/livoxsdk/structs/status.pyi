import ctypes
import typing

import livoxsdk
from livoxsdk.structs.structure_type import StructureType


class LidarErrorCode(StructureType):
    temp_status: ctypes.c_int32
    volt_status: ctypes.c_int32
    motor_status: ctypes.c_int32
    dirty_warn: ctypes.c_int32
    firmware_err: ctypes.c_int32
    pps_status: ctypes.c_int32
    device_status: ctypes.c_int32
    fan_status: ctypes.c_int32
    self_heating: ctypes.c_int32
    ptp_status: ctypes.c_int32
    system_status: ctypes.c_int32

    @property
    def time_sync_status(self) -> livoxsdk.enums.devices.TimeSync:
        raise NotImplementedError

    @time_sync_status.setter
    def time_sync_status(self, val: livoxsdk.enums.devices.TimeSync) -> None:
        raise NotImplementedError


class HubErrorCode(StructureType):
    temp_status: ctypes.c_uint32
    lidar_status: ctypes.c_uint32
    lidar_link_status: ctypes.c_uint32
    firmware_err: ctypes.c_uint32
    system_status: ctypes.c_uint32

    @property
    def sync_status(self) -> livoxsdk.enums.devices.TimeSync:
        raise NotImplementedError

    @sync_status.setter
    def sync_status(self, val: livoxsdk.enums.devices.TimeSync) -> None:
        raise NotImplementedError

    @property
    def time_sync_status(self) -> livoxsdk.enums.devices.TimeSync:
        raise NotImplementedError

    @time_sync_status.setter
    def time_sync_status(self, val: livoxsdk.enums.devices.TimeSync) -> None:
        raise NotImplementedError


class ErrorMessage(ctypes.Union):
    error_code: ctypes.c_uint32
    lidar_error_code: LidarErrorCode
    hub_error_code: HubErrorCode

    def typed_get(self, device_type: typing.Optional[livoxsdk.enums.devices.DeviceType] = None):
        raise NotImplementedError


class StatusUnion(ctypes.Union):
    progress: ctypes.c_uint32
    error_code: ctypes.c_uint32
    lidar_error_code: LidarErrorCode
    hub_error_code: HubErrorCode
