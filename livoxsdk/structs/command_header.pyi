import livoxsdk
from livoxsdk.structs.structure_type import StructureType


class CommandHeader(StructureType):
    @property
    def command_set(self) -> livoxsdk.enums.CommandSet: ...

    @property
    def command_type(self) -> livoxsdk.enums.CommandId: ...

    @command_type.setter
    def command_type(self, val: livoxsdk.enums.CommandId) -> None: ...
