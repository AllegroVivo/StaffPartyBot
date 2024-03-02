from __future__ import annotations
from discord.abc import GuildChannel

from ._Error import ErrorMessage
################################################################################

__all__ = ("ChannelTypeError", )

################################################################################
class ChannelTypeError(ErrorMessage):

    def __init__(self, channel: GuildChannel, expected_type: str):

        super().__init__(
            title="Invalid Channel Type",
            message=f"The channel {channel.mention} is not a `{expected_type}`.",
            solution=f"Please ensure you mention a valid {expected_type}."
        )

################################################################################
