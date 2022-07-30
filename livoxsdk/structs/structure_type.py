import ctypes
import typing

import livoxsdk

BaseStructureType: typing.Type[typing.Union[ctypes.Structure, livoxsdk.BinarySerializable, typing.SupportsBytes]] =\
    ctypes.LittleEndianStructure if livoxsdk.endianness == "little" else ctypes.BigEndianStructure


class StructureType(BaseStructureType):
    def __init__(self, **kwargs):
        if hasattr(self, "_defaults_"):
            values = self.__getattribute__("_defaults_").copy()
        else:
            values = {}
        values.update(kwargs)
        super().__init__(**values)

    def __str__(self):
        field_replacements = {a: b for a, b in getattr(type(self), "_mapped_", ())}
        fields = [f[0] for f in getattr(type(self), "_fields_")]
        fields = [field_replacements[f] if f in field_replacements else f for f in fields]
        fields = [f for f in fields if f is not None]
        return "{} {{{}}}".format(type(self).__name__, ", ".join(
            "{}: {}".format(f, str(getattr(self, f))) for f in fields))

    def __eq__(self, other) -> bool:
        if not isinstance(other, type(self)):
            return False
        return all(getattr(self, f[0]) == getattr(other, f[0])
                   for f in getattr(type(self), "_fields_"))
