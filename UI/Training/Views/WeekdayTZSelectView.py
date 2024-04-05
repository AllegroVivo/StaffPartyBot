from __future__ import annotations

from discord import Interaction, User
from discord.ui import Select

from UI.Common import FroggeView, CloseMessageButton
from Utilities import Weekday, Timezone, edit_message_helper
################################################################################

__all__ = ("WeekdayTZSelectView",)

################################################################################
class WeekdayTZSelectView(FroggeView):

    def __init__(self,  user: User):
        
        super().__init__(user, close_on_complete=True)
        
        self.weekday = None
        
        self.add_item(WeekdaySelect())
        self.add_item(CloseMessageButton())
        
################################################################################
class WeekdaySelect(Select):
    
    def __init__(self):
                                   
        super().__init__(
            placeholder="Select a day of the week to set availability for...",
            options=Weekday.select_options(),
            min_values=1,
            max_values=1,
            disabled=False,
            row=0
        )
        
    async def callback(self, interaction: Interaction):
        self.view.value = Weekday(int(self.values[0]))
        self.view.complete = True

        await interaction.edit()
        await self.view.stop()  # type: ignore
        
        # self.view.add_item(TimezoneSelect())
        # 
        # self.placeholder = self.view.weekday.proper_name
        # self.disabled = True
        # 
        # await edit_message_helper(interaction, view=self.view)
    
################################################################################
class TimezoneSelect(Select):
    
    def __init__(self):
        
        super().__init__(
            placeholder="Select a timezone...",
            options=Timezone.select_options(),
            min_values=1,
            max_values=1,
            disabled=False,
            row=1
        )
        
    async def callback(self, interaction: Interaction):
        self.view.value = self.view.weekday, Timezone(int(self.values[0]))
        self.view.complete = True
        
        await interaction.edit()
        await self.view.stop()  # type: ignore
        
################################################################################
        