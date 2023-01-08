import livoxsdk
from livoxsdk.structs.structure_type import StructureType


class PointReturnModeResponsePayload(StructureType):
    ret_code: int

    @property
    def point_cloud_return_mode(self) -> livoxsdk.enums.PointCloudReturnMode: ...

    @point_cloud_return_mode.setter
    def point_cloud_return_mode(self, mode: livoxsdk.enums.PointCloudReturnMode) -> None: ...
