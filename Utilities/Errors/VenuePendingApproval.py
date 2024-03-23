from __future__ import annotations

from ._Error import ErrorMessage
################################################################################

__all__ = ("VenuePendingApprovalError",)

################################################################################
class VenuePendingApprovalError(ErrorMessage):

    def __init__(self, name: str):
        super().__init__(
            title="Venue Still Pending Approval",
            message=f"Sorry, but the venue '{name}' is still pending approval",
            solution="Please wait for an admin to approve it before trying again."
        )

################################################################################
