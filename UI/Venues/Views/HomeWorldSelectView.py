from __future__ import annotations

from discord import Interaction, User
from discord.ui import Select

from UI.Common import FroggeView, CloseMessageButton
from Utilities import GameWorld, DataCenter
################################################################################

__all__ = ("HomeWorldSelectView",)

################################################################################
class HomeWorldSelectView(FroggeView):

    def __init__(self,  user: User, dc: DataCenter):
        
        super().__init__(user, close_on_complete=True)
        
        self.add_item(HomeWorldSelect(dc))
        self.add_item(CloseMessageButton())
        
################################################################################
class HomeWorldSelect(Select):
    
    def __init__(self, dc: DataCenter):
                                   
        super().__init__(
            placeholder="Select a home world...",
            options=GameWorld.select_options_by_dc(dc),
            min_values=1,
            max_values=1,
            disabled=False,
            row=0
        )
        
    async def callback(self, interaction: Interaction):
        self.view.value = GameWorld(int(self.values[0]))
        self.view.complete = True
        
        await self.view.edit_message_helper(interaction)
        await self.view.stop()  # type: ignore
    
################################################################################
