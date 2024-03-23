from __future__ import annotations

from typing import TYPE_CHECKING, List

from discord import Interaction, SelectOption, User
from discord.ui import Select

from UI.Common import FroggeView, CloseMessageButton

if TYPE_CHECKING:
    from Classes import Venue
################################################################################

__all__ = ("RemoveUserView",)

################################################################################
class RemoveUserView(FroggeView):

    def __init__(self, user: User, venue: Venue):
        
        super().__init__(user, close_on_complete=True)
        
        self.venue: Venue = venue
        
        self.add_item(RemoveUserSelect(self.venue.user_select_options(user)))
        self.add_item(CloseMessageButton())
        
################################################################################
class RemoveUserSelect(Select):
    
    def __init__(self, options: List[SelectOption]):
                                   
        super().__init__(
            placeholder="Select the user(s) to remove...",
            options=options,
            min_values=1,
            max_values=len(options),
            disabled=False,
            row=0
        )
        
    async def callback(self, interaction: Interaction):
        self.view.value = [int(i) for i in self.values]
        self.view.complete = True
        
        await interaction.edit()
        await self.view.stop()  # type: ignore
    
################################################################################
