import abc
import typing

T = typing.TypeVar("T")


class BitField:
    bits: int

    def __init__(self, bits: int):
        self.bits = bits


@typing.runtime_checkable
class CheckableAnnotation(typing.Protocol[T]):
    __slots__ = ()

    @abc.abstractmethod
    def check(self, val: T) -> bool:
        raise NotImplementedError


@typing.runtime_checkable
class Comparable(typing.Protocol[T]):
    __slots__ = ()

    @abc.abstractmethod
    def __lt__(self, other: 'Comparable[T]') -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def __eq__(self, other: 'Comparable[T]') -> bool:
        raise NotImplementedError


assert isinstance(int, Comparable)

_C = typing.TypeVar("_C", bound=Comparable)


class LowerBound(typing.Generic[_C]):
    minimum: _C
    inclusive: bool = True

    def __init__(self, minimum: _C, inclusive: bool = True):
        self.minimum = minimum
        self.inclusive = inclusive

    def check(self, val: _C) -> bool:
        if self.inclusive:
            return val >= self.minimum
        else:
            return val > self.minimum


class UpperBound(typing.Generic[_C]):
    maximum: _C
    inclusive: bool = True

    def __init__(self, maximum: _C, inclusive: bool = True):
        self.maximum = maximum
        self.inclusive = inclusive

    def check(self, val: _C) -> bool:
        if self.inclusive:
            return val <= self.maximum
        else:
            return val < self.maximum


assert isinstance(LowerBound[int](0), CheckableAnnotation)
