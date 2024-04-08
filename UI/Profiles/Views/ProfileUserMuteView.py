from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from discord import Interaction, ButtonStyle
from discord.ui import View

from UI.Common import FroggeButton

if TYPE_CHECKING:
    from Classes import Profile
################################################################################

__all__ = ("ProfileUserMuteView",)

################################################################################        
class ProfileUserMuteView(View):

    def __init__(self, profile: Profile):

        super().__init__(timeout=None)

        self.profile: Profile = profile
        self.add_item(MuteUserButton(self.profile.id))

################################################################################        
class MuteUserButton(FroggeButton):

    def __init__(self, _id: str) -> None:

        super().__init__(
            style=ButtonStyle.secondary,
            label="Mute/Unmute User",
            disabled=False,
            row=0,
            custom_id=f"mute_user_{_id}"
        )

    async def callback(self, interaction: Interaction) -> None:
        await self.view.profile.venue_mute(interaction)

################################################################################
