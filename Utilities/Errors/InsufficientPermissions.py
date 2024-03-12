from __future__ import annotations

from discord import TextChannel

from ._Error import ErrorMessage
################################################################################

__all__ = ("InsufficientPermissionsError",)

################################################################################
class InsufficientPermissionsError(ErrorMessage):

    def __init__(self, channel: TextChannel, permissions_needed: str):
    
        super().__init__(
            title="Insufficient Permissions",
            message=(
                f"You do not have the required permission(s) `{permissions_needed}` "
                f"to perform that action in the channel {channel.mention}."
            ),
            solution="Please contact a server administrator for assistance."
        )

################################################################################
