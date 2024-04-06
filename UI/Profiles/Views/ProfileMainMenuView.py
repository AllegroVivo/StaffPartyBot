from __future__ import annotations

from typing import TYPE_CHECKING

from discord import Interaction, User, ButtonStyle
from discord.ui import Button

from Assets import BotEmojis
from UI.Common import FroggeView, CloseMessageButton

if TYPE_CHECKING:
    from Classes import Profile
################################################################################

__all__ = ("ProfileMainMenuView",)

################################################################################        
class ProfileMainMenuView(FroggeView):

    def __init__(self, user: User, profile: Profile):

        super().__init__(user, timeout=1200)

        self.profile: Profile = profile

        button_list = [
            DetailsButton(),
            AtAGlanceButton(),
            PersonalityButton(),
            ImagesButton(),
            PreviewProfileButton(),
            PreviewAvailabilityButton(),
            PreviewAboutMeButton(),
            PostOrUpdateButton(),
            ProfileProgressButton(),
            ProfileExportButton(),
            CloseMessageButton()
        ]
        for btn in button_list:
            self.add_item(btn)

################################################################################        
class DetailsButton(Button):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.primary,
            label="Main Info & Details",
            disabled=False,
            row=0
        )

    async def callback(self, interaction: Interaction) -> None:
        await self.view.profile.set_details(interaction)

################################################################################
class AtAGlanceButton(Button):
    
    def __init__(self) -> None:
        
        super().__init__(
            style=ButtonStyle.primary,
            label="At A Glance Section",
            disabled=False,
            row=0
        )
        
    async def callback(self, interaction: Interaction) -> None:
        await self.view.profile.set_ataglance(interaction)
        
################################################################################
class PersonalityButton(Button):
    
    def __init__(self) -> None:
        
        super().__init__(
            style=ButtonStyle.primary,
            label="Personality Elements",
            disabled=False,
            row=0
        )
        
    async def callback(self, interaction: Interaction) -> None:
        await self.view.profile.set_personality(interaction)
        
################################################################################
class ImagesButton(Button):
    
    def __init__(self) -> None:
        
        super().__init__(
            style=ButtonStyle.primary,
            label="View/Remove Images",
            disabled=False,
            row=0
        )
        
    async def callback(self, interaction: Interaction) -> None:
        await self.view.profile.set_images(interaction)
        
################################################################################
class PreviewProfileButton(Button):
    
    def __init__(self) -> None:
        
        super().__init__(
            style=ButtonStyle.primary,
            label="Preview Profile",
            disabled=False,
            row=1
        )
        
    async def callback(self, interaction: Interaction) -> None:
        await self.view.profile.preview_profile(interaction)
        
################################################################################
class PreviewAvailabilityButton(Button):
    
    def __init__(self) -> None:
        
        super().__init__(
            style=ButtonStyle.primary,
            label="Preview Availability",
            disabled=False,
            row=1
        )
        
    async def callback(self, interaction: Interaction) -> None:
        await self.view.profile.preview_availability(interaction)
        
################################################################################
class PreviewAboutMeButton(Button):
    
    def __init__(self) -> None:
        
        super().__init__(
            style=ButtonStyle.primary,
            label="Preview About Me",
            disabled=False,
            row=1
        )
        
    async def callback(self, interaction: Interaction) -> None:
        await self.view.profile.preview_aboutme(interaction)
        
################################################################################
class PostOrUpdateButton(Button):
    
    def __init__(self) -> None:
        
        super().__init__(
            style=ButtonStyle.secondary,
            label="Post/Update Profile",
            disabled=False,
            row=2,
            emoji=BotEmojis.FlyingEnvelope
        )
        
    async def callback(self, interaction: Interaction) -> None:
        await self.view.profile.post(interaction)
        
################################################################################
class ProfileProgressButton(Button):
    
    def __init__(self) -> None:
        
        super().__init__(
            style=ButtonStyle.secondary,
            label="Profile Progress",
            disabled=False,
            row=2,
            emoji=BotEmojis.Goose
        )
        
    async def callback(self, interaction: Interaction) -> None:
        await self.view.profile.progress(interaction)
        
################################################################################
class ProfileExportButton(Button):
    
    def __init__(self) -> None:
        
        super().__init__(
            style=ButtonStyle.secondary,
            label="Export Profile",
            disabled=False,
            row=2,
            emoji=BotEmojis.ArrowRight
        )
        
    async def callback(self, interaction: Interaction) -> None:
        await self.view.profile.export(interaction)
        
################################################################################
