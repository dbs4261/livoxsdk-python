import ctypes

import livoxsdk
from livoxsdk.structs.structure_type import StructureType


class PointReturnModeResponsePayload(StructureType):
    _pack_ = 1
    _mapped_ = (
        ("point_cloud_return_mode_c", "point_cloud_return_mode"),
    )
    _fields_ = (
        ("ret_code", ctypes.c_uint8),
        ("point_cloud_return_mode_c", ctypes.c_uint8),
    )

    @property
    def point_cloud_return_mode(self) -> livoxsdk.enums.PointCloudReturnMode:
        return livoxsdk.enums.PointCloudReturnMode(getattr(self, "point_cloud_return_mode_c"))

    @point_cloud_return_mode.setter
    def point_cloud_return_mode(self, mode: livoxsdk.enums.PointCloudReturnMode) -> None:
        setattr(self, "point_cloud_return_mode", ctypes.c_uint8(mode.value))
