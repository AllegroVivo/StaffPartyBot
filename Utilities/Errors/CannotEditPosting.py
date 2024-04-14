from __future__ import annotations

from ._Error import ErrorMessage
################################################################################

__all__ = ("CannotEditPostingError",)

################################################################################
class CannotEditPostingError(ErrorMessage):

    def __init__(self):
        super().__init__(
            title="Cannot Edit Job Posting",
            message=(
                "This job posting has been accepted or has expired. You may not edit it."
            ),
            solution=(
                "Create a new job posting with the same or similar details. "
                "Make sure to set the expiration date to a later time."
            )
        )

################################################################################
