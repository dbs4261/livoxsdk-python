import ctypes

from livoxsdk.structs.structure_type import StructureType


class FirmwareVersion(StructureType):
    major: ctypes.c_uint8
    minor: ctypes.c_uint8
    revision: ctypes.c_uint8
    build: ctypes.c_uint8

    @property
    def patch(self) -> ctypes.c_uint16:
        raise NotImplementedError

    def __str__(self):
        """
        :return: "major.minor.revision.build"
        """
        raise NotImplementedError


class QueryResponsePayload(StructureType):
    ret_code: ctypes.c_uint8
    firmware_version: FirmwareVersion
