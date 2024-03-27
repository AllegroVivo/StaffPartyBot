from __future__ import annotations

from ._Error import ErrorMessage
################################################################################

__all__ = ("InvalidSalaryError",)

################################################################################
class InvalidSalaryError(ErrorMessage):

    def __init__(self, value: str):
        super().__init__(
            title="Invalid Salary",
            description=f"Invalid Value: {value}",
            message="The salary you entered is invalid.",
            solution="Enter __**only**__ a whole number, with or without the commas.",
        )

################################################################################
        