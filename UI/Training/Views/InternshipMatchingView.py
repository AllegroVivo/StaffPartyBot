from __future__ import annotations

from typing import TYPE_CHECKING

from discord import Interaction, User
from discord.ui import Select

from UI.Common import FroggeView, CloseMessageButton
from Utilities import RPLevel, NSFWPreference, VenueSize

if TYPE_CHECKING:
    pass
################################################################################

__all__ = ("InternshipMatchingView",)

################################################################################
class InternshipMatchingView(FroggeView):

    def __init__(self,  user: User):
        
        super().__init__(user, close_on_complete=True)
        
        self.add_item(RPLevelSelect())
        self.add_item(CloseMessageButton())
        
################################################################################
class RPLevelSelect(Select):
    
    def __init__(self):
                                   
        super().__init__(
            placeholder="Select your preferred RP level...",
            options=RPLevel.select_options(),
            min_values=1,
            max_values=1,
            disabled=False,
            row=0
        )
        
    async def callback(self, interaction: Interaction):
        self.view.value = [RPLevel(int(self.values[0]))]
        self.view.add_item(NSFWSelect())
        
        self.placeholder = self.view.value[0].proper_name
        self.disabled = True

        await interaction.edit(view=self.view)
    
################################################################################
class NSFWSelect(Select):
    
    def __init__(self):
        
        super().__init__(
            placeholder="Select your comfort level with NSFW...",
            options=NSFWPreference.select_options(),
            min_values=1,
            max_values=1,
            disabled=False,
            row=1
        )
        
    async def callback(self, interaction: Interaction):
        self.view.value.append(NSFWPreference(int(self.values[0])))
        self.view.add_item(VenueSizeSelect())

        self.placeholder = self.view.value[1].proper_name
        self.disabled = True

        await interaction.edit(view=self.view)

################################################################################
class VenueSizeSelect(Select):

    def __init__(self):

        super().__init__(
            placeholder="Select the size of venue you're looking for...",
            options=VenueSize.select_options(),
            min_values=1,
            max_values=1,
            disabled=False,
            row=2
        )

    async def callback(self, interaction: Interaction):
        self.view.value.append(VenueSize(int(self.values[0])))
        self.view.add_item(VenueTagSelect())

        self.placeholder = self.view.value[2].proper_name
        self.disabled = True

        await interaction.edit(view=self.view)

################################################################################
class VenueTagSelect(Select):

    def __init__(self):

        super().__init__(
            placeholder="Select up to three venue style tags...",
            options=VenueTag.select_options(),
            min_values=1,
            max_values=3,
            disabled=False,
            row=3
        )

    async def callback(self, interaction: Interaction):
        self.view.value.append([VenueTag(int(v)) for v in self.values])
        self.view.complete = True

        await interaction.edit()
        await self.view.stop()  # type: ignore

################################################################################
