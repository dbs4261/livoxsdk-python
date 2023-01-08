import ctypes
import typing

import livoxsdk
from livoxsdk.structs.structure_type import StructureType


class LidarErrorCode(StructureType):
    _pack_ = 1
    _mapped_ = (
        ("time_sync_status_c", "time_sync_status"),
        ("_rsvd", None),
    )
    _fields_ = (
        ("temp_status", ctypes.c_int32, 2),
        ("volt_status", ctypes.c_int32, 2),
        ("motor_status", ctypes.c_int32, 2),
        ("dirty_warn", ctypes.c_int32, 2),
        ("firmware_err", ctypes.c_int32, 1),
        ("pps_status", ctypes.c_int32, 1),
        ("device_status", ctypes.c_int32, 1),
        ("fan_status", ctypes.c_int32, 1),
        ("self_heating", ctypes.c_int32, 1),
        ("ptp_status", ctypes.c_int32, 1),
        ("time_sync_status_c", ctypes.c_int32, 3),
        ("_rsvd", ctypes.c_int32, 13),
        ("system_status", ctypes.c_int32, 2),
    )

    @property
    def time_sync_status(self) -> livoxsdk.enums.devices.TimeSync:
        return livoxsdk.enums.devices.TimeSync(getattr(self, "time_sync_status_c"))

    @time_sync_status.setter
    def time_sync_status(self, val: livoxsdk.enums.devices.TimeSync) -> None:
        setattr(self, "time_sync_status_c", val.value)


class HubErrorCode(StructureType):
    _pack_ = 1
    _mapped_ = (
        ("sync_status_c", "sync_status_c"),
        ("_rsvd", None),
    )
    _fields_ = (
        ("sync_status_c", ctypes.c_uint32, 2),
        ("temp_status", ctypes.c_uint32, 2),
        ("lidar_status", ctypes.c_uint32, 1),
        ("lidar_link_status", ctypes.c_uint32, 1),
        ("firmware_err", ctypes.c_uint32, 1),
        ("_rsvd", ctypes.c_uint32, 23),
        ("system_status", ctypes.c_uint32, 2)
    )

    @property
    def sync_status(self) -> livoxsdk.enums.devices.TimeSync:
        temp_val = livoxsdk.enums.devices.TimeSync(getattr(self, "sync_status_c"))
        if temp_val == livoxsdk.enums.devices.TimeSync.PPS:
            temp_val = livoxsdk.enums.devices.TimeSync.Abnormal
        return temp_val

    @sync_status.setter
    def sync_status(self, val: livoxsdk.enums.devices.TimeSync) -> None:
        if val == livoxsdk.enums.devices.TimeSync.PPS:
            raise ValueError("Livox Hubs do not support PPS synchronization")
        if val != livoxsdk.enums.devices.TimeSync.Abnormal:
            temp_val: int = val.value
        else:
            temp_val: int = livoxsdk.enums.devices.TimeSync.Abnormal.value
        setattr(self, "sync_status_c", temp_val)

    time_sync_status = sync_status


class ErrorMessage(ctypes.Union):
    _pack_ = 1
    _fields_ = (
        ("error_code", ctypes.c_uint32),
        ("lidar_error_code", LidarErrorCode),
        ("hub_error_code", HubErrorCode),
    )

    def typed_get(self, device_type: typing.Optional[livoxsdk.enums.devices.DeviceType] = None):
        if device_type not in livoxsdk.enums.devices.DeviceType._value2member_map_:
            return self.error_code
        elif device_type.is_hub():
            return self.hub_error_code
        else:
            return self.lidar_error_code

    def __str__(self) -> str:
        return "ErrorMessage {{error_code: {}}}".format(self.error_code)


class StatusUnion(ctypes.Union):
    _pack_ = 1
    _anonymous_ = (
        "status_code",
    )
    _fields_ = (
        ("progress", ctypes.c_uint32),
        ("status_code", ErrorMessage),
    )

    def typed_get(self, device_type: typing.Union[
        None, typing.Literal["progress", "error_code"], livoxsdk.enums.devices.DeviceType] = None):
        if device_type not in livoxsdk.enums.devices.DeviceType._value2member_map_:
            return self.error_code
        elif device_type.is_hub():
            return self.hub_error_code
        else:
            return self.lidar_error_code

    def __str__(self) -> str:
        return "StatusUnion {{error_code/progress: {}}}".format(self.error_code)
