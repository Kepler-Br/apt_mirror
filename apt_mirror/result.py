from dataclasses import dataclass
from typing import Any, Callable, Optional, TypeVar


_K = TypeVar("_K")
_V = TypeVar("_V")


@dataclass
class Result[_K, _V]:
    value: Optional[_K]
    error: Optional[_V]

    @staticmethod
    def ok(value: _K) -> "Result[_K, _V]":
        return Result(value=value, error=None)

    @staticmethod
    def err(err: _V) -> "Result[_K, _V]":
        return Result(value=None, error=err)

    def unwrap(
        self, msg_on_err: Optional[Callable[[_V], str]] = None
    ) -> _K:
        if self.error is not None or self.value is None:
            error_string = "Unwrapped Result with error"
            if msg_on_err is not None:
                error_string += msg_on_err(self.error) # type: ignore
            raise RuntimeError(error_string)

        return self.value
