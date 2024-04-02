from __future__ import annotations

from ._Error import ErrorMessage
################################################################################

__all__ = ("InvalidWorldNameError",)

################################################################################
class InvalidWorldNameError(ErrorMessage):

    def __init__(self, invalid_value: str):

        super().__init__(
            title="Invalid World Name",
            message=f"You entered `{invalid_value}` for the parent world.",
            solution="Check the world name and try again."
        )

################################################################################
