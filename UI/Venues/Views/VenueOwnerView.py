from __future__ import annotations

from discord import Interaction, User, ButtonStyle
from discord.ui import Button

from UI.Common import FroggeView, CloseMessageButton
################################################################################

__all__ = ("VenueOwnerView",)

################################################################################
class VenueOwnerView(FroggeView):

    def __init__(self,  user: User):
        
        super().__init__(user, close_on_complete=True)
        
        button_list = [
            VenueOwnerButton(),
            VenueManagerButton(),
            CloseMessageButton()
        ]
        for btn in button_list:
            self.add_item(btn)
            
################################################################################
class VenueOwnerButton(Button):
    
    def __init__(self):
                                   
        super().__init__(
            style=ButtonStyle.primary,
            label="Yes, I am the Venue Owner",
            disabled=False,
            row=0
        )
        
    async def callback(self, interaction: Interaction):
        self.view.value = True
        self.view.complete = True
        
        await interaction.edit()
        await self.view.stop()  # type: ignore
    
################################################################################
class VenueManagerButton(Button):

    def __init__(self):

        super().__init__(
            style=ButtonStyle.primary,
            label="No, I am a Venue Manager",
            disabled=False,
            row=0
        )

    async def callback(self, interaction: Interaction):
        self.view.value = False
        self.view.complete = True

        await interaction.edit()
        await self.view.stop()  # type: ignore

################################################################################

