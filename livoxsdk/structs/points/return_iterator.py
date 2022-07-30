import typing

from livoxsdk.structs.points.point_return import ReturnUnion, CartesianReturn, SphericalReturn
from livoxsdk.structs.points.return_tag import ReturnTagBitfield


class ReturnIterator:
    def __init__(self, obj: typing.Any, num_returns: int, cartesian: bool):
        self._obj = obj
        self._num_returns: int = num_returns
        if self._num_returns < 1:
            raise ValueError("Must have at least one return")
        self._cartesian: bool = cartesian
        self._index: int = 0

    def __next__(self) -> ReturnUnion:
        if self._index >= self._num_returns:
            raise StopIteration
        # Its ok to increment early because the attribute indices start at 1 instead of 0
        self._index += 1
        if self._cartesian:
            if self._num_returns == 1:
                return CartesianReturn(x=self._obj.x, y=self._obj.y, z=self._obj.z,
                                       reflectivity=self._obj.reflectivity,
                                       tag=(self._obj.tag if hasattr(self._obj, "tag_bitfield") else ReturnTagBitfield()))
            else:
                return CartesianReturn(x=getattr(self._obj, f"x{self._index}"),
                                       y=getattr(self._obj, f"y{self._index}"),
                                       z=getattr(self._obj, f"z{self._index}"),
                                       reflectivity=getattr(self._obj, f"reflectivity{self._index}"),
                                       tag=getattr(self._obj, f"tag{self._index}_bitfield", ReturnTagBitfield()))
        else:
            if self._num_returns == 1:
                return SphericalReturn(theta=self._obj.theta, phi=self._obj.phi, depth=self._obj.depth,
                                       reflectivity=self._obj.reflectivity,
                                       tag=(self._obj.tag if hasattr(self._obj, "tag_bitfield") else ReturnTagBitfield()))
            else:
                return SphericalReturn(theta=self._obj.theta, phi=self._obj.phi,
                                       depth=getattr(self._obj, f"depth{self._index}"),
                                       reflectivity=getattr(self._obj, f"reflectivity{self._index}"),
                                       tag=getattr(self._obj, f"tag{self._index}_bitfield", ReturnTagBitfield()))

    def __len__(self) -> int:
        return self._num_returns
