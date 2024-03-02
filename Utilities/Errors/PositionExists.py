from __future__ import annotations

from ._Error import ErrorMessage
################################################################################

__all__ = ("PositionExistsError", )

################################################################################
class PositionExistsError(ErrorMessage):

    def __init__(self, position_name: str):

        super().__init__(
            title="Position Exists",
            message=f"The position `{position_name}` already exists.",
            solution=f"Try a different name for the position."
        )
        
################################################################################
        