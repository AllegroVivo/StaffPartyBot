from __future__ import annotations

from ._Error import ErrorMessage
################################################################################

__all__ = ("PositionNotFoundError", )

################################################################################
class PositionNotFoundError(ErrorMessage):

    def __init__(self, position_name: str):

        super().__init__(
            title="Position Not Found",
            message=f"The position `{position_name}` was not found.",
            solution=f"Try a different name for the position."
        )

################################################################################
