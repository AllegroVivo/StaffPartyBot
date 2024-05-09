from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from discord import Interaction, User, ButtonStyle
from discord.ui import Button

from UI.Common import FroggeView, CloseMessageButton

if TYPE_CHECKING:
    from Classes import Profile
################################################################################

__all__ = ("AdditionalImageView",)

################################################################################        
class ProfilePreView(FroggeView):

    def __init__(self, owner: User, profile: Profile):

        super().__init__(owner, close_on_complete=True)

        self.profile: Profile = profile

        button_list = [
            ProfilePreviewButton(),
            AvailabilityPreviewButton(),
            AboutMePreviewButton(self.profile.aboutme),
            CloseMessageButton()
        ]

        for btn in button_list:
            self.add_item(btn)
            
################################################################################
class ProfilePreviewButton(Button):

    def __init__(self):
        super().__init__(
            style=ButtonStyle.primary,
            label="Main Profile",
            disabled=False,
            row=0
        )

    async def callback(self, interaction: Interaction):
        await self.view.profile.preview_profile(interaction)
        
################################################################################
class AvailabilityPreviewButton(Button):

    def __init__(self):
        super().__init__(
            style=ButtonStyle.primary,
            label="Availability",
            disabled=False,
            row=0
        )

    async def callback(self, interaction: Interaction):
        await self.view.profile.preview_availability(interaction)

################################################################################
class AboutMePreviewButton(Button):

    def __init__(self, cur_val: Optional[str]):
        super().__init__(
            style=ButtonStyle.primary,
            label="About Me",
            disabled=cur_val is None,
            row=0
        )

    async def callback(self, interaction: Interaction):
        await self.view.profile.preview_aboutme(interaction)

################################################################################

