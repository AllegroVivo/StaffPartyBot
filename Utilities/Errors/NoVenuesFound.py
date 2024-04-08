from __future__ import annotations

from ._Error import ErrorMessage
################################################################################

__all__ = ("NoVenuesFoundError",)

################################################################################
class NoVenuesFoundError(ErrorMessage):

    def __init__(self):

        super().__init__(
            title="No Venues Found",
            message="You are not registered as a venue owner in the system.",
            solution="Please speak to administration to get registered."
        )

################################################################################
