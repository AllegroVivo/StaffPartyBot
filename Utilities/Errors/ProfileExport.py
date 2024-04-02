from __future__ import annotations

from ._Error import ErrorMessage
################################################################################

__all__ = ("ProfileExportError",)

################################################################################
class ProfileExportError(ErrorMessage):

    def __init__(self):

        super().__init__(
            title="Profile Export Error",
            message="An error occurred while exporting the profile.",
            solution="Please try again or contact the developer if the problem persists."
        )

################################################################################
