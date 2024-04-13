from __future__ import annotations

from typing import TYPE_CHECKING, Optional, List, Any

from discord import Interaction, User, ButtonStyle

from Assets import BotEmojis
from UI.Common import FroggeView, CloseMessageButton, FroggeButton
from Utilities import edit_message_helper

if TYPE_CHECKING:
    from Classes import ProfileDetails, Position, PAvailability
################################################################################

__all__ = ("ProfileDetailsStatusView",)

################################################################################        
class ProfileDetailsStatusView(FroggeView):

    def __init__(self, user: User, details: ProfileDetails):

        super().__init__(user, timeout=300)

        self.details: ProfileDetails = details

        button_list = [
            NameButton(self.details.name),
            CustomURLButton(self.details.url),
            ColorButton(self.details.color),
            SetAvailabilityButton(self.details.availability),
            JobsButton(self.details.jobs),
            RatesButton(self.details.rates),
            PositionsButton(self.details.positions),
            ToggleDMPrefButton(self.details.dm_preference),
            CloseMessageButton()
        ]
        for btn in button_list:
            self.add_item(btn)

################################################################################        
class NameButton(FroggeButton):

    def __init__(self, name: Optional[str]) -> None:

        super().__init__(
            label="Character Name",
            disabled=False,
            row=0
        )
        
        self.set_style(name)

    async def callback(self, interaction: Interaction) -> None:
        await self.view.details.set_name(interaction)
        self.set_style(self.view.details.name)
        
        await interaction.edit(embed=self.view.details.status(), view=self.view)

################################################################################
class CustomURLButton(FroggeButton):
    
    def __init__(self, url: Optional[str]) -> None:
        
        super().__init__(
            label="Custom URL",
            disabled=False,
            row=0
        )
        
        self.set_style(url)
        
    async def callback(self, interaction: Interaction) -> None:
        await self.view.details.set_url(interaction)
        self.set_style(self.view.details.url)

        await interaction.edit(embed=self.view.details.status(), view=self.view)
        
################################################################################
class ColorButton(FroggeButton):
    
    def __init__(self, color: Optional[str]) -> None:
        
        super().__init__(
            label="Accent Color",
            disabled=False,
            row=0
        )
        
        self.set_style(color)
        
    async def callback(self, interaction: Interaction) -> None:
        await self.view.details.set_color(interaction)
        self.set_style(self.view.details.color)

        await interaction.edit(embed=self.view.details.status(), view=self.view)
        
################################################################################
class JobsButton(FroggeButton):
    
    def __init__(self, jobs: Optional[List[str]]) -> None:
        
        super().__init__(
            label="RP Jobs",
            disabled=False,
            row=1
        )
        
        self.set_style(jobs)
        
    async def callback(self, interaction: Interaction) -> None:
        await self.view.details.set_jobs(interaction)
        self.set_style(self.view.details.jobs)

        await interaction.edit(embed=self.view.details.status(), view=self.view)
        
################################################################################
class RatesButton(FroggeButton):
    
    def __init__(self, rates: Optional[str]) -> None:
        
        super().__init__(
            label="Professional Rates",
            disabled=False,
            row=1
        )
        
        self.set_style(rates)
        
    async def callback(self, interaction: Interaction) -> None:
        await self.view.details.set_rates(interaction)
        self.set_style(self.view.details.rates)
        
        await interaction.edit(embed=self.view.details.status(), view=self.view)
        
################################################################################
class PositionsButton(FroggeButton):
    
    def __init__(self, positions: List[Position]) -> None:
        
        super().__init__(
            label="Employable Positions",
            disabled=False,
            row=1
        )
        
        self.set_style(positions)
        
    async def callback(self, interaction: Interaction) -> None:
        await self.view.details.set_positions(interaction)
        self.set_style(self.view.details.positions)

        await edit_message_helper(
            interaction, embed=self.view.details.status(), view=self.view
        )
        
################################################################################
class SetAvailabilityButton(FroggeButton):
    
    def __init__(self, availability: List[PAvailability]) -> None:
        
        super().__init__(
            label="Set Availability",
            disabled=False,
            row=0
        )
        
        self.set_style(availability)
        
    async def callback(self, interaction: Interaction) -> None:
        await self.view.details.set_availability(interaction)
        self.set_style(self.view.details.availability)
        
        await edit_message_helper(
            interaction, embed=self.view.details.status(), view=self.view
        )
        
################################################################################
class ToggleDMPrefButton(FroggeButton):
    
    def __init__(self, dm_pref: bool) -> None:
        
        super().__init__(
            disabled=False,
            row=1
        )
        
        self.set_style(dm_pref)

    def set_style(self, attribute: Optional[Any]) -> None:
        
        if attribute:
            self.style = ButtonStyle.success
            self.label = "Accepting DMs"
            self.emoji = BotEmojis.ThumbsUp
        else:
            self.style = ButtonStyle.danger
            self.label = "Not Accepting DMs"
            self.emoji = BotEmojis.ThumbsDown
        
    async def callback(self, interaction: Interaction) -> None:
        self.view.details.toggle_dm_preference()
        self.set_style(self.view.details.dm_preference)
        
        await interaction.edit(embed=self.view.details.status(), view=self.view)
        
################################################################################
