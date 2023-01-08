import typing

from livoxsdk.structs.points.point_return import ReturnUnion


class ReturnIterator:
    def __init__(self, obj: typing.Any, num_returns: int, cartesian: bool): ...

    def __next__(self) -> ReturnUnion: ...

    def __len__(self) -> int: ...
