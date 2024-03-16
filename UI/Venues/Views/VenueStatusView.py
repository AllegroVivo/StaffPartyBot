from __future__ import annotations

from typing import TYPE_CHECKING, Optional, List

from discord import Interaction, User, ButtonStyle
from discord.ui import Button

from Assets import BotEmojis
from UI.Common import FroggeView, CloseMessageButton, FroggeButton
from Utilities import edit_message_helper, RPLevel, VenueStyle, VenueSize

if TYPE_CHECKING:
    from Classes import Venue, Position
################################################################################

__all__ = ("VenueStatusView",)

################################################################################
class VenueStatusView(FroggeView):

    def __init__(self, user: User, venue: Venue) -> None:

        super().__init__(user)

        self.venue: Venue = venue

        button_list = [
            EditNameButton(),
            EditDescriptionButton(self.venue.description),
            OpenHoursButton(self.venue.fmt_hours()),
            LocationButton(self.venue.fmt_location()),
            ToggleAcceptingButton(self.venue.accepting_internships),
            RPLevelButton(self.venue.rp_level),
            NSFWToggleButton(self.venue.nsfw),
            VenueStyleButton(self.venue.style),
            VenueSizeButton(self.venue.size),
            LogoButton(self.venue.logo_url),
            SponsorPositionsButton(self.venue.sponsored_positions),
            CloseMessageButton()
        ]
        for btn in button_list:
            self.add_item(btn)

################################################################################
class EditNameButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.primary,
            label="Name",
            disabled=False,
            row=0
        )

    async def callback(self, interaction: Interaction) -> None:
        await self.view.venue.set_name(interaction)
        await interaction.edit(embed=self.view.venue.status())

################################################################################
class EditDescriptionButton(FroggeButton):

    def __init__(self, desc: Optional[str]) -> None:

        super().__init__(
            label="Description",
            disabled=False,
            row=0
        )
        
        self.set_style(desc)

    async def callback(self, interaction: Interaction) -> None:
        await self.view.venue.set_description(interaction)
        self.set_style(self.view.venue.description)
        
        await interaction.edit(embed=self.view.venue.status(), view=self.view)

################################################################################
class RPLevelButton(FroggeButton):

    def __init__(self, level: Optional[RPLevel]) -> None:

        super().__init__(
            label="RP Level",
            disabled=False,
            row=1
        )
        
        self.set_style(level)

    async def callback(self, interaction: Interaction) -> None:
        await self.view.venue.set_level(interaction)
        self.set_style(self.view.venue.rp_level)
        
        await edit_message_helper(
            interaction, embed=self.view.venue.status(), view=self.view
        )

################################################################################
class NSFWToggleButton(FroggeButton):

    def __init__(self, nsfw: bool) -> None:

        super().__init__(
            disabled=False,
            label="NSFW",
            row=1
        )
        
        self._set_style(nsfw)

    def _set_style(self, nsfw: bool) -> None:
        self.style = ButtonStyle.success if nsfw else ButtonStyle.danger

    async def callback(self, interaction: Interaction) -> None:
        await self.view.venue.toggle_nsfw(interaction)
        self._set_style(self.view.venue.nsfw)

        await edit_message_helper(
            interaction, embed=self.view.venue.status(), view=self.view
        )

################################################################################
class VenueStyleButton(FroggeButton):
    
    def __init__(self, style: Optional[VenueStyle]) -> None:
        
        super().__init__(
            label="Venue Style",
            disabled=False,
            row=1
        )
        
        self.set_style(style)
    
    async def callback(self, interaction: Interaction) -> None:
        await self.view.venue.set_style(interaction)       
        self.set_style(self.view.venue.style)
        
        await edit_message_helper(
            interaction, embed=self.view.venue.status(), view=self.view
        )
        
################################################################################
class VenueSizeButton(FroggeButton):

    def __init__(self, size: Optional[VenueSize]) -> None:

        super().__init__(
            label="Venue Size",
            disabled=False,
            row=1
        )
        
        self.set_style(size)

    async def callback(self, interaction: Interaction) -> None:
        await self.view.venue.set_size(interaction)
        self.set_style(self.view.venue.size)
        
        await edit_message_helper(
            interaction, embed=self.view.venue.status(), view=self.view
        )

################################################################################
class OpenHoursButton(FroggeButton):

    def __init__(self, hours: str) -> None:

        super().__init__(
            label="Open Hours",
            row=0
        )
        
        self.set_style(hours)

    async def callback(self, interaction: Interaction) -> None:
        await self.view.venue.set_hours(interaction)
        self.set_style(self.view.venue.fmt_hours())
        
        await edit_message_helper(
            interaction, embed=self.view.venue.status(), view=self.view
        )

################################################################################
class LocationButton(FroggeButton):

    def __init__(self, loc: str) -> None:

        super().__init__(
            label="Location",
            row=0
        )
        
        self.set_style(loc)

    async def callback(self, interaction: Interaction) -> None:
        await self.view.venue.set_location(interaction)
        await edit_message_helper(
            interaction, embed=self.view.venue.status(), view=self.view
        )

################################################################################
class ToggleAcceptingButton(Button):
    
    def __init__(self, accepting: bool) -> None:
        
        super().__init__(
            style=ButtonStyle.success if accepting else ButtonStyle.danger,
            label="Internships",
            disabled=False,
            row=2,
            emoji=BotEmojis.Check if accepting else BotEmojis.ThumbsDown
        )
        
    async def callback(self, interaction: Interaction) -> None:
        await self.view.venue.toggle_accepting(interaction)
        
        self.style = (
            ButtonStyle.success if self.view.venue.accepting_internships 
            else ButtonStyle.danger
        )
        self.emoji = (
            BotEmojis.Check if self.view.venue.accepting_internships 
            else BotEmojis.ThumbsDown
        )
        
        await edit_message_helper(
            interaction, embed=self.view.venue.status(), view=self.view
        )
        
################################################################################
class LogoButton(FroggeButton):

    def __init__(self, logo: Optional[str]) -> None:

        super().__init__(
            label="Logo",
            row=2,
            disabled=False
        )
        
        self.set_style(logo)

    async def callback(self, interaction: Interaction) -> None:
        await self.view.venue.set_logo(interaction)
        self.set_style(self.view.venue.logo_url)
        
        await edit_message_helper(
            interaction, embed=self.view.venue.status(), view=self.view
        )
        
################################################################################
class SponsorPositionsButton(FroggeButton):

    def __init__(self, positions: List[Position]) -> None:

        super().__init__(
            label="Sponsor Position(s)",
            row=2,
            disabled=False
        )
        
        self.set_style(positions)

    async def callback(self, interaction: Interaction) -> None:
        await self.view.venue.set_sponsored_positions(interaction)
        self.set_style(self.view.venue.sponsored_positions)
        
        await edit_message_helper(
            interaction, embed=self.view.venue.status(), view=self.view
        )
        
################################################################################
