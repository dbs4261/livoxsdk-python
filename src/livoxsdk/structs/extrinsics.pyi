import ctypes

from livoxsdk.structs.structure_type import StructureType


class Extrinsics(StructureType):
    roll: float = 0.0
    pitch: float = 0.0
    yaw: float = 0.0

    @property
    def x(self) -> float: ...

    @x.setter
    def x(self, v: float) -> None: ...

    @property
    def y(self) -> float: ...

    @y.setter
    def y(self, v: float) -> None: ...

    @property
    def z(self) -> float: ...

    @z.setter
    def z(self, v: float) -> None: ...
