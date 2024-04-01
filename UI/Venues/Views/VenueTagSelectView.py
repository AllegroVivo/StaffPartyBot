from __future__ import annotations

from discord import Interaction, User
from discord.ui import Select

from UI.Common import FroggeView, CloseMessageButton
from Utilities import VenueForumTag, edit_message_helper
################################################################################

__all__ = ("VenueTagSelectView",)

################################################################################
class VenueTagSelectView(FroggeView):

    def __init__(self,  user: User):
        
        super().__init__(user, close_on_complete=True)
        
        self.add_item(VenueTagSelect())
        self.add_item(CloseMessageButton())
        
################################################################################
class VenueTagSelect(Select):
    
    def __init__(self):
                                   
        super().__init__(
            placeholder="Selecta all applicable venue tags...",
            options=VenueForumTag.select_options(),
            min_values=0,
            max_values=len(VenueForumTag.select_options()),
            disabled=False,
            row=0
        )
        
    async def callback(self, interaction: Interaction):
        self.view.value = [VenueForumTag(int(t)) for t in self.values]
        self.view.complete = True
        
        await edit_message_helper(interaction, embed=self.view.venue.status())
        await self.view.stop()  # type: ignore
    
################################################################################
