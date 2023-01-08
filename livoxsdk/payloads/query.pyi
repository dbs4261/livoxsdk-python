import ctypes
import typing

from livoxsdk.structs.structure_type import StructureType


class FirmwareVersion(StructureType):
    major: typing.Annotated[int, ctypes.c_uint8]
    minor: typing.Annotated[int, ctypes.c_uint8]
    revision: typing.Annotated[int, ctypes.c_uint8]
    build: typing.Annotated[int, ctypes.c_uint8]

    @property
    def patch(self) -> ctypes.c_uint16: ...

    def __str__(self):
        """
        :return: "major.minor.revision.build"
        """
        pass


class QueryResponsePayload(StructureType):
    ret_code: typing.Annotated[int, ctypes.c_uint8]
    firmware_version: FirmwareVersion
