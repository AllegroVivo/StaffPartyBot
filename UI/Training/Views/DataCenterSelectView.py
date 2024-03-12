from __future__ import annotations

from discord import Interaction, User
from discord.ui import Select

from UI.Common import FroggeView, CloseMessageButton
from Utilities import DataCenter
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
            placeholder="Select a data center...",
            options=DataCenter.select_options(),
            min_values=1,
            max_values=1,
            disabled=False,
            row=0
        )
        
    async def callback(self, interaction: Interaction):
        self.view.value = DataCenter(int(self.values[0]))
        self.view.complete = True
        
        await interaction.edit()
        await self.view.stop()  # type: ignore
    
################################################################################
