import ctypes
import typing

from livoxsdk.structs.structure_type import StructureType
from livoxsdk.structs.points.return_iterator import ReturnIterator


class RawPoint(StructureType):
    x: ctypes.c_int32
    y: ctypes.c_int32
    z: ctypes.c_int32
    reflectivity: ctypes.c_uint8

    def __iter__(self) -> ReturnIterator:
        raise NotImplementedError


Point: typing.TypeAlias = RawPoint
CartesianPoint: typing.TypeAlias = RawPoint


class SpherPoint(StructureType):
    depth: ctypes.c_uint32
    theta: ctypes.c_uint16
    phi: ctypes.c_uint16
    reflectivity: ctypes.c_uint8

    def __iter__(self) -> ReturnIterator:
        raise NotImplementedError


SphericalPoint: typing.TypeAlias = SpherPoint
