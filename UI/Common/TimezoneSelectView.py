from __future__ import annotations

from discord import Interaction, User
from discord.ui import Select

from UI.Common.FroggeView import FroggeView
from UI.Common.CloseMessageButton import CloseMessageButton
from Utilities import Timezone
################################################################################

__all__ = ("TimezoneSelectView",)

################################################################################
class TimezoneSelectView(FroggeView):

    def __init__(self,  user: User):
        
        super().__init__(user, close_on_complete=True)
        
        self.add_item(TimezoneSelect())
        self.add_item(CloseMessageButton())
        
################################################################################
class TimezoneSelect(Select):
    
    def __init__(self):
                                   
        super().__init__(
            placeholder="Select a timezone...",
            options=Timezone.select_options(),
            min_values=1,
            max_values=1,
            disabled=False,
            row=0
        )
        
    async def callback(self, interaction: Interaction):
        self.view.value = (Timezone(int(self.values[0])), interaction)
        self.view.complete = True
        
        await self.view.stop()  # type: ignore
    
################################################################################
