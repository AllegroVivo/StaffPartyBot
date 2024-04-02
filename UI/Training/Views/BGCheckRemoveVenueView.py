from __future__ import annotations

from typing import TYPE_CHECKING, List

from discord import Interaction, SelectOption, User
from discord.ui import Select

from UI.Common import FroggeView, CloseMessageButton
from Utilities import edit_message_helper

if TYPE_CHECKING:
    from Classes import BackgroundCheck
################################################################################

__all__ = ("BGCheckRemoveVenueView",)

################################################################################
class BGCheckRemoveVenueView(FroggeView):

    def __init__(self,  user: User, bg_check: BackgroundCheck):
        
        super().__init__(user, close_on_complete=True)
        
        options = [
            SelectOption(
                label=f"{v.name}",
                description=f"({v.world})",
                value=v.name
            )
            for v in bg_check.venues
        ]
        
        self.add_item(RemoveVenueSelect(options))
        self.add_item(CloseMessageButton())
        
################################################################################
class RemoveVenueSelect(Select):
    
    def __init__(self, options: List[SelectOption]):
        
        if not options:
            options.append(SelectOption(label="None", value="-1"))
                                   
        super().__init__(
            placeholder="Select a venue to remove...",
            options=options,
            min_values=1,
            max_values=1,
            disabled=True if options[0].value == "-1" else False,
            row=0
        )
        
    async def callback(self, interaction: Interaction):
        self.view.value = self.values[0]
        self.view.complete = True
        
        await edit_message_helper(interaction, view=self.view)
        await self.view.stop()  # type: ignore
    
################################################################################
