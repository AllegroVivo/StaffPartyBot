from __future__ import annotations

from typing import TYPE_CHECKING, Optional, List

from discord import Interaction, User, ButtonStyle
from discord.ui import Button

from Assets import BotEmojis
from UI.Common import FroggeView, CloseMessageButton, FroggeButton
from Utilities import edit_message_helper, RPLevel, VenueSize

if TYPE_CHECKING:
    from Classes import Venue, Position, VenueHours, VenueTag
################################################################################

__all__ = ("VenueStatusView",)

################################################################################
class VenueStatusView(FroggeView):

    def __init__(self, user: User, venue: Venue) -> None:

        super().__init__(user)

        self.venue: Venue = venue

        # If uncommenting any buttons, make sure to check/adjust row numbers accordingly
        button_list = [
            # EditNameButton(),
            # EditDescriptionButton(self.venue.description),
            # SetScheduleButton(self.venue.schedule),
            # LocationButton(self.venue.location.format()),
            # DiscordURLButton(self.venue.discord_url),
            ToggleHiringButton(self.venue.hiring),
            RPLevelButton(self.venue.rp_level),
            # NSFWToggleButton(self.venue.nsfw),
            # VenueTagsButton(self.venue.tags),
            WebsiteURLButton(self.venue.website_url),
            ApplicationURLButton(self.venue.application_url),
            LogoButton(self.venue.logo_url),
            SetPositionsButton(self.venue.positions),
            # RemoveManagerButton(self.venue),
            MuteReportButton(),
            PostVenueButton(),
            UpdateVenueButton(),
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

    def __init__(self, desc: List[str]) -> None:

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
            row=0
        )
        
        self.set_style(level)

    async def callback(self, interaction: Interaction) -> None:
        await self.view.venue.set_rp_level(interaction)
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
class VenueTagsButton(FroggeButton):
    
    def __init__(self, tags: List[VenueTag]) -> None:
        
        super().__init__(
            label="Venue Tags",
            disabled=False,
            row=1
        )
        
        self.set_style(tags)
    
    async def callback(self, interaction: Interaction) -> None:
        await self.view.venue.set_tags(interaction)       
        self.set_style(self.view.venue.tags)
        
        await edit_message_helper(
            interaction, embed=self.view.venue.status(), view=self.view
        )
        
################################################################################
class SetScheduleButton(FroggeButton):

    def __init__(self, hours: List[VenueHours]) -> None:

        super().__init__(
            label="Schedule",
            row=0,
            disabled=False
        )
        
        self.set_style(hours)

    async def callback(self, interaction: Interaction) -> None:
        await self.view.venue.set_schedule(interaction)
        self.set_style(self.view.venue.schedule)
        
        await edit_message_helper(
            interaction, embed=self.view.venue.status(), view=self.view
        )

################################################################################
class LocationButton(FroggeButton):

    def __init__(self, loc: str) -> None:

        super().__init__(
            label="Location",
            row=0,
            disabled=False
        )
        
        self.set_style(loc)

    async def callback(self, interaction: Interaction) -> None:
        await self.view.venue.set_location(interaction)
        self.set_style(self.view.venue.location.format())
        
        await edit_message_helper(
            interaction, embed=self.view.venue.status(), view=self.view
        )

################################################################################
class ToggleHiringButton(Button):
    
    def __init__(self, accepting: bool) -> None:
        
        super().__init__(
            style=ButtonStyle.success if accepting else ButtonStyle.danger,
            label="Hiring",
            disabled=False,
            row=1,
            emoji=BotEmojis.Check if accepting else BotEmojis.ThumbsDown
        )
        
    async def callback(self, interaction: Interaction) -> None:
        await self.view.venue.toggle_hiring(interaction)
        
        self.style = (
            ButtonStyle.success if self.view.venue.hiring else ButtonStyle.danger
        )
        self.emoji = (
            BotEmojis.Check if self.view.venue.hiring else BotEmojis.ThumbsDown
        )
        
        await edit_message_helper(
            interaction, embed=self.view.venue.status(), view=self.view
        )
        
