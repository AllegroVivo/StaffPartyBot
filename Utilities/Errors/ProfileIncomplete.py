from __future__ import annotations

from ._Error import ErrorMessage
################################################################################

__all__ = ("ProfileIncompleteError",)

################################################################################
class ProfileIncompleteError(ErrorMessage):

    def __init__(self):
        super().__init__(
            title="Profile Incomplete",
            message="Your profile is incomplete and cannot be posted.",
            solution=(
                "Please ensure that all of the following required fields are "
                "filled out and try again:\n"
                "- Name *(Main Info)*\n"
                "- Availability *(Main Info)*\n"
                "- Employable Positions *(Main Info)*\n"
                "- Home Region(s) *(At a Glance)*\n"
            )
        )

################################################################################
