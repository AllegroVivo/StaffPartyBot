from __future__ import annotations

from discord import Interaction, User
from discord.ui import Select

from UI.Common import FroggeView, CloseMessageButton
from Utilities import edit_message_helper, GlobalDataCenter
################################################################################

__all__ = ("DataCenterSelectView",)

################################################################################
class DataCenterSelectView(FroggeView):

    def __init__(self,  user: User):
        
        super().__init__(user, close_on_complete=True)
        
        self.add_item(DataCenterSelect())
        self.add_item(CloseMessageButton())
        
################################################################################
class DataCenterSelect(Select):
    
    def __init__(self):
                                   
        super().__init__(
            placeholder="Select your home region(s)...",
            options=GlobalDataCenter.select_options(),
            min_values=1,
            max_values=len(GlobalDataCenter.select_options()),
            disabled=False,
            row=0
        )
        
    async def callback(self, interaction: Interaction):
        self.view.value = [GlobalDataCenter(int(dc)) for dc in self.values]
        self.view.complete = True
        
        await edit_message_helper(interaction)
        await self.view.stop()  # type: ignore
    
################################################################################
