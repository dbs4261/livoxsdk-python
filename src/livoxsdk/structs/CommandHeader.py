import ctypes

import livoxsdk.enums.messages

if __name__ == "__main__":
    from livoxsdk.structs import StructureType
else:
    from .StructureType import StructureType


class CommandHeader(StructureType):
    _pack_ = 1
    _mapped_ = (
        ("command_set_c", "command_set"),
        ("command_type_c", "command_type"),
    )
    _fields_ = [
        ("command_set_c", ctypes.c_uint8),  # livoxsdk.enums.messages.CommandSet
        ("command_type_c", ctypes.c_uint8),  # livoxsdk.enums.messages.CommandId
    ]

    @property
    def command_set(self) -> livoxsdk.enums.messages.CommandSet:
        return livoxsdk.enums.messages.CommandSet(getattr(self, "command_set_c"))

    @command_set.setter
    def command_set(self, val: livoxsdk.enums.messages.CommandSet) -> None:
        setattr(self, "command_set_c", ctypes.c_uint8(val))

    @property
    def command_type(self) -> livoxsdk.enums.messages.CommandId:
        if self.command_set == livoxsdk.enums.messages.CommandSet.General:
            return livoxsdk.enums.messages.GeneralCommandId(getattr(self, "command_type_c"))
        elif self.command_set == livoxsdk.enums.messages.CommandSet.Lidar:
            return livoxsdk.enums.messages.LidarCommandId(getattr(self, "command_type_c"))
        elif self.command_set == livoxsdk.enums.messages.CommandSet.Hub:
            return livoxsdk.enums.messages.HubCommandId(getattr(self, "command_type_c"))
        raise TypeError("Unknown command type for command set {}".format(self.command_set))

    @command_type.setter
    def command_type(self, val: livoxsdk.enums.messages.CommandId) -> None:
        if isinstance(val, livoxsdk.enums.messages.GeneralCommandId):
            self.command_set = livoxsdk.enums.messages.CommandSet.General
        elif isinstance(val, livoxsdk.enums.messages.LidarCommandId):
            self.command_set = livoxsdk.enums.messages.CommandSet.Lidar
        elif isinstance(val, livoxsdk.enums.messages.HubCommandId):
            self.command_set = livoxsdk.enums.messages.CommandSet.Hub
        setattr(self, "command_type_c", ctypes.c_uint8(val))
