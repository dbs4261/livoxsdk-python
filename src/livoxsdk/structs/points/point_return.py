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

    def nonzero(self) -> bool:
        return not (self.x == 0 and self.y == 0 and self.z == 0)

    def valid(self) -> bool:
        return self.nonzero() and self.x > 0 and not self.tag.is_noise()


@dataclasses.dataclass
class SphericalReturn:
    theta: int
    phi: int
    depth: int
    reflectivity: int
    tag: ReturnTagBitfield

    def nonzero(self) -> bool:
        return self.depth != 0

    def valid(self):
        return self.depth > 0 and not self.tag.is_noise()


ReturnUnion = typing.Union[CartesianReturn, SphericalReturn]
