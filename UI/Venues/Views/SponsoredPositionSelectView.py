from __future__ import annotations

from typing import List

from discord import Interaction, SelectOption, User
from discord.ui import Select

from UI.Common import FroggeView, CloseMessageButton
from Utilities import edit_message_helper
################################################################################

__all__ = ("SponsoredPositionSelectView",)

################################################################################
class SponsoredPositionSelectView(FroggeView):

    def __init__(self,  user: User, options: List[SelectOption]):
        
        super().__init__(user, close_on_complete=True)
        
        self.add_item(PositionSelect(options))
        self.add_item(CloseMessageButton())
        
################################################################################
class PositionSelect(Select):
    
    def __init__(self, options: List[SelectOption]):
        
        if not options:
            options.append(SelectOption(label="No positions available", value="-1"))
                                   
        super().__init__(
            placeholder="Select all positions you want to sponsor...",
            options=options,
            min_values=0,
            max_values=len(options),
            disabled=True if options[0].value == "-1" else False,
            row=0
        )
        
    async def callback(self, interaction: Interaction):
        self.view.value = self.values
        self.view.complete = True
        
        await interaction.respond("** **", delete_after=0.1)
        await self.view.stop()  # type: ignore
    
################################################################################
