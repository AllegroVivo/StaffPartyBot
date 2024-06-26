from __future__ import annotations

from typing import TYPE_CHECKING, List

from discord import Interaction, SelectOption, User
from discord.ui import Select

from UI.Common import FroggeView, CloseMessageButton
from Utilities import Timezone

if TYPE_CHECKING:
    pass
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
            placeholder="Select a timezone for this job posting...",
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
