from __future__ import annotations

from discord import Interaction, User
from discord.ui import Select

from UI.Common import FroggeView, CloseMessageButton
from Utilities import Weekday
################################################################################

__all__ = ("VenueWeekdaySelectView",)

################################################################################
class VenueWeekdaySelectView(FroggeView):

    def __init__(self,  user: User):
        
        super().__init__(user, close_on_complete=True)
        
        self.add_item(WeekdaySelect())
        self.add_item(CloseMessageButton())
        
################################################################################
class WeekdaySelect(Select):
    
    def __init__(self):
                                   
        super().__init__(
            placeholder="Select a day to set the schedule for...",
            options=Weekday.select_options(),
            min_values=1,
            max_values=1,
            disabled=False,
            row=0
        )
        
    async def callback(self, interaction: Interaction):
        self.view.value = Weekday(int(self.values[0]))
        self.view.complete = True
        
        await self.view.edit_message_helper(interaction)
        await self.view.stop()  # type: ignore
        
################################################################################
