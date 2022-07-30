import ctypes
import sys
import typing

from livoxsdk.structs.structure_type import StructureType


class ReturnTagBitfield(StructureType):
    _pack_ = 1
    _mapped_ = (
        # ("reserved", None)
    )
    _fields_ = [
        ("spatial_noise", ctypes.c_uint8, 2),
        ("intensity_noise", ctypes.c_uint8, 2),
        ("return_number", ctypes.c_uint8, 2),
        ("reserved", ctypes.c_uint8, 2),
    ]

    def __repr__(self):
        return super().__str__() + " ({:08b})".format(int.from_bytes(bytes(self), byteorder=sys.byteorder))

    def is_noise(self) -> bool:
        return getattr(self, "spatial_noise") != 0 or getattr(self, "intensity_noise") != 0


class _ReturnTagUnion(ctypes.Union):
    _pack_ = 1
    _fields_ = (
        ("bitfield", ReturnTagBitfield),
        ("raw", ctypes.c_uint8),
    )


_ExtendedPoint = typing.TypeVar("_ExtendedPoint", bound=StructureType)


def _add_return_tag_bitfield(cls: _ExtendedPoint) -> _ExtendedPoint:
    if hasattr(cls, "tag"):
        def get_bitfield(self) -> ReturnTagBitfield:
            return ReturnTagBitfield.from_buffer(memoryview(self), getattr(getattr(cls, "tag"), "offset"))
        def set_bitfield(self, val: ReturnTagBitfield) -> None:
            setattr(self, "tag", ctypes.c_uint8.from_buffer(memoryview(val)))
        setattr(cls, "tag_bitfield", property(get_bitfield, set_bitfield, None, None))
        return cls
    else:
        i = 0
        while hasattr(cls, f"tag{i}"):
            def get_bitfield(self) -> ReturnTagBitfield:
                return ReturnTagBitfield.from_buffer(memoryview(self), getattr(getattr(cls, f"tag{i}"), "offset"))
            def set_bitfield(self, val: ReturnTagBitfield) -> None:
                setattr(self, f"tag{i}", ctypes.c_uint8.from_buffer(memoryview(val)))
            setattr(cls, f"tag{i}_bitfield", property(get_bitfield, set_bitfield, None, None))
        return cls
