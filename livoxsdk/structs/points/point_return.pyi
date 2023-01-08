import dataclasses
import typing

from livoxsdk.structs.points.return_tag import ReturnTagBitfield


@dataclasses.dataclass
class CartesianReturn:
    x: int
    y: int
    z: int
    reflectivity: int
    tag: ReturnTagBitfield

    def nonzero(self) -> bool: ...

    def valid(self) -> bool: ...


@dataclasses.dataclass
class SphericalReturn:
    theta: int
    phi: int
    depth: int
    reflectivity: int
    tag: ReturnTagBitfield

    def nonzero(self) -> bool: ...

    def valid(self): ...


ReturnUnion = typing.Union[CartesianReturn, SphericalReturn]
