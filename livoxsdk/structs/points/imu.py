import ctypes

from livoxsdk.structs.structure_type import StructureType


class ImuPoint(StructureType):
    _pack_ = 1
    _fields_ = [
        ("gyro_x", ctypes.c_float),
        ("gyro_y", ctypes.c_float),
        ("gyro_z", ctypes.c_float),
        ("acc_x", ctypes.c_float),
        ("acc_y", ctypes.c_float),
        ("acc_z", ctypes.c_float)
    ]
