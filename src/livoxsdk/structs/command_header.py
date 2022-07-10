import ctypes
import typing

import livoxsdk
from livoxsdk.structs.structure_type import StructureType


class CommandHeader(StructureType):
    _pack_ = 1
    _mapped_ = (
        ("command_set_c", None),
        ("command_type_c", "command_type"),
    )
    _fields_ = [
        ("command_set_c", ctypes.c_uint8),
        ("command_type_c", ctypes.c_uint8),
    ]

    @property
    def command_set(self) -> livoxsdk.enums.CommandSet:
        return livoxsdk.enums.CommandSet(getattr(self, "command_set_c"))

    @property
    def command_type(self) -> livoxsdk.enums.CommandId:
        if self.command_set == livoxsdk.enums.CommandSet.General:
            return livoxsdk.enums.GeneralCommandId(getattr(self, "command_type_c"))
        elif self.command_set == livoxsdk.enums.CommandSet.Lidar:
            return livoxsdk.enums.LidarCommandId(getattr(self, "command_type_c"))
        elif self.command_set == livoxsdk.enums.CommandSet.Hub:
            return livoxsdk.enums.HubCommandId(getattr(self, "command_type_c"))
        raise TypeError("Unknown command type for command set {}".format(self.command_set))

    @command_type.setter
    def command_type(self, val: livoxsdk.enums.CommandId) -> None:
        command_set: typing.Optional[livoxsdk.enums.CommandSet] = None
        if isinstance(val, livoxsdk.enums.GeneralCommandId):
            command_set = livoxsdk.enums.CommandSet.General
        elif isinstance(val, livoxsdk.enums.LidarCommandId):
            command_set = livoxsdk.enums.CommandSet.Lidar
        elif isinstance(val, livoxsdk.enums.HubCommandId):
            command_set = livoxsdk.enums.CommandSet.Hub
        if command_set is None:
            raise ValueError
        setattr(self, "command_set_c", ctypes.c_uint8(command_set))
        setattr(self, "command_type_c", ctypes.c_uint8(val))
