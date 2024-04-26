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
                "- Name\n"
                "- Availability\n"
                "- Home Region(s)\n"
                "- Employable Positions\n"
            )
        )

################################################################################
