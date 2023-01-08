import ctypes
import typing

from livoxsdk.structs.structure_type import StructureType
from livoxsdk.structs.points.return_tag import ReturnTagBitfield
from livoxsdk.structs.points.return_iterator import ReturnIterator


class ExtendRawPoint(StructureType):
    x: typing.Annotated[int, ctypes.c_int32]
    y: typing.Annotated[int, ctypes.c_int32]
    z: typing.Annotated[int, ctypes.c_int32]
    reflectivity: typing.Annotated[int, ctypes.c_uint8]
    tag: typing.Annotated[int, ctypes.c_uint8]
    tag_bitfield: ReturnTagBitfield

    def __iter__(self) -> ReturnIterator: ...


ExtendCartesianPoint: typing.TypeAlias = ExtendRawPoint
ExtendedRawPoint: typing.TypeAlias = ExtendRawPoint
ExtendedCartesianPoint: typing.TypeAlias = ExtendedRawPoint


class ExtendSpherPoint(StructureType):
    depth: typing.Annotated[int, ctypes.c_uint32]
    theta: typing.Annotated[int, ctypes.c_uint16]
    phi: typing.Annotated[int, ctypes.c_uint16]
    reflectivity: typing.Annotated[int, ctypes.c_uint8]
    tag: typing.Annotated[int, ctypes.c_uint8]
    tag_bitfield: ReturnTagBitfield

    def __iter__(self) -> ReturnIterator: ...


ExtendSphericalPoint: typing.TypeAlias = ExtendSpherPoint
ExtendedSpherPoint: typing.TypeAlias = ExtendSpherPoint
ExtendedSphericalPoint: typing.TypeAlias = ExtendSpherPoint
