import livoxsdk
from livoxsdk.structs.structure_type import StructureType


class CommandHeader(StructureType):
    @property
    def command_set(self) -> livoxsdk.enums.CommandSet:
        raise NotImplementedError

    @property
    def command_type(self) -> livoxsdk.enums.CommandId:
        raise NotImplementedError

    @command_type.setter
    def command_type(self, val: livoxsdk.enums.CommandId) -> None:
        raise NotImplementedError
