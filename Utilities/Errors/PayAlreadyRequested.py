from __future__ import annotations

from ._Error import ErrorMessage
################################################################################

__all__ = ("PayAlreadyRequestedError",)

################################################################################
class PayAlreadyRequestedError(ErrorMessage):

    def __init__(self):

        super().__init__(
            title="Pay Already Requested",
            message=f"You've already requested pay for your currently completed trainings.",
            solution="Please wait for your pay to be processed or contact a staff member for assistance."
        )

################################################################################
