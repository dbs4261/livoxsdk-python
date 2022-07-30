import ctypes

from livoxsdk.structs.structure_type import StructureType


class Extrinsics(StructureType):
    _mapped_ = (
        ("x_c", "x"),
        ("y_c", "y"),
        ("z_c", "z")
    )
    _fields_ = (
        ("x_c", ctypes.c_int32),
        ("y_c", ctypes.c_int32),
        ("z_c", ctypes.c_int32),
        ("roll", ctypes.c_float),
        ("pitch", ctypes.c_float),
        ("yaw", ctypes.c_float),
    )
    _defaults_ = {
        "x": 0,
        "y": 0,
        "z": 0,
        "roll": 0.0,
        "pitch": 0.0,
        "yaw": 0.0,
    }

    @property
    def x(self) -> float:
        return getattr(self, "x_c") / 1000.0

    @x.setter
    def x(self, v: float) -> None:
        setattr(self, "x_c", int(v * 1000))

    @property
    def y(self) -> float:
        return getattr(self, "y_c") / 1000.0

    @y.setter
    def y(self, v: float) -> None:
        setattr(self, "y_c", int(v * 1000))

    @property
    def z(self) -> float:
        return getattr(self, "z_c") / 1000.0

    @z.setter
    def z(self, v: float) -> None:
        setattr(self, "z_c", int(v * 1000))
