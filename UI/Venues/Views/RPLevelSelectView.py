from __future__ import annotations

from typing import TYPE_CHECKING, List

from discord import Interaction, SelectOption, User
from discord.ui import Select

from UI.Common import FroggeView, CloseMessageButton
from Utilities import TrainingLevel, RPLevel, edit_message_helper

if TYPE_CHECKING:
    from Classes import Venue
################################################################################

__all__ = ("RPLevelSelectView",)

################################################################################
class RPLevelSelectView(FroggeView):

    def __init__(self,  user: User, venue: Venue):
        
        super().__init__(user, close_on_complete=True)
        
        self.venue: Venue = venue
        
        self.add_item(RPLevelSelect())
        self.add_item(CloseMessageButton())
        
################################################################################
class RPLevelSelect(Select):
    
    def __init__(self):
                                   
        super().__init__(
            placeholder="Select a RP Level for this venue...",
            options=RPLevel.select_options(),
            min_values=1,
            max_values=1,
            disabled=False,
            row=0
        )
        
    async def callback(self, interaction: Interaction):
        self.view.value = RPLevel(int(self.values[0]))
        self.view.complete = True
        
        await edit_message_helper(interaction, embed=self.view.venue.status())
        await self.view.stop()  # type: ignore
    
################################################################################
