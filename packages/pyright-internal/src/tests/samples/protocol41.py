# This sample verifies that a generic protocol that is specialized with
# a type variable can be matched if that type variable's type is
# supplied by another argument in a call.

from typing import Any, Protocol, TypeVar

_T_co = TypeVar("_T_co", covariant=True)
_T_contra = TypeVar("_T_contra", contravariant=True)


class MyStr:
    ...


class MyBytes:
    def __buffer__(self, __flags: int) -> memoryview:
        ...


MyAnyStr = TypeVar("MyAnyStr", MyStr, MyBytes)


class Buffer(Protocol):
    def __buffer__(self, __flags: int) -> memoryview:
        ...


class SupportsRead(Protocol[_T_co]):
    def read(self, __length: int = ...) -> _T_co:
        ...


class SupportsWrite(Protocol[_T_contra]):
    def write(self, __s: _T_contra) -> object:
        ...


class BufferedWriter:
    def write(self, __buffer: Buffer) -> int:
        raise NotImplementedError


def func1(s: SupportsRead[MyAnyStr], t: SupportsWrite[MyAnyStr]) -> None:
    ...


def test1(src: SupportsRead[MyBytes], tgt: BufferedWriter) -> None:
    func1(src, tgt)


def test2(src: Any, tgt: BufferedWriter) -> None:
    func1(src, tgt)
