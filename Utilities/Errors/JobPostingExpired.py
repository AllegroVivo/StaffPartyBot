from __future__ import annotations

from ._Error import ErrorMessage
################################################################################

__all__ = ("JobPostingExpiredError",)

################################################################################
class JobPostingExpiredError(ErrorMessage):

    def __init__(self):
        super().__init__(
            title="Job Posting Expired",
            message=(
                "This job posting has expired. "
                "Please create a new job posting to continue."
            ),
            solution=(
                "Create a new job posting with the same or similar details. "
                "Make sure to set the expiration date to a later time."
            )
        )

################################################################################
