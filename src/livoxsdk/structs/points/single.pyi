import ctypes
import typing

from livoxsdk.structs.structure_type import StructureType
from livoxsdk.structs.points.return_tag import ReturnTagBitfield
from livoxsdk.structs.points.return_iterator import ReturnIterator


class ExtendRawPoint(StructureType):
    x: ctypes.c_int32
    y: ctypes.c_int32
    z: ctypes.c_int32
    reflectivity: ctypes.c_uint8
    tag: ctypes.c_uint8
    tag_bitfield: ReturnTagBitfield

    def __iter__(self) -> ReturnIterator:
        return ReturnIterator(self, 1, True)


ExtendCartesianPoint: typing.TypeAlias = ExtendRawPoint
ExtendedRawPoint: typing.TypeAlias = ExtendRawPoint
ExtendedCartesianPoint: typing.TypeAlias = ExtendedRawPoint


class ExtendSpherPoint(StructureType):
    depth: ctypes.c_uint32
    theta: ctypes.c_uint16
    phi: ctypes.c_uint16
    reflectivity: ctypes.c_uint8
    tag: ctypes.c_uint8
    tag_bitfield: ReturnTagBitfield

    def __iter__(self) -> ReturnIterator:
        return ReturnIterator(self, 1, False)


ExtendSphericalPoint: typing.TypeAlias = ExtendSpherPoint
ExtendedSpherPoint: typing.TypeAlias = ExtendSpherPoint
ExtendedSphericalPoint: typing.TypeAlias = ExtendSpherPoint
