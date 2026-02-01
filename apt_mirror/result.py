from dataclasses import dataclass
from typing import Optional, TypeVar


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
        self, msg_on_err: Optional[str] = None, include_error_value: bool = False
    ) -> _K:
        if self.error is not None or self.value is None:
            error_string = "Unwrapped Result with error"
            if msg_on_err is not None:
                error_string += msg_on_err
            if include_error_value:
                error_string += f". {self.error}"
            raise RuntimeError("Unwrapped Result with error")

        return self.value
