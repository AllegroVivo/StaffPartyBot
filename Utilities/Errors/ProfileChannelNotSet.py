from __future__ import annotations

from ._Error import ErrorMessage
################################################################################

__all__ = ("ProfileChannelNotSetError",)

################################################################################
class ProfileChannelNotSetError(ErrorMessage):

    def __init__(self):
        super().__init__(
            title="Profile Posting Channel Not Set",
            message="The profile posting channel has not been set for this server.",
            solution=(
                "Please contact a server administrator to set the "
                "profile posting channel."
            )
        )

################################################################################
