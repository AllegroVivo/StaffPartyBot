from __future__ import annotations

from ._Error import ErrorMessage
################################################################################

__all__ = ("UnauthorizedError",)

################################################################################
class UnauthorizedError(ErrorMessage):

    def __init__(self):

        super().__init__(
            title="Unauthorized User",
            message="You are not authorized to perform this action.",
            solution="Please contact an administrator for assistance."
        )
        
################################################################################
        