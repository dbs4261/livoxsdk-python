import ctypes
import typing

from livoxsdk.structs.structure_type import StructureType
from livoxsdk.structs.points.return_iterator import ReturnIterator


class RawPoint(StructureType):
    _pack_ = 1
    _fields_ = [
        ("x", ctypes.c_int32),
        ("y", ctypes.c_int32),
        ("z", ctypes.c_int32),
        ("reflectivity", ctypes.c_uint8)
    ]

    def __iter__(self) -> ReturnIterator:
        return ReturnIterator(self, 1, True)


Point: typing.TypeAlias = RawPoint
CartesianPoint: typing.TypeAlias = RawPoint


class SpherPoint(StructureType):
    _pack_ = 1
    _fields_ = [
        ("depth", ctypes.c_uint32),
        ("theta", ctypes.c_uint16),
        ("phi", ctypes.c_uint16),
        ("reflectivity", ctypes.c_uint8)
    ]

    def __iter__(self) -> ReturnIterator:
        return ReturnIterator(self, 1, False)


SphericalPoint: typing.TypeAlias = SpherPoint
