from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Any, Union

from discord import Interaction, User

from UI.Common import FroggeView, CloseMessageButton, ProfileSectionButton
from Utilities import edit_message_helper

if TYPE_CHECKING:
    from Classes import ProfileAtAGlance
################################################################################

__all__ = ("AtAGlanceStatusView",)

################################################################################        
class AtAGlanceStatusView(FroggeView):

    def __init__(self, user: User, aag: ProfileAtAGlance):

        super().__init__(user, timeout=300)

        self.aag: ProfileAtAGlance = aag

        button_list = [
            RaceClanButton(self.aag.race),
            GenderPronounButton(self.aag.gender),
            OrientationButton(self.aag.orientation),
            HeightButton(self.aag.height),
            AgeButton(self.aag.age),
            MareButton(self.aag.mare),
            CloseMessageButton()
        ]
        for btn in button_list:
            self.add_item(btn)

################################################################################        
class GenderPronounButton(ProfileSectionButton):

    def __init__(self, gender: Optional[Any]) -> None:

        super().__init__(
            label="Gender/Pronouns",
            disabled=False,
            row=0
        )
        
        self.set_style(gender)

    async def callback(self, interaction: Interaction) -> None:
        await self.view.aag.set_gender(interaction)
        self.set_style(self.view.aag.gender)

        await edit_message_helper(
            interaction=interaction,
            embed=self.view.aag.status(),
            view=self.view
        )

################################################################################
class RaceClanButton(ProfileSectionButton):
    
    def __init__(self, race: Optional[Any]) -> None:
        
        super().__init__(
            label="Race/Clan",
            disabled=False,
            row=0
        )
        
        self.set_style(race)
        
    async def callback(self, interaction: Interaction) -> None:
        await self.view.aag.set_raceclan(interaction)
        self.set_style(self.view.aag.race)
        
        await edit_message_helper(
            interaction=interaction,
            embed=self.view.aag.status(), 
            view=self.view
        )
        
################################################################################
class OrientationButton(ProfileSectionButton):
    
    def __init__(self, orientation: Optional[Any]) -> None:
        
        super().__init__(
            label="Orientation",
            disabled=False,
            row=0
        )
        
        self.set_style(orientation)
        
    async def callback(self, interaction: Interaction) -> None:
        await self.view.aag.set_orientation(interaction)
        self.set_style(self.view.aag.orientation)

        await edit_message_helper(
            interaction=interaction,
            embed=self.view.aag.status(),
            view=self.view
        )
        
################################################################################
class HeightButton(ProfileSectionButton):
    
    def __init__(self, height: Optional[int]) -> None:
        
        super().__init__(
            label="Height",
            disabled=False,
            row=1
        )
        
        self.set_style(height)
        
    async def callback(self, interaction: Interaction) -> None:
        await self.view.aag.set_height(interaction)
        self.set_style(self.view.aag.height)
        
        await interaction.edit(embed=self.view.aag.status(), view=self.view)
        
################################################################################
class AgeButton(ProfileSectionButton):
    
    def __init__(self, age: Optional[Union[str, int]]) -> None:
        
        super().__init__(
            label="Age",
            disabled=False,
            row=1
        )
        
        self.set_style(age)
        
    async def callback(self, interaction: Interaction) -> None:
        await self.view.aag.set_age(interaction)
        self.set_style(self.view.aag.age)
        
        await interaction.edit(embed=self.view.aag.status(), view=self.view)
        
################################################################################
class MareButton(ProfileSectionButton):

    def __init__(self, mare: Optional[str]) -> None:

        super().__init__(
            label="Mare ID",
            disabled=False,
            row=1
        )
        
        self.set_style(mare)

    async def callback(self, interaction: Interaction) -> None:
        await self.view.aag.set_mare(interaction)
        self.set_style(self.view.aag.mare)

        await interaction.edit(embed=self.view.aag.status(), view=self.view)

################################################################################