################################################################################
class LogoButton(FroggeButton):

    def __init__(self, logo: Optional[str]) -> None:

        super().__init__(
            label="Logo",
            row=0,
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
class SetPositionsButton(FroggeButton):

    def __init__(self, positions: List[Position]) -> None:

        super().__init__(
            label="Employed Jobs",
            row=1,
            disabled=False
        )
        
        self.set_style(positions)

    async def callback(self, interaction: Interaction) -> None:
        await self.view.venue.set_positions(interaction)
        self.set_style(self.view.venue.positions)
        
        await edit_message_helper(
            interaction, embed=self.view.venue.status(), view=self.view
        )
        
################################################################################
class DiscordURLButton(FroggeButton):
    
    def __init__(self, url: Optional[str]) -> None:
        
        super().__init__(
            label="Discord URL",
            row=0,
            disabled=False
        )
        
        self.set_style(url)
        
    async def callback(self, interaction: Interaction) -> None:
        await self.view.venue.set_discord_url(interaction)
        self.set_style(self.view.venue.discord_url)
        
        await edit_message_helper(
            interaction, embed=self.view.venue.status(), view=self.view
        )
        
################################################################################
class WebsiteURLButton(FroggeButton):
    
    def __init__(self, url: Optional[str]) -> None:
        
        super().__init__(
            label="Website URL",
            row=0,
            disabled=False
        )
        
        self.set_style(url)
        
    async def callback(self, interaction: Interaction) -> None:
        await self.view.venue.set_website_url(interaction)
        self.set_style(self.view.venue.website_url)
        
        await edit_message_helper(
            interaction, embed=self.view.venue.status(), view=self.view
        )
        
################################################################################
class RemoveManagerButton(FroggeButton):

    def __init__(self, venue: Venue) -> None:

        super().__init__(
            label="Remove Manager",
            row=2,
            disabled=False
        )
        
        self.set_style(venue.authorized_users)

    async def callback(self, interaction: Interaction) -> None:
        await self.view.venue.remove_authorized_user(interaction)
        self.set_style(self.view.venue.authorized_users)
        
        await edit_message_helper(
            interaction, embed=self.view.venue.status(), view=self.view
        )
            
################################################################################
class ApplicationURLButton(FroggeButton):
    
    def __init__(self, url: Optional[str]) -> None:
        
        super().__init__(
            label="Application URL",
            row=0,
            disabled=False
        )
        
        self.set_style(url)
        
    async def callback(self, interaction: Interaction) -> None:
        await self.view.venue.set_application_url(interaction)
        self.set_style(self.view.venue.application_url)
        
        await edit_message_helper(
            interaction, embed=self.view.venue.status(), view=self.view
        )
        
################################################################################
class MuteReportButton(FroggeButton):
    
    def __init__(self) -> None:
        
        super().__init__(
            style=ButtonStyle.primary,
            label="Muted User Report",
            row=1,
            disabled=False
        )
        
    async def callback(self, interaction: Interaction) -> None:
        await self.view.venue.mute_list_report(interaction)
        
################################################################################
class PostVenueButton(Button):

    def __init__(self):

        super().__init__(
            style=ButtonStyle.secondary,
            label="Post This Venue Listing",
            disabled=False,
            row=2,
            emoji=BotEmojis.FlyingEnvelope
        )

    async def callback(self, interaction):
        await self.view.venue.post(interaction, None)
        await edit_message_helper(
            interaction, embed=self.view.posting.status()
        )

################################################################################
class UpdateVenueButton(Button):
    
    def __init__(self) -> None:
        
        super().__init__(
            style=ButtonStyle.secondary,
            label="Update This Venue from FFXIV Venues",
            disabled=False,
            row=2,
            emoji=BotEmojis.Cycle
        )
        
    async def callback(self, interaction: Interaction) -> None:
        await interaction.response.defer()
        await self.view.venue.update_from_xiv_venue(interaction)
        
        await edit_message_helper(
            interaction, embed=self.view.posting.status()
        )
        
################################################################################
