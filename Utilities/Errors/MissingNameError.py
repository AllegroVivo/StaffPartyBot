from __future__ import annotations

from ._Error import ErrorMessage
################################################################################

__all__ = ("MissingNameError",)

################################################################################
class MissingNameError(ErrorMessage):

    def __init__(self):

        super().__init__(
            title="Missing Name",
            message="You must provide at least one character name to continue.",
            solution="Enter your character name(s) and try again."
        )

################################################################################
