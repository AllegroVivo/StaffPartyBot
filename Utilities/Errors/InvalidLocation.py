from __future__ import annotations

from ._Error import ErrorMessage
################################################################################

__all__ = ("InvalidLocationValueError",)

################################################################################
class InvalidLocationValueError(ErrorMessage):

    def __init__(self, field: str, value: str):
        super().__init__(
            title="Invalid Location Value",
            message=f"The value you entered for `{field}` is invalid: `{value}`",
            solution="Enter a whole number.",
        )

################################################################################
        