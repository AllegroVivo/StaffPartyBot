from __future__ import annotations

from typing import TYPE_CHECKING, Optional, List

from discord import Interaction, User

from UI.Common import FroggeView, CloseMessageButton, ProfileSectionButton

if TYPE_CHECKING:
    from Classes import ProfileDetails
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
            JobsButton(self.details.jobs),
            RatesButton(self.details.rates),
            CloseMessageButton()
        ]
        for btn in button_list:
            self.add_item(btn)

################################################################################        
class NameButton(ProfileSectionButton):

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
class CustomURLButton(ProfileSectionButton):
    
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
class ColorButton(ProfileSectionButton):
    
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
class JobsButton(ProfileSectionButton):
    
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
class RatesButton(ProfileSectionButton):
    
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
