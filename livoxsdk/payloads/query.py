import ctypes

from livoxsdk.structs.structure_type import StructureType


class FirmwareVersion(StructureType):
    _pack_ = 1
    _fields_ = (
        ("major", ctypes.c_uint8),
        ("minor", ctypes.c_uint8),
        ("revision", ctypes.c_uint8),
        ("build", ctypes.c_uint8),
    )

    @property
    def patch(self) -> ctypes.c_uint16:
        return ctypes.c_uint16(getattr(self, "revision").value << 8 + getattr(self, "build"))

    def __str__(self):
        return ".".join(str(getattr(self, v)) for v in ["major", "minor", "revision", "build"])


class QueryResponsePayload(StructureType):
    _pack_ = 1
    _fields_ = (
        ("ret_code", ctypes.c_uint8),
        ("firmware_version", FirmwareVersion),
    )
