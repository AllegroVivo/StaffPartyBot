from __future__ import annotations

from ._Error import ErrorMessage
################################################################################

__all__ = ("NotRegisteredError",)

################################################################################
class NotRegisteredError(ErrorMessage):

    def __init__(self):

        super().__init__(
            title="User Not Registered",
            message="You are not registered in the system.",
            solution="Please speak to administration to get registered."
        )

################################################################################
