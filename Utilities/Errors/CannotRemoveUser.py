from __future__ import annotations

from ._Error import ErrorMessage
################################################################################

__all__ = ("CannotRemoveUserError",)

################################################################################
class CannotRemoveUserError(ErrorMessage):

    def __init__(self, cause: str):

        super().__init__(
            title="Cannot Remove User",
            message=(
                f"An error occurred while trying to remove the user from the venue. "
                f"Error: {cause}"
            ),
            solution=(
                "Please try again later. If the problem persists, please contact the "
                "support team for further assistance."
            )
        )
        
################################################################################
        