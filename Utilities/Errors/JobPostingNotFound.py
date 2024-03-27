from __future__ import annotations

from ._Error import ErrorMessage
################################################################################

__all__ = ("JobPostingNotFoundError",)

################################################################################
class JobPostingNotFoundError(ErrorMessage):

    def __init__(self, post_id: str):

        super().__init__(
            title="Job Posting Not Found",
            message=f"The job posting with ID: `{post_id}` could not be located.",
            solution="Please make sure you are using the correct ID."
        )
        
################################################################################
        