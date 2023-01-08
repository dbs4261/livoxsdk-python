import typing

import livoxsdk
from livoxsdk.structs.structure_type import StructureType


_point_structs: typing.List[typing.Type[StructureType]] = [
    livoxsdk.structs.points.RawPoint,
    livoxsdk.structs.points.SpherPoint,
    livoxsdk.structs.points.ExtendRawPoint,
    livoxsdk.structs.points.ExtendSpherPoint,
    livoxsdk.structs.points.DualExtendRawPoint,
    livoxsdk.structs.points.DualExtendSpherPoint,
    livoxsdk.structs.points.TripleExtendRawPoint,
    livoxsdk.structs.points.TripleExtendSpherPoint,
    livoxsdk.structs.points.ImuPoint,
]

PointUnionType = typing.Union[
    typing.Type[livoxsdk.structs.points.RawPoint],
    typing.Type[livoxsdk.structs.points.SpherPoint],
    typing.Type[livoxsdk.structs.points.ExtendRawPoint],
    typing.Type[livoxsdk.structs.points.ExtendSpherPoint],
    typing.Type[livoxsdk.structs.points.DualExtendRawPoint],
    typing.Type[livoxsdk.structs.points.DualExtendSpherPoint],
    typing.Type[livoxsdk.structs.points.TripleExtendRawPoint],
    typing.Type[livoxsdk.structs.points.TripleExtendSpherPoint],
    typing.Type[livoxsdk.structs.points.ImuPoint],
]


PointUnionListType = typing.Union[tuple(typing.List[t] for t in PointUnionType.__args__)]

def point_type_from_enum(val: livoxsdk.enums.PointDataType) -> typing.Type[PointUnionType]: ...

def point_enum_from_type(t: typing.Type[PointUnionType]) -> livoxsdk.enums.PointDataType: ...

def point_enum_from_point(point: PointUnionType) -> livoxsdk.enums.PointDataType: ...
