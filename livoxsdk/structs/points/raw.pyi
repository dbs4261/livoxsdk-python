import ctypes
import typing

from livoxsdk.structs.structure_type import StructureType
from livoxsdk.structs.points.return_iterator import ReturnIterator


class RawPoint(StructureType):
    x: typing.Annotated[int, ctypes.c_int32]
    y: typing.Annotated[int, ctypes.c_int32]
    z: typing.Annotated[int, ctypes.c_int32]
    reflectivity: typing.Annotated[int, ctypes.c_uint8]

    def __iter__(self) -> ReturnIterator: ...


Point: typing.TypeAlias = RawPoint
CartesianPoint: typing.TypeAlias = RawPoint


class SpherPoint(StructureType):
    depth: typing.Annotated[int, ctypes.c_uint32]
    theta: typing.Annotated[int, ctypes.c_uint16]
    phi: typing.Annotated[int, ctypes.c_uint16]
    reflectivity: typing.Annotated[int, ctypes.c_uint8]

    def __iter__(self) -> ReturnIterator: ...


SphericalPoint: typing.TypeAlias = SpherPoint
