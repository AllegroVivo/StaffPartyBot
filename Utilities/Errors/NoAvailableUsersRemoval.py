from __future__ import annotations

from ._Error import ErrorMessage
################################################################################

__all__ = ("NoAvailableUsersRemovalError",)

################################################################################
class NoAvailableUsersRemovalError(ErrorMessage):

    def __init__(self):

        super().__init__(
            title="No Available Users to Remove",
            message=(
                f"No users (aside from yourself) are available to remove "
                f"from the venue."
            ),
            solution=(
                f"Ensure that there are authorized users assigned to the venue, "
                f"besides you, before attempting to remove them."
            )
        )

################################################################################
